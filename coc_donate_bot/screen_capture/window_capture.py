"""窗口截图模块：查找雷电模拟器/COC游戏窗口并精准截取。"""
import os
from typing import Optional, Tuple

import numpy as np

from utils.config import WINDOW_KEYWORDS
from utils.logger import get_logger

logger = get_logger("screen_capture")


def _try_import_pygetwindow():
    try:
        import pygetwindow as gw
        return gw
    except Exception as exc:
        logger.warning("pygetwindow import failed: %s", exc)
        return None


def _try_import_mss():
    try:
        import mss
        return mss
    except Exception as exc:
        logger.warning("mss import failed: %s", exc)
        return None


def find_game_window():
    """查找包含关键词的窗口句柄，返回 (left, top, width, height, title)。"""
    gw = _try_import_pygetwindow()
    if gw is None:
        return None

    try:
        windows = gw.getAllWindows()
    except Exception as exc:
        logger.error("get windows failed: %s", exc)
        return None

    for w in windows:
        try:
            title = (w.title or "").strip()
        except Exception:
            continue
        if not title:
            continue
        for kw in WINDOW_KEYWORDS:
            if kw.lower() in title.lower():
                try:
                    if w.width <= 0 or w.height <= 0:
                        continue
                    return (int(w.left), int(w.top),
                            int(w.width), int(w.height), title)
                except Exception:
                    continue
    return None


def capture_region(region: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
    """截取屏幕指定区域 (left, top, width, height)，返回 BGR numpy 数组。"""
    mss_lib = _try_import_mss()
    if mss_lib is None:
        return None

    left, top, width, height = region
    try:
        with mss_lib.mss() as sct:
            monitor = {"left": int(left), "top": int(top),
                       "width": int(width), "height": int(height)}
            shot = sct.grab(monitor)
            frame = np.array(shot, dtype=np.uint8)
            if frame.ndim == 2:
                return frame
            rgba = frame[:, :, :4]
            bgr = rgba[:, :, :3][:, :, ::-1].copy()
            return bgr
    except Exception as exc:
        logger.error("capture failed: %s", exc)
        return None


class GameWindow:
    """封装游戏窗口的定位与截图能力。"""

    def __init__(self):
        self.region: Optional[Tuple[int, int, int, int]] = None
        self.title: Optional[str] = None
        self.try_refresh()

    def try_refresh(self) -> bool:
        info = find_game_window()
        if info is None:
            self.region = None
            self.title = None
            return False
        left, top, width, height, title = info
        self.region = (left, top, width, height)
        self.title = title
        return True

    def capture(self) -> Optional[np.ndarray]:
        if self.region is None:
            if not self.try_refresh():
                return None
        return capture_region(self.region)

    def screen_to_window(self, sx: int, sy: int) -> Tuple[int, int]:
        left, top, _, _ = self.region or (0, 0, 0, 0)
        return int(sx - left), int(sy - top)

    def window_to_screen(self, wx: int, wy: int) -> Tuple[int, int]:
        left, top, _, _ = self.region or (0, 0, 0, 0)
        return int(wx + left), int(wy + top)
