# COC 部落冲突本地自动捐兵脚本

一套 Python 桌面脚本，参考 **BetterGI** 架构：纯上层视觉识别 + 系统级模拟点击，适配雷电安卓模拟器 COC，无任何进程注入/内存读取/网络抓包。

## 目录结构

```
coc_donate_bot/
├── main.py                     # 入口
├── requirements.txt            # 依赖清单
├── screen_capture/             # 窗口截图
│   └── window_capture.py
├── cv_processor/               # 图像预处理 + 模板匹配
│   └── image_pipeline.py
├── ocr_engine/                 # OCR 文字识别 + 关键词匹配
│   └── text_recognizer.py
├── action_controller/          # 曲线鼠标 + 模拟点击
│   └── mouse_clicker.py
├── core_logic/                 # 捐兵循环决策
│   └── donate_engine.py
├── ui_panel/                   # tkinter 桌面 UI
│   └── main_window.py
├── utils/                      # 配置/日志/公共工具
│   ├── config.py
│   ├── logger.py
│   └── common.py
└── data/
    ├── config/
    └── templates/              # 放置模板截图
        ├── request_popup.png
        ├── donate_button.png
        └── close_button.png
```

## 部署运行

1. **环境要求**：Windows 10/11 + Python 3.9 ~ 3.11（推荐 3.10）。
2. **安装依赖**（首次运行前）：
   ```
   cd coc_donate_bot
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **模拟器设置**：
   - 开启雷电模拟器，启动 COC；将游戏置于前台并常驻。
   - 模拟器分辨率推荐 `1280x720` 或 `1920x1080`，DPI `240`。
   - 窗口标题需包含 `雷电`、`ldplayer`、`Clash of Clans`、`COC` 或 `部落冲突` 之一，脚本会自动识别。
4. **模板素材**（首次必须配置）：
   - 用系统自带截图工具，从模拟器中截取三张典型模板（像素越小精度越高，建议 80x80 以内）：
     - `request_popup.png`：部落增援请求弹窗的标题栏或头部。
     - `donate_button.png`：捐兵按钮。
     - `close_button.png`：弹窗关闭按钮。
   - 放到 `coc_donate_bot/data/templates/` 下。
5. **启动**：
   ```
   python main.py
   ```
   打开桌面面板后点击 `启动脚本`；OCR 首次加载模型需约 10~30 秒，属正常现象。

## 可扩展方向（已预留接口但未实现）

- `core_logic.donate_engine` 中 `match_troop_request` 可扩展为优先级列表；
- `screen_capture.window_capture` 可扩展多开/多窗口轮询；
- `utils.config.TROOP_KEYWORD_MAP` 可进一步扩展兵种别名；
- 加入自动造兵/断线重连/日志系统时，建议在 `core_logic/` 下新增子模块。

## 免责声明

纯上层视觉自动化。使用本脚本请遵守游戏厂商用户协议；作者不承担账号相关责任。
