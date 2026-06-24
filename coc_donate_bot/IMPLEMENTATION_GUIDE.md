# COC 自动捐兵脚本实现指南

## 一、项目架构与目录结构

```
coc_donate_bot/
├── action_controller/      # 键鼠操作模块
│   ├── __init__.py
│   └── mouse_clicker.py    # 曲线移动、随机点击
├── core_logic/             # 业务逻辑模块
│   ├── __init__.py
│   └── donate_engine.py    # 捐兵主循环、状态机
├── cv_processor/           # 图像处理模块
│   ├── __init__.py
│   └── image_pipeline.py   # 模板匹配、颜色检测
├── data/
│   └── templates/          # 模板图片目录
│       ├── request_popup.png
│       ├── donate_button.png
│       └── reinforce_window.png
├── ocr_engine/             # OCR文字识别模块
│   ├── __init__.py
│   └── text_recognizer.py  # EasyOCR识别
├── screen_capture/         # 窗口截图模块
│   ├── __init__.py
│   └── window_capture.py   # 窗口定位、精准截图
├── ui_panel/               # 桌面UI模块
│   ├── __init__.py
│   └── main_window.py      # Tkinter控制面板
├── utils/                  # 工具模块
│   ├── __init__.py
│   ├── common.py           # 通用工具函数
│   ├── config.py           # 配置常量
│   └── logger.py           # 日志输出
├── main.py                 # 入口文件
└── requirements.txt        # 依赖清单
```

---

## 二、核心功能需求

### 2.1 功能概述

| 功能模块 | 描述 | 状态 |
|---------|------|------|
| 窗口检测 | 自动识别雷电模拟器中的COC游戏窗口 | 已实现 |
| 截图捕获 | 精准截取游戏窗口画面 | 已实现 |
| 请求检测 | 识别增援请求弹窗（模板+OCR） | 已实现 |
| 坐标校准 | 解决DPI缩放、窗口边框导致的点击偏移 | **待实现** |
| 增援窗口检测 | 检测增援资源选择窗口 | **待实现** |
| 高亮兵种识别 | 通过颜色饱和度区分可捐赠兵种 | **待实现** |
| 兵种选择策略 | 优先捐赠请求的兵种 | **待实现** |

### 2.2 捐兵流程状态机

```
待机状态 → 检测到增援请求 → 点击增援按钮 → 
    检测增援窗口 → 识别高亮兵种 → 选择兵种 → 
    点击捐赠 → 等待动画 → 完成 → 返回待机
```

---

## 三、技术方案详解

### 3.1 坐标校准方案

#### 问题分析

| 误差来源 | 影响 | 解决方案 |
|---------|------|---------|
| 窗口边框/标题栏 | 点击偏下偏右 | 使用客户区坐标 |
| DPI缩放 | 坐标缩放偏差 | 启用DPI感知 |
| 模拟器渲染偏移 | 画面错位 | 相对坐标+校准偏移 |

#### 实现代码

```python
# 在 screen_capture/window_capture.py 中添加
import ctypes
import win32gui
import win32api

# 启用DPI感知
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class GameWindow:
    def get_client_rect(self):
        """获取窗口客户区的屏幕坐标"""
        if self.hwnd is None:
            return None
        
        # 获取客户区相对于窗口左上角的坐标（总是(0,0,w,h)）
        client_rect = win32gui.GetClientRect(self.hwnd)
        left, top, right, bottom = client_rect
        width = right - left
        height = bottom - top
        
        # 转换客户区左上角为屏幕坐标
        client_screen_pos = win32gui.ClientToScreen(self.hwnd, (0, 0))
        
        return {
            'left': client_screen_pos[0],
            'top': client_screen_pos[1],
            'width': width,
            'height': height
        }
    
    def window_to_screen(self, x, y):
        """将窗口客户区坐标转换为屏幕坐标"""
        client = self.get_client_rect()
        if client is None:
            return x, y
        
        # 应用校准偏移（可配置）
        return (
            client['left'] + x + self.calibration_offset_x,
            client['top'] + y + self.calibration_offset_y
        )
```

### 3.2 高亮兵种识别方案

#### 技术原理

**核心思想**：高亮卡片饱和度高，灰色卡片饱和度低

```python
# 在 cv_processor/image_pipeline.py 中添加
import cv2
import numpy as np

def detect_highlighted_units(frame, roi, rows=2, cols=7):
    """
    检测高亮兵种卡片
    :param frame: 截图（BGR格式）
    :param roi: 兵种区域 (x, y, w, h)
    :param rows: 行数（兵种2行，法术1行）
    :param cols: 列数（固定7列）
    :return: 高亮位置列表 [(row, col), ...]
    """
    x, y, w, h = roi
    unit_area = frame[y:y+h, x:x+w]
    
    cell_w = w // cols
    cell_h = h // rows
    
    highlighted = []
    
    for row in range(rows):
        for col in range(cols):
            cx = col * cell_w
            cy = row * cell_h
            cell = unit_area[cy:cy+cell_h, cx:cx+cell_w]
            
            # 转换为HSV空间
            hsv = cv2.cvtColor(cell, cv2.COLOR_BGR2HSV)
            saturation = hsv[:, :, 1]
            
            # 计算平均饱和度
            avg_saturation = np.mean(saturation)
            
            # 饱和度 > 80 视为高亮
            if avg_saturation > 80:
                highlighted.append((row, col))
    
    return highlighted
```

### 3.3 兵种选择策略

```python
# 在 core_logic/donate_engine.py 中添加
def select_unit(highlighted_units, is_troops=True):
    """
    选择要捐赠的兵种
    :param highlighted_units: 高亮位置列表
    :param is_troops: True=兵种, False=法术
    :return: 选中位置 (row, col)
    """
    total_units = 14 if is_troops else 7
    
    # 情况1：有限制请求（部分高亮）
    if 0 < len(highlighted_units) < total_units:
        # 按列排序，选择最左边的
        highlighted_units.sort(key=lambda pos: pos[1])
        return highlighted_units[0]
    
    # 情况2：无限制请求（全部高亮或全部灰色）
    else:
        # 按预设优先级选择
        priority = get_unit_priority(is_troops)
        for idx in priority:
            row = idx // 7
            col = idx % 7
            if (row, col) in highlighted_units or len(highlighted_units) == 0:
                return (row, col)
    
    return None

def get_unit_priority(is_troops=True):
    """获取兵种/法术优先级列表（0-13或0-6）"""
    if is_troops:
        # 兵种优先级：野蛮人>弓箭手>巨人>哥布林>...
        return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    else:
        # 法术优先级
        return [0, 1, 2, 3, 4, 5, 6]
```

### 3.4 完整捐兵流程

```python
# 在 core_logic/donate_engine.py 中
def _donate_cycle(self):
    """单次捐兵循环"""
    # 1. 等待增援窗口出现
    frame = self._capture_frame()
    if not self._is_reinforce_window_open(frame):
        return False
    
    # 2. 获取兵种区域ROI
    troops_roi = self._get_troops_region(frame)
    spells_roi = self._get_spells_region(frame)
    
    if troops_roi is None:
        return False
    
    # 3. 检测高亮兵种
    highlighted_troops = detect_highlighted_units(frame, troops_roi)
    highlighted_spells = detect_highlighted_units(frame, spells_roi, rows=1)
    
    # 4. 选择并点击兵种（直到捐满15个）
    donated_count = 0
    while donated_count < 15:
        selected = select_unit(highlighted_troops)
        if selected is None:
            break
        
        # 点击兵种卡片
        self._click_unit(frame, troops_roi, selected[0], selected[1])
        donated_count += 1
        
        # 等待卡片移动动画
        random_sleep(0.3, 0.5)
        
        # 重新检测（可能有冷却）
        frame = self._capture_frame()
        highlighted_troops = detect_highlighted_units(frame, troops_roi)
    
    # 5. 捐赠法术（如果有）
    if highlighted_spells and donated_count > 0:
        selected_spell = select_unit(highlighted_spells, is_troops=False)
        if selected_spell:
            self._click_unit(frame, spells_roi, selected_spell[0], selected_spell[1])
    
    return True

def _click_unit(self, frame, roi, row, col):
    """点击指定位置的兵种卡片"""
    x, y, w, h = roi
    cell_w = w // 7
    cell_h = h // (2 if 'troop' in str(roi) else 1)
    
    # 计算卡片中心
    center_x = x + col * cell_w + cell_w // 2
    center_y = y + row * cell_h + cell_h // 2
    
    # 转换为屏幕坐标并点击
    screen_x, screen_y = self.game_window.window_to_screen(center_x, center_y)
    human_click_region(screen_x, screen_y, rand=5)
```

---

## 四、配置参数

```python
# 在 utils/config.py 中添加

# 增援窗口配置
REINFORCE_WINDOW_TEMPLATE = os.path.join(TEMPLATE_DIR, "reinforce_window.png")
REINFORCE_WINDOW_THRESHOLD = 0.75

# 兵种/法术区域配置（需要校准）
# 格式：(x, y, w, h) - 相对于游戏窗口客户区左上角
TROOPS_REGION = (80, 180, 580, 260)    # 兵种区域
SPELLS_REGION = (80, 460, 580, 140)    # 法术区域

# 颜色检测配置
HIGHLIGHT_SATURATION_THRESHOLD = 80

# 坐标校准偏移（手动微调）
CALIBRATION_OFFSET_X = 0
CALIBRATION_OFFSET_Y = 0

# 捐兵配置
MAX_TROOPS_PER_DONATION = 15
MAX_SPELLS_PER_DONATION = 2

# 兵种优先级配置（索引对应2行×7列）
TROOP_PRIORITY = [
    0,   # 野蛮人
    1,   # 弓箭手
    2,   # 巨人
    3,   # 哥布林
    4,   # 骷髅兵
    5,   # 气球
    6,   # 法师
    7,   # 炸弹人
    8,   # 女武神
    9,   # 小亡灵
    10,  # 骷髅法师
    11,  # 野猪骑士
    12,  # 法师
    13,  # 飞龙
]
```

---

## 五、实现步骤

### 步骤1：准备模板图片

| 模板 | 说明 | 截图位置 |
|-----|------|---------|
| `request_popup.png` | 增援请求弹窗标题 | 部落聊天中的增援请求横幅 |
| `donate_button.png` | 绿色增援按钮 | 请求弹窗右下角的绿色按钮 |
| `reinforce_window.png` | 增援资源窗口 | 点击增援后弹出的窗口标题栏 |

### 步骤2：启用DPI感知

修改 `screen_capture/window_capture.py`：
- 添加 `ctypes.windll.shcore.SetProcessDpiAwareness(1)`
- 实现 `get_client_rect()` 方法
- 修改 `window_to_screen()` 使用客户区坐标

### 步骤3：实现颜色检测

修改 `cv_processor/image_pipeline.py`：
- 添加 `detect_highlighted_units()` 函数
- 添加饱和度计算逻辑

### 步骤4：实现捐兵逻辑

修改 `core_logic/donate_engine.py`：
- 添加 `_donate_cycle()` 方法
- 添加 `select_unit()` 方法
- 添加 `_click_unit()` 方法
- 修改主循环调用捐兵流程

### 步骤5：校准测试

1. 运行脚本，观察点击位置偏差
2. 调整 `CALIBRATION_OFFSET_X/Y` 进行微调
3. 调整 `TROOPS_REGION/SPELLS_REGION` 精确定位

---

## 六、调试方法

### 6.1 调试输出

```python
# 在关键位置添加调试日志
logger.info(f"Window client rect: {client_rect}")
logger.info(f"Highlighted troops: {highlighted_troops}")
logger.info(f"Selected unit: {selected} at ({screen_x}, {screen_y})")
logger.info(f"Donated {donated_count} troops")
```

### 6.2 截图保存

```python
# 在检测失败时保存截图用于分析
cv2.imwrite(f"debug_{timestamp}.png", frame)
```

### 6.3 校准工具

```python
# 添加校准模式
def calibration_mode():
    """手动校准模式"""
    while True:
        frame = capture_frame()
        cv2.imshow("Calibration", frame)
        
        # 点击窗口中的某个位置
        # 显示该位置的坐标
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
```

---

## 七、测试验证清单

| 测试项 | 预期结果 |
|-------|---------|
| 窗口检测 | 正确识别COC游戏窗口 |
| 截图功能 | 截取的画面清晰，无黑边 |
| 请求检测 | 能识别增援请求弹窗 |
| 增援窗口检测 | 点击增援按钮后能检测到窗口 |
| 高亮识别 | 正确区分高亮/灰色兵种 |
| 兵种选择 | 优先选择请求的兵种 |
| 点击精度 | 点击位置准确落在卡片中心 |
| 捐兵完成 | 成功捐赠15个兵种 |

---

## 八、常见问题排查

### Q1：点击位置偏差

**原因**：DPI缩放、窗口边框、校准偏移

**解决**：
1. 启用DPI感知
2. 使用客户区坐标
3. 调整 `CALIBRATION_OFFSET_X/Y`

### Q2：兵种识别错误

**原因**：饱和度阈值不合适、ROI区域错误

**解决**：
1. 调整 `HIGHLIGHT_SATURATION_THRESHOLD`
2. 调整 `TROOPS_REGION` 坐标

### Q3：增援窗口检测不到

**原因**：模板不匹配、窗口位置变化

**解决**：
1. 重新截取模板图片
2. 降低匹配阈值
3. 添加OCR辅助检测

### Q4：脚本运行卡顿

**原因**：EasyOCR加载慢、截图频率过高

**解决**：
1. 预加载OCR模型
2. 降低截图频率
3. 使用多线程

---

## 九、性能优化建议

### 9.1 减少截图频率

```python
# 设置合理的检测间隔
LOOP_INTERVAL = 1.0  # 每秒检测一次
```

### 9.2 预加载模板

```python
# 在启动时预加载所有模板
templates = {
    'request': load_template('request_popup.png'),
    'donate': load_template('donate_button.png'),
    'reinforce': load_template('reinforce_window.png'),
}
```

### 9.3 多线程处理

```python
# OCR识别放在单独线程
ocr_thread = threading.Thread(target=ocr_worker)
ocr_thread.daemon = True
ocr_thread.start()
```

---

## 十、安全注意事项

### 10.1 防封禁措施

| 措施 | 说明 |
|-----|------|
| 随机延时 | 每次操作间隔随机0.2-1.2秒 |
| 曲线移动 | 模拟人手移动轨迹 |
| 点击抖动 | 每次点击偏移±3像素 |
| 限制频率 | 每分钟最多捐5次 |

### 10.2 异常处理

```python
try:
    # 捐兵逻辑
except Exception as e:
    logger.error(f"Donate failed: {e}")
    # 等待后重试
    random_sleep(5, 10)
```

---

## 十一、扩展功能规划

### Phase 1（当前）
- [ ] 基础捐兵功能
- [ ] 坐标校准
- [ ] 高亮兵种识别

### Phase 2
- [ ] 兵种优先级配置
- [ ] 法术捐赠支持
- [ ] 日志系统

### Phase 3
- [ ] 自动造兵
- [ ] 断线重连
- [ ] 多账号管理

---

## 十二、启动说明

```bash
# 安装依赖
pip install -r requirements.txt

# 准备模板图片
# 将 request_popup.png、donate_button.png、reinforce_window.png 放入 data/templates/

# 运行脚本
python main.py

# 点击UI面板的"启动"按钮开始运行
```

---

**文档版本**: v1.0  
**创建日期**: 2024-01-XX  
**适用版本**: Python 3.9+