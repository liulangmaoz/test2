"""COC 本地自动捐兵脚本入口。

用法：
    pip install -r requirements.txt
    python main.py
"""
import os
import sys

from ui_panel import MainPanel


def _ensure_dirs():
    base = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base)
    for d in ("data", "data/templates", "data/config"):
        os.makedirs(os.path.join(base, d), exist_ok=True)


def main():
    _ensure_dirs()
    app = MainPanel()
    app.run()


if __name__ == "__main__":
    main()
