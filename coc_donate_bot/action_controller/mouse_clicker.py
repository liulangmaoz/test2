"""键鼠操作模块：模拟人手曲线移动 + 随机延时。"""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import math
import random
import time
from typing import Tuple

from utils import config as cfg
from utils.logger import get_logger

logger = get_logger("action")


def _try_pyautogui():
    try:
        import pyautogui
        pyautogui.FAILSAFE = False
        return pyautogui
    except Exception as exc:
        logger.warning("pyautogui import failed: %s", exc)
        return None


def _curve_points(start: Tuple[int, int], end: Tuple[int, int],
                  steps: int = 20):
    """生成贝塞尔风格的曲线移动点序列。"""
    x0, y0 = start
    x1, y1 = end
    cx = (x0 + x1) / 2 + random.uniform(-40, 40)
    cy = (y0 + y1) / 2 + random.uniform(-40, 40)
    points = []
    for i in range(steps + 1):
        t = i / steps
        inv = 1 - t
        x = inv * inv * x0 + 2 * inv * t * cx + t * t * x1
        y = inv * inv * y0 + 2 * inv * t * cy + t * t * y1
        points.append((int(x), int(y)))
    return points


def move_to(x: int, y: int) -> bool:
    """曲线移动鼠标到屏幕坐标 (x, y)。"""
    pg = _try_pyautogui()
    if pg is None:
        return False
    try:
        cur = pg.position()
        start = (int(cur[0]), int(cur[1]))
        end = (int(x) + random.randint(-cfg.CLICK_OFFSET_PIXEL, cfg.CLICK_OFFSET_PIXEL),
               int(y) + random.randint(-cfg.CLICK_OFFSET_PIXEL, cfg.CLICK_OFFSET_PIXEL))
        dist = math.hypot(end[0] - start[0], end[1] - start[1])
        steps = max(8, min(30, int(dist / 25)))
        points = _curve_points(start, end, steps)
        duration = random.uniform(cfg.MOUSE_MOVE_DURATION_MIN,
                                  cfg.MOUSE_MOVE_DURATION_MAX)
        step_t = duration / steps
        for px, py in points:
            pg.moveTo(px, py, duration=0)
            time.sleep(step_t / max(1, steps // 8))
        return True
    except Exception as exc:
        logger.error("move_to failed: %s", exc)
        return False


def click(x: int = None, y: int = None) -> bool:
    """在目标位置执行左键点击；若未传入坐标则在当前位置点击。"""
    pg = _try_pyautogui()
    if pg is None:
        return False
    try:
        if x is not None and y is not None:
            ok = move_to(x, y)
            if not ok:
                return False
        time.sleep(random.uniform(0.05, 0.2))
        pg.mouseDown()
        time.sleep(random.uniform(0.05, 0.15))
        pg.mouseUp()
        return True
    except Exception as exc:
        logger.error("click failed: %s", exc)
        return False


def human_click_region(screen_center_x: int, screen_center_y: int,
                       rand: int = 4) -> bool:
    cx = screen_center_x + random.randint(-rand, rand)
    cy = screen_center_y + random.randint(-rand, rand)
    return click(cx, cy)
