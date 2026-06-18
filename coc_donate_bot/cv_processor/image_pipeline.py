"""图像处理模块：标准化预处理 + 模板匹配。"""
import os
from typing import Optional, Tuple

import cv2
import numpy as np

from utils.config import MATCH_CONFIDENCE_THRESHOLD
from utils.logger import get_logger

logger = get_logger("cv_processor")


def preprocess(frame: np.ndarray) -> np.ndarray:
    """标准化预处理流水线：灰度 → 高斯模糊 → 二值化 → 形态学去噪。"""
    if frame is None or frame.size == 0:
        return frame
    gray = frame if frame.ndim == 2 else cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, binary = cv2.threshold(gray, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return cleaned


def crop_roi(frame: np.ndarray,
             x_ratio: float, y_ratio: float,
             w_ratio: float, h_ratio: float) -> np.ndarray:
    """按相对比例裁剪 ROI。ratio ∈ [0,1]。"""
    if frame is None:
        return frame
    h, w = frame.shape[:2]
    x = int(w * x_ratio)
    y = int(h * y_ratio)
    rw = int(w * w_ratio)
    rh = int(h * h_ratio)
    x = max(0, min(x, w - 1))
    y = max(0, min(y, h - 1))
    rw = max(1, min(rw, w - x))
    rh = max(1, min(rh, h - y))
    return frame[y:y + rh, x:x + rw]


def load_template(template_path: str) -> Optional[np.ndarray]:
    if not template_path or not os.path.exists(template_path):
        logger.debug("template not found: %s", template_path)
        return None
    try:
        img = cv2.imread(template_path)
        if img is None:
            return None
        return img
    except Exception as exc:
        logger.error("read template %s failed: %s", template_path, exc)
        return None


def match_template(frame: np.ndarray, template: np.ndarray,
                   threshold: float = MATCH_CONFIDENCE_THRESHOLD
                   ) -> Optional[Tuple[int, int, int, int, float]]:
    """在 frame 中匹配 template，返回 (x, y, w, h, confidence) 或 None。"""
    if frame is None or template is None:
        return None
    try:
        if frame.ndim == 3:
            f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            f_gray = frame
        if template.ndim == 3:
            t_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        else:
            t_gray = template

        th, tw = t_gray.shape[:2]
        fh, fw = f_gray.shape[:2]
        if th >= fh or tw >= fw:
            return None

        res = cv2.matchTemplate(f_gray, t_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val >= threshold:
            x, y = max_loc
            return int(x), int(y), int(tw), int(th), float(max_val)
        return None
    except Exception as exc:
        logger.error("match template failed: %s", exc)
        return None


def find_all_matches(frame: np.ndarray, template: np.ndarray,
                     threshold: float = MATCH_CONFIDENCE_THRESHOLD,
                     nms_dist: int = 20):
    """多目标匹配，返回列表 [(x, y, w, h, conf)]。"""
    if frame is None or template is None:
        return []
    try:
        if frame.ndim == 3:
            f_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            f_gray = frame
        if template.ndim == 3:
            t_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        else:
            t_gray = template

        th, tw = t_gray.shape[:2]
        fh, fw = f_gray.shape[:2]
        if th >= fh or tw >= fw:
            return []

        res = cv2.matchTemplate(f_gray, t_gray, cv2.TM_CCOEFF_NORMED)
        ys, xs = np.where(res >= threshold)
        candidates = []
        for x, y in zip(xs, ys):
            candidates.append((int(x), int(y), int(tw), int(th),
                               float(res[y, x])))
        candidates.sort(key=lambda c: c[4], reverse=True)

        kept = []
        for c in candidates:
            cx, cy = c[0] + c[2] // 2, c[1] + c[3] // 2
            dup = False
            for k in kept:
                kx, ky = k[0] + k[2] // 2, k[1] + k[3] // 2
                if abs(cx - kx) < nms_dist and abs(cy - ky) < nms_dist:
                    dup = True
                    break
            if not dup:
                kept.append(c)
        return kept
    except Exception as exc:
        logger.error("find all matches failed: %s", exc)
        return []
