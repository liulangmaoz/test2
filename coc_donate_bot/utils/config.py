"""全局配置常量：阈值、时间、关键词等集中管理。"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "data", "templates")

WINDOW_KEYWORDS = ["雷电", "ldplayer", "Clash of Clans", "COC", "部落冲突"]

LOOP_SLEEP_MIN = 0.2
LOOP_SLEEP_MAX = 1.2
IDLE_SLEEP_MIN = 1.5
IDLE_SLEEP_MAX = 3.0

MATCH_CONFIDENCE_THRESHOLD = 0.82
OCR_MIN_CONFIDENCE = 0.3

MOUSE_MOVE_DURATION_MIN = 0.25
MOUSE_MOVE_DURATION_MAX = 0.6
CLICK_OFFSET_PIXEL = 3

SUPPORTED_TROOPS = [
    "超弓", "超级弓箭", "冰人", "法师", "亡灵",
    "皮卡", "气球", "飞龙", "女巫", "巨石",
    "哥布林", "野蛮人", "弓箭手", "巨人", "武神",
]

TROOP_KEYWORD_MAP = {
    "超弓": ["超弓", "超级弓箭", "超级弓", "超弓手"],
    "冰人": ["冰人", "冰石头人", "寒冰"],
    "法师": ["法师", "魔法师"],
    "亡灵": ["亡灵", "小亡灵"],
    "皮卡": ["皮卡", "皮卡超人"],
    "气球": ["气球", "气球兵"],
    "飞龙": ["飞龙", "龙"],
    "女巫": ["女巫"],
    "巨石": ["巨石", "巨石投手"],
    "哥布林": ["哥布林", "哥布"],
    "野蛮人": ["野蛮人", "黄毛"],
    "弓箭手": ["弓箭手", "弓箭"],
    "巨人": ["巨人"],
    "武神": ["武神", "女武神"],
}

REQUEST_POPUP_KEYWORDS = ["需要", "增援", "部落增援", "请求", "要"]
REQUEST_POPUP_TEMPLATE = os.path.join(TEMPLATE_DIR, "request_popup.png")
DONATE_BUTTON_TEMPLATE = os.path.join(TEMPLATE_DIR, "donate_button.png")
LOG_FILE = os.path.join(BASE_DIR, "data", "coc_donate.log")
