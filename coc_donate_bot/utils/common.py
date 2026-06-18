"""通用工具函数：随机延时、异常捕获装饰器等。"""
import os
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import random
import time
from functools import wraps

from utils import config as cfg
from utils.logger import get_logger

logger = get_logger("utils")


def random_sleep(a: float = None, b: float = None) -> float:
    if a is None:
        a = cfg.LOOP_SLEEP_MIN
    if b is None:
        b = cfg.LOOP_SLEEP_MAX
    t = random.uniform(a, b)
    time.sleep(t)
    return t


def safe_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            logger.error("call %s failed: %s", func.__name__, exc)
            return None
    return wrapper
