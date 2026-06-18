"""OCR 文字识别模块：本地离线识别 + 关键词匹配。"""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from typing import List, Optional

import numpy as np

from utils import config as cfg
from utils.logger import get_logger

logger = get_logger("ocr_engine")

_reader_instance = None


def _get_reader(lang: List[str] = None):
    global _reader_instance
    if _reader_instance is not None:
        return _reader_instance
    try:
        import easyocr
        _reader_instance = easyocr.Reader(lang or ["ch_sim", "en"],
                                          gpu=False, verbose=False)
        return _reader_instance
    except Exception as exc:
        logger.error("easyocr init failed: %s", exc)
        return None


def recognize_text(frame: np.ndarray) -> List[str]:
    """识别 ROI 内文字，返回文本行列表。"""
    if frame is None or frame.size == 0:
        return []
    reader = _get_reader()
    if reader is None:
        return []
    try:
        results = reader.readtext(frame, detail=1, paragraph=False)
    except Exception as exc:
        logger.error("ocr failed: %s", exc)
        return []
    lines = []
    for item in results:
        if len(item) < 3:
            continue
        text, conf = item[1], item[2]
        if conf and float(conf) >= cfg.OCR_MIN_CONFIDENCE:
            t = str(text).strip()
            if t:
                lines.append(t)
    return lines


def match_troop_request(lines: List[str]) -> Optional[str]:
    """从 OCR 文本中匹配预设兵种关键词，返回兵种名或 None。"""
    if not lines:
        return None
    text = "".join(lines)
    for troop, keywords in cfg.TROOP_KEYWORD_MAP.items():
        for kw in keywords:
            if kw in text:
                return troop
    return None


def is_request_popup(lines: List[str]) -> bool:
    if not lines:
        return False
    text = "".join(lines)
    return any(kw in text for kw in cfg.REQUEST_POPUP_KEYWORDS)
