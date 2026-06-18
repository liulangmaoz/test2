"""极简桌面 UI 面板：启停按钮 + 状态显示。"""
import tkinter as tk
from tkinter import ttk

from core_logic import DonateEngine
from utils.logger import get_logger

logger = get_logger("ui")


class MainPanel:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("COC 自动捐兵面板")
        self.root.geometry("360x200")
        self.root.resizable(False, False)

        self.engine = DonateEngine(on_status=self._update_status_threadsafe)
        self._status_var = tk.StringVar(value="待启动")
        self._count_var = tk.StringVar(value="捐兵次数：0")

        self._build()

    def _build(self):
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)

        title = ttk.Label(frame, text="COC 本地自动捐兵",
                          font=("Microsoft YaHei", 14, "bold"))
        title.pack(pady=(0, 8))

        status_box = ttk.LabelFrame(frame, text="运行状态")
        status_box.pack(fill="x", pady=6)
        ttk.Label(status_box, textvariable=self._status_var,
                  font=("Microsoft YaHei", 11)).pack(padx=8, pady=6)

        ttk.Label(frame, textvariable=self._count_var).pack(anchor="w")

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=10)
        self.start_btn = ttk.Button(btn_frame, text="启动脚本",
                                    command=self._on_start)
        self.start_btn.pack(side="left", expand=True, fill="x", padx=4)
        self.stop_btn = ttk.Button(btn_frame, text="停止脚本",
                                   command=self._on_stop, state="disabled")
        self.stop_btn.pack(side="left", expand=True, fill="x", padx=4)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_start(self):
        self.engine.start()
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

    def _on_stop(self):
        self.engine.stop()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def _update_status_threadsafe(self, text: str):
        try:
            self.root.after(0, self._set_status, text)
        except Exception:
            pass

    def _set_status(self, text: str):
        self._status_var.set(text)
        try:
            self._count_var.set(f"捐兵次数：{self.engine.donate_count}")
        except Exception:
            pass

    def _on_close(self):
        try:
            self.engine.stop()
        finally:
            self.root.destroy()

    def run(self):
        self.root.mainloop()
