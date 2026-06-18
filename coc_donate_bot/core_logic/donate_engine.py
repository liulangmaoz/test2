"""核心捐兵业务逻辑：循环调度 + 决策判断。"""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import threading
import time
from typing import Callable, Optional

import numpy as np

from action_controller import click, human_click_region
from cv_processor import (
    crop_roi, load_template, match_template,
)
from ocr_engine import is_request_popup, match_troop_request, recognize_text
from screen_capture import GameWindow
from utils.common import random_sleep
from utils import config as cfg
from utils.logger import get_logger

logger = get_logger("core_logic")


class DonateEngine:
    """捐兵引擎：在独立线程中运行识别循环。"""

    def __init__(self, on_status: Optional[Callable[[str], None]] = None):
        self.game_window = GameWindow()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._on_status = on_status or (lambda s: None)
        self.donate_count = 0

    def _set_status(self, text: str):
        try:
            self._on_status(text)
        except Exception:
            pass

    def is_running(self) -> bool:
        return self._running

    def start(self):
        if self._running:
            return
        self._running = True
        self._set_status("启动中...")
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logger.info("engine started")

    def stop(self):
        self._running = False
        self._set_status("已停止")
        logger.info("engine stop requested")

    def _click_match(self):
        """识别 + 决策 + 操作 单轮逻辑。"""
        if not self.game_window.try_refresh() or self.game_window.region is None:
            self._set_status("未找到游戏窗口")
            random_sleep(cfg.IDLE_SLEEP_MIN, cfg.IDLE_SLEEP_MAX)
            return

        frame = self.game_window.capture()
        if frame is None:
            self._set_status("截图失败，重试中")
            return

        popup_tpl = load_template(cfg.REQUEST_POPUP_TEMPLATE)
        popup_box = None
        if popup_tpl is not None:
            popup_box = match_template(frame, popup_tpl)

        # 优先走 OCR，识别中心区域
        popup_roi = crop_roi(frame, 0.15, 0.20, 0.70, 0.55)
        lines = recognize_text(popup_roi)

        has_request = (popup_box is not None) or is_request_popup(lines)

        if not has_request:
            self._set_status("待机中，未发现增援请求")
            random_sleep(cfg.IDLE_SLEEP_MIN, cfg.IDLE_SLEEP_MAX)
            return

        troop = match_troop_request(lines)
        if troop is None:
            troop = "(未识别兵种)"
            self._set_status(f"发现请求，未解析兵种")
        else:
            self._set_status(f"发现请求: {troop}")

        # 尝试点击捐兵按钮
        donate_tpl = load_template(cfg.DONATE_BUTTON_TEMPLATE)
        donated = False
        if donate_tpl is not None:
            box = match_template(frame, donate_tpl)
            if box:
                x, y, w, h, conf = box
                sx, sy = self.game_window.window_to_screen(x + w // 2, y + h // 2)
                logger.info(f"found donate button at ({sx},{sy}) conf={conf:.3f}")
                if human_click_region(sx, sy):
                    donated = True
                    self.donate_count += 1
                    logger.info("donated %s", troop)
                    time.sleep(0.3)
            else:
                logger.info("donate button template not matched, using fallback")
        else:
            logger.info("donate button template file not found: %s", cfg.DONATE_BUTTON_TEMPLATE)
        if not donated:
            # 兜底：点击画面中央区域（用户需要自行替换坐标/模板）
            # 暂时禁用，等待模板匹配成功
            logger.info("donate button not found, skipping")
            # h, w = frame.shape[:2]
            # sx, sy = self.game_window.window_to_screen(int(w * 0.5), int(h * 0.75))
            # logger.info(f"using fallback click at ({sx},{sy})")
            # human_click_region(sx, sy, rand=20)



        random_sleep()

    def _run_loop(self):
        self._set_status("运行中")
        while self._running:
            try:
                self._click_match()
            except Exception as exc:
                logger.error("loop exception: %s", exc)
                self._set_status("识别异常，自动跳过")
                random_sleep(cfg.IDLE_SLEEP_MIN, cfg.IDLE_SLEEP_MAX)
        self._set_status("已退出")
