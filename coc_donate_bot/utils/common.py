"""通用工具函数：随机延时、异常捕获装饰器等。"""
import random
import time
from functools import wraps

from utils.config import LOOP_SLEEP_MIN, LOOP_SLEEP_MAX
from utils.logger import get_logger

logger = get_logger("utils")


def random_sleep(a: float = LOOP_SLEEP_MIN, b: float = LOOP_SLEEP_MAX) -> float:
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
