# VSCode Claude Code 完整使用教程

## 目录

- [快速入门](#一快速入门)
- [前置校验与安装](#二前置校验与安装)
- [完整API与全局配置](#三完整api与全局配置)
- [面板操作与快捷键体系](#四面板操作与快捷键体系)
- [核心基础功能](#五核心基础功能)
- [内置斜杠命令大全](#六内置斜杠命令大全)
- [分场景提示词模板库](#七分场景提示词模板库)
- [项目级批量操作与进阶技巧](#八项目级批量操作与进阶技巧)
- [项目规范固化：CLAUDE.md](#九项目规范固化claudemd)
- [性能优化与Token节省](#十性能优化与token节省)
- [故障排查指南](#十一故障排查指南)
- [安全最佳实践](#十二安全最佳实践)
- [附录](#附录)

---

## 一、快速入门

### 5分钟快速上手

如果你是第一次使用Claude Code并且在终端下载了Claude Code，按照以下步骤快速开始：

#### 步骤1：安装扩展（1分钟）

1. 打开VSCode
2. 按 `Ctrl+Shift+X` 或最左侧第五个图标打开扩展市场
3. 搜索 `Claude Code`
4. 点击第一个插件安装，重启VSCode

#### 步骤2：配置API密钥（2分钟）

1. 按 `Ctrl`+`,` 打开设置
2. 搜索 `Claude Code: Edit in settings.json`
3. 下滑点击蓝色链接`settings.json`打开配置文件
4. 添加最简配置：

```json
{
  "claudeCode.environmentVariables": [
    {
      "name": "ANTHROPIC_AUTH_TOKEN",
      "value": "sk-你的API密钥"
    }
  ]
}
```
- 备注：如果使用第三方中转工具比如CC Switch配置过API Key,后台挂CC优先级高于VS Code，使用时直接挂在后台就可以。
#### 步骤3：开始使用（2分钟）

1. 点击编辑器右上角火花图标 ✨ 打开Claude面板
2. 输入你的第一个指令：

```
你好，请帮我解释一下当前打开的文件
```

3. 按 `Enter` 发送，Claude会自动读取当前文件并给出解释

#### 恭喜！你已经开始使用Claude Code了

继续阅读后续章节，了解更多高级功能和最佳实践。

---

## 二、前置校验与安装

### 1. 环境要求

| 项目 | 要求 | 说明 |
|------|------|------|
| VSCode版本 | ≥ 1.98.0 | 旧版会出现功能缺失、面板打不开 |
| 操作系统 | Windows/macOS/Linux | 全平台支持 |
| 网络环境 | 能访问Claude API | 国内用户需要配置中转 |

### 2. 账号准备

- **官方账号**: 在 [Anthropic官网](https://www.anthropic.com) 注册
`https://www.anthropic.com`
- **中转服务**: 选择合规的中转平台获取API Key

### 3. VSCode扩展安装

安装以下两个扩展：

1. **Claude Code for VS Code** - 核心扩展
2. **Chinese (Simplified)** - 简体中文语言包（可选）

安装后重启VSCode生效。

### 4. 验证安装

安装完成后，检查以下项目：

- [ ] 右上角出现火花图标 ✨
- [ ] 底部状态栏显示"Claude Code"
- [ ] 按 `Ctrl+Shift+P` 输入"Claude"能看到相关命令

---

## 三、完整API与全局配置

### 1. 打开配置文件

**方法一：通过设置界面**

1. 快捷键 `Ctrl`+`,` 打开设置
2. 搜索框输入：`Claude Code: Edit in settings.json`
3. 向下滚动找到蓝色链接"在settings.json中编辑"
4. 点击打开配置文件

**方法二：直接打开**

1. 按 `Ctrl+Shift+P` 打开命令面板
2. 输入 `Preferences: Open User Settings (JSON)`
3. 直接编辑配置文件

### 2. 完整配置模板

#### 方案A：官方API直连配置

```json
{
  // 基础连接配置
  "claudeCode.environmentVariables": [
    {
      "name": "ANTHROPIC_AUTH_TOKEN",
      "value": "sk-ant-api03-你的官方密钥"
    },
    {
      "name": "ANTHROPIC_MODEL",
      "value": "claude-sonnet-4"
    }
  ],

  // 界面与默认行为
  "claudeCode.preferredLocation": "panel",
  "claudeCode.initialPermissionMode": "plan",
  "claudeCode.useTerminal": false,
  "claudeCode.showTokenUsageInStatusBar": true,

  // 效率快捷键开关
  "claudeCode.enableInlineEditShortcut": true,
  "claudeCode.autoInsertAtMention": true
}
```

#### 方案B：中转API配置

```json
{
  // 基础连接配置
  "claudeCode.environmentVariables": [
    {
      "name": "ANTHROPIC_AUTH_TOKEN",
      "value": "sk-你的中转密钥"
    },
    {
      "name": "ANTHROPIC_BASE_URL",
      "value": "https://你的中转域名/v1"
    },
    {
      "name": "ANTHROPIC_MODEL",
      "value": "claude-sonnet-4"
    }
  ],

  // 界面与默认行为
  "claudeCode.preferredLocation": "panel",
  "claudeCode.initialPermissionMode": "plan",
  "claudeCode.useTerminal": false,
  "claudeCode.showTokenUsageInStatusBar": true,

  // 效率快捷键开关
  "claudeCode.enableInlineEditShortcut": true,
  "claudeCode.autoInsertAtMention": true
}
```

### 3. 配置参数详解

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ANTHROPIC_AUTH_TOKEN` | string | - | API密钥，必填 |
| `ANTHROPIC_BASE_URL` | string | - | 中转地址，官方直连可省略 |
| `ANTHROPIC_MODEL` | string | claude-sonnet-4 | 模型选择 |
| `preferredLocation` | string | panel | 面板位置：panel/sidebar |
| `initialPermissionMode` | string | plan | 权限模式：plan/ask/auto |
| `useTerminal` | boolean | false | 是否使用终端模式 |
| `showTokenUsageInStatusBar` | boolean | true | 状态栏显示Token消耗 |
| `enableInlineEditShortcut` | boolean | true | 启用内联编辑快捷键 |
| `autoInsertAtMention` | boolean | true | 输入@自动检索文件 |

### 4. 模型选择建议

| 模型 | 特点 | 适用场景 |
|------|------|----------|
| `claude-sonnet-4` | 平衡性能与成本 | 日常开发、代码补全 |
| `claude-opus-4` | 最强推理能力 | 复杂重构、架构设计 |
| `claude-haiku-3.5` | 快速响应 | 简单查询、快速迭代 |

**推荐配置**：日常使用 `claude-sonnet-4`，复杂任务临时切换到 `claude-opus-4`。

### 5. CC Switch用户配置

如果你已经使用CC Switch接入中转，可以简化配置：

```json
{
  "claudeCode.preferredLocation": "panel",
  "claudeCode.initialPermissionMode": "plan",
  "claudeCode.useTerminal": false,
  "claudeCode.showTokenUsageInStatusBar": true,
  "claudeCode.enableInlineEditShortcut": true,
  "claudeCode.autoInsertAtMention": true
}
```

使用时确保CC Switch在后台运行即可。

---

## 四、面板操作与快捷键体系

### 1. 打开Claude面板

**方式一：图标点击**
- 点击编辑器右上角火花图标 ✨（最快）

**方式二：状态栏**
- 点击底部状态栏"Claude Code"文字

**方式三：命令面板**
- 按 `Ctrl+Shift+P`
- 输入 `Claude Code: Open`

### 2. 核心快捷键速查

| 快捷键 | 功能 | 说明 |
|--------|------|------|
| `Esc` | 中断生成 | 停止AI当前输出 |
| `Esc` `Esc` | 撤销修改 | 回溯上一轮代码修改 |
| `Shift+Tab` | 切换权限模式 | Plan → Auto → Ask 循环 |
| `Enter` | 发送指令 | 发送提示词 |
| `Ctrl+G` | 打开外部编辑框 | 编写长提示词 |
| `Ctrl+R` | 历史记录 | 检索历史对话命令 |
| `Alt+K` | 精准引用 | 插入 `@文件#行号` 格式 |

### 3. 权限模式说明

在输入框底部切换权限模式：

| 模式 | 图标 | 行为 | 适用场景 |
|------|------|------|----------|
| **Plan** | 📋 | 先输出修改方案，确认后执行 | 复杂修改、首次使用 |
| **Ask** | ❓ | 每次修改前弹窗确认 | 安全优先、重要文件 |
| **Auto** | ⚡ | 自动修改，无需确认 | 信任AI、批量操作 |
| **Edit Auto** | ✏️ | 自动编辑选中代码 | 快速局部修改 |

**新手推荐**：默认使用 `Plan` 模式，熟悉后可切换到 `Auto` 提升效率。

### 4. Effort档位

Effort（思考强度）不是权限模式，而是AI思考深度：

| 档位 | 特点 | 适用场景 |
|------|------|----------|
| Low | 快速响应 | 简单查询、格式化 |
| Medium | 平衡模式 | 日常开发 |
| High | 深度思考 | 复杂重构、架构设计 |

**注意**：档位越高，Token消耗越大，响应越慢。

---

## 五、核心基础功能

### 1. @文件引用系统

AI自动读取指定文件/目录，精准理解项目上下文，无需复制粘贴代码。

#### 引用方式

| 方式 | 语法 | 示例 |
|------|------|------|
| 单文件 | `@文件名` | `@main.py` |
| 精准行号 | `@文件名#起始行-结束行` | `@main.py#25-48` |
| 整个目录 | `@目录路径` | `@src/components` |
| 多文件组合 | 空格分隔 | `@utils.ts @types.d.ts` |

#### 快速引用技巧

1. **选中代码 → Alt+K**：自动生成精准行号引用
2. **拖拽文件**：直接拖拽文件到输入框
3. **输入@触发**：输入`@`后自动弹出文件列表

#### 使用示例

```text
@server/index.ts#10-35
这段接口存在数据库并发冲突，帮我加分布式锁，只修改选中函数，输出完整可运行代码，附带注释
```

### 2. 内联编辑（Inline Edit）

无需打开聊天面板，选中代码直接局部重写，打断思路最少。

#### 操作步骤

1. 选中需要修改的代码
2. 右键选择 `Claude Code: Inline Edit`
3. 输入修改需求
4. 查看差异预览，接受或拒绝修改

#### 适用场景

- 重构单个函数
- 修复单处bug
- 优化算法
- 补充注释

#### 示例需求

```text
将该同步函数改为async/await，增加异常捕获，返回统一格式Result<T>
```

### 3. 代码差异预览

AI修改文件后弹出左右分栏对比：

- **左侧**：原代码
- **右侧**：AI修改后代码

操作选项：
- ✅ 全部接受
- ❌ 全部拒绝
- 📝 部分接受（接受某几行）
- 🔄 发送指令让AI二次调整

### 4. 上下文管理

#### 清空上下文

输入 `/clear` 清空当前对话历史，消除历史干扰。

**使用场景**：
- 切换到完全不相关的任务
- 对话逻辑跑偏
- AI忘记之前的需求

#### 查看Token消耗

输入 `/usage` 查看当前会话Token消耗。

---

## 六、内置斜杠命令大全

在聊天输入框输入 `/` 唤起命令菜单。

### 开发高频命令

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/fix` | 一键修复bug | 快速定位和修复代码错误 |
| `/debug` | 完整调试流程 | 定位→复现→修复→测试 |
| `/doc` | 生成文档 | JSDoc、接口文档、README |
| `/test` | 生成单元测试 | Jest/Pytest/go test |
| `/improve` | 代码优化 | 性能、可读性、规范 |

### 工具命令

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/model` | 切换模型 | opus/sonnet/haiku |
| `/usage` | Token统计 | 控制成本 |
| `/clear` | 清空上下文 | 消除历史干扰 |
| `/file` | 追加文件 | 等价手动@引用 |

### 命令使用示例

#### /fix 示例

```text
@api/login.ts /fix 接口500报错，定位空指针问题
```

#### /debug 示例

```text
@main.py#60-90 /debug
现象：循环读取CSV时内存持续暴涨，程序10分钟崩溃
```

#### /doc 示例

```text
@utils/helper.ts /doc
为所有函数生成JSDoc注释，包含参数说明和返回值类型
```

#### /test 示例

```text
@services/user.ts /test
使用Jest为UserService类生成单元测试，覆盖正常和异常情况
```

---

## 七、分场景提示词模板库

### 模板通用公式

```
@精准代码 + 明确任务 + 约束规则 + 输出格式
```

### 场景1：从零生成完整功能模块

```text
@src/types/user.ts @src/utils/request.ts

任务：创建用户注册接口模块，包含参数校验、密码加密、数据库写入

约束：
1. 使用TypeScript，严格类型定义，禁止any
2. 捕获所有异常，统一返回{code, msg, data}格式
3. 密码使用bcrypt加密，增加重复邮箱校验
4. 只生成service+controller两个文件，不改动已有工具代码

输出：完整文件代码 + 简短使用说明
```

### 场景2：Bug调试

```text
@main.py#60-90 /debug

现象：循环读取CSV时内存持续暴涨，程序10分钟崩溃

约束：
1. 定位内存泄漏点，解释泄漏原因
2. 给出2套优化方案：极简修改版、高性能迭代版
3. 补充一行性能测试代码验证优化效果
4. 不修改文件其他无关逻辑
```

### 场景3：大规模代码重构

```text
@src/views 整个目录

重构需求：
1. 将所有Class Vue组件改为Composition API + <script setup>
2. 统一导入路径别名@/，删除相对../../导入
3. 提取重复弹窗逻辑至hooks/modal.ts公共钩子
4. 先输出修改清单，确认后批量执行修改
```

### 场景4：代码优化

```text
@utils/calc.js /improve

优化要求：
1. 简化嵌套if，使用卫语句提前return
2. 增加入参合法性校验，抛出明确错误信息
3. 删除冗余console.log，替换为日志工具logger
4. 补充边界值测试用例
```

### 场景5：生成项目文档

```text
@src 整个项目目录 /doc

生成完整README.md，包含：
- 环境依赖
- 启动命令
- 目录结构
- 接口清单
- 部署步骤

要求：简洁专业，无多余废话
```

### 场景6：代码审查

```text
@src/api 整个目录

审查要求：
1. 检查SQL注入、XSS等安全漏洞
2. 检查错误处理是否完善
3. 检查代码是否符合项目规范
4. 输出问题清单和修复建议
```

### 场景7：单元测试生成

```text
@src/services/user.ts

任务：为UserService类生成完整单元测试

要求：
1. 使用Jest框架
2. 覆盖所有公共方法
3. 包含正常流程和异常流程
4. Mock外部依赖
5. 测试覆盖率目标：80%+
```

### 场景8：性能优化

```text
@src/components/Dashboard.vue

性能问题：页面加载时卡顿明显，首屏渲染超过3秒

优化要求：
1. 分析性能瓶颈
2. 提出优化方案（懒加载、虚拟滚动、缓存等）
3. 给出具体实现代码
4. 预估优化效果
```

---

## 八、项目级批量操作与进阶技巧

### 1. 批量文件修改

通过 `@文件夹` 让AI一次性处理数十个文件。

#### 示例：批量添加生命周期清理

```text
@src/components

批量修改：所有组件onMounted生命周期增加路由离开销毁监听，清除定时器，防止内存泄漏

约束：
1. 只修改.vue文件，跳过测试文件
2. 保持原有代码风格
3. 输出修改清单，确认后执行
```

### 2. 跨文件依赖分析

适合接手陌生项目、排查循环依赖。

```text
@src 整个项目

分析项目模块依赖：
1. 找出循环导入文件
2. 输出依赖图谱
3. 给出拆分重构方案
```

### 3. 新建整套文件结构

AI自动生成目录和代码。

```text
新建后台权限模块，目录结构：

src/permission/
├── types.ts      # 权限类型定义
├── service.ts    # 接口请求
├── store.ts      # pinia状态管理
└── index.ts      # 统一导出

要求：
- 使用Vue3 + TypeScript + Pinia
- 遵循项目现有代码风格
- 包含完整的类型定义
```

### 4. 代码迁移与升级

```text
@src 整个项目

迁移任务：将Vue2项目升级到Vue3

要求：
1. 先分析需要修改的文件清单
2. 列出breaking changes
3. 分批次执行修改
4. 每批次输出修改摘要
```

### 5. 多文件重构策略

对于大型重构，建议分步骤进行：

**步骤1：分析现状**
```text
@src 整个项目
分析当前代码结构，找出需要重构的模块，输出重构优先级清单
```

**步骤2：制定计划**
```text
根据分析结果，制定分阶段重构计划，每阶段不超过10个文件
```

**步骤3：执行重构**
```text
@src/module1
执行第一阶段重构：[具体重构内容]
```

---

## 九、项目规范固化：CLAUDE.md

在项目根目录新建 `CLAUDE.md`，AI每次对话自动读取，不用每次重复写规范约束，节省Token。

### CLAUDE.md 模板示例

```markdown
# 本项目编码强制规范

## 技术栈
Vue3 + TypeScript + Vite + Pinia + Element Plus

## 代码规则
1. 禁止any，所有变量/函数必须显式定义类型
2. 接口返回统一格式：{ code: number; msg: string; data: T | null }
3. 异步函数全部async/await，拒绝.then嵌套
4. 工具函数统一放入src/utils，组件逻辑抽至hooks
5. 注释：复杂逻辑加单行注释，函数头部加JSDoc

## 命名规范
- 组件：PascalCase（如UserProfile.vue）
- 函数：camelCase（如getUserInfo）
- 常量：UPPER_SNAKE_CASE（如API_BASE_URL）
- 文件：kebab-case（如user-service.ts）

## 输出要求
1. 修改代码只输出变更部分，不要完整复制全文件
2. 每次修改前说明改动目的、影响范围
3. 不自动删除原有业务逻辑，仅优化、新增功能
4. 生成测试用例使用vitest框架

## 禁止事项
- 禁止使用var声明变量
- 禁止在循环中调用异步函数
- 禁止直接修改props
- 禁止在template中使用复杂表达式
```

### 创建后的效果

创建后无需额外操作，任何对话AI都会自动遵循文档规则。

---

## 十、性能优化与Token节省

### 1. 减少Token消耗

| 策略 | 方法 | 效果 |
|------|------|------|
| 精准引用 | 使用 `@文件#行号` 片段引用 | 减少50%+ Token |
| 限定作用域 | 只传当前业务目录 | 避免上下文爆炸 |
| 固化规范 | 使用CLAUDE.md | 提示词不用重复写约束 |
| 分轮拆解 | 复杂任务分多轮 | 避免一次性丢整个项目 |
| 降低温度 | temperature固定0.2 | 减少AI冗余解释文字 |

### 2. 解决响应卡顿

| 问题 | 解决方案 |
|------|----------|
| API延迟高 | 中转API替换低延迟节点 |
| 上下文过大 | 调低maxContextLength |
| 任务过重 | 单次指令只处理一类任务 |
| IO阻塞 | 关闭Auto自动修改 |
| 网络冲突 | 核对代理端口，关闭冲突VPN |

### 3. 成本控制策略

#### Token消耗估算

| 操作类型 | 预估Token |
|----------|-----------|
| 简单查询 | 500-1000 |
| 代码解释 | 1000-2000 |
| 单文件修改 | 2000-5000 |
| 多文件重构 | 5000-20000 |
| 全项目分析 | 20000+ |

#### 成本优化建议

1. **使用合适的模型**
   - 简单任务：claude-haiku-3.5
   - 日常开发：claude-sonnet-4
   - 复杂任务：claude-opus-4

2. **优化提示词**
   - 简洁明确，避免冗余
   - 使用模板减少重复描述
   - 分步骤处理复杂任务

3. **监控使用量**
   - 定期使用 `/usage` 查看消耗
   - 设置预算提醒
   - 分析高消耗操作

### 4. 上下文混乱处理

**症状**：对话逻辑跑偏、AI忘记之前需求

**解决方案**：

1. 输入 `/clear` 清空历史对话
2. 重新发起指令
3. 使用 `@文件` 重新建立上下文

---

## 十一、故障排查指南

### 常见问题FAQ

#### Q1：面板打不开或显示空白

**症状**：点击火花图标无反应，或面板显示空白

**解决方案**：

1. 检查VSCode版本是否 ≥ 1.98.0
2. 重启VSCode
3. 禁用其他可能冲突的扩展
4. 查看输出面板（`Ctrl+Shift+U`）的错误日志
5. 重新安装Claude Code扩展

#### Q2：API连接失败

**症状**：提示"Connection refused"或"Timeout"

**解决方案**：

1. 检查API密钥是否正确
2. 检查网络是否能访问Claude API
3. 中转用户检查 `ANTHROPIC_BASE_URL` 配置
4. 检查代理设置是否正确
5. 尝试切换到其他网络环境

#### Q3：响应速度慢

**症状**：AI响应时间超过30秒

**解决方案**：

1. 切换到更快的模型（haiku）
2. 减少上下文大小（使用精准引用）
3. 更换低延迟的中转节点
4. 检查网络延迟
5. 分步骤处理复杂任务

#### Q4：Token消耗过快

**症状**：Token消耗速度超出预期

**解决方案**：

1. 使用 `@文件#行号` 精准引用
2. 避免传入整个大文件
3. 使用 `/clear` 清空无用上下文
4. 创建CLAUDE.md固化规范
5. 切换到haiku模型处理简单任务

#### Q5：代码修改不符合预期

**症状**：AI修改的代码不是想要的结果

**解决方案**：

1. 使用Plan模式，先查看修改方案
2. 更明确地描述需求
3. 提供更多上下文和约束条件
4. 使用差异预览仔细检查
5. 分步骤处理复杂修改

#### Q6：快捷键不生效

**症状**：按快捷键无反应

**解决方案**：

1. 检查快捷键是否被其他扩展占用
2. 在VSCode快捷键设置中查看冲突
3. 重新设置快捷键
4. 重启VSCode

#### Q7：中文显示乱码

**症状**：中文字符显示异常

**解决方案**：

1. 确保文件编码为UTF-8
2. 安装Chinese语言包
3. 检查VSCode编码设置

### 错误代码对照表

| 错误代码 | 含义 | 解决方案 |
|----------|------|----------|
| 401 | 认证失败 | 检查API密钥是否正确 |
| 403 | 权限不足 | 检查账号权限或密钥有效期 |
| 429 | 请求过于频繁 | 降低请求频率，稍后重试 |
| 500 | 服务器错误 | 稍后重试，或联系服务商 |
| 502/504 | 网关超时 | 检查网络，更换中转节点 |

---

## 十二、安全最佳实践

### 1. API密钥管理

#### 安全存储

```json
// ❌ 错误做法：硬编码密钥
"ANTHROPIC_AUTH_TOKEN": "sk-ant-api03-xxxxx"

// ✅ 正确做法：使用环境变量
"ANTHROPIC_AUTH_TOKEN": "${ANTHROPIC_API_KEY}"
```

#### 密钥轮换

- 定期更换API密钥（建议每3个月）
- 发现泄露立即更换
- 不同环境使用不同密钥

#### 权限控制

- 使用最小权限原则
- 为不同项目创建独立密钥
- 设置使用量上限

### 2. 敏感信息处理

#### 不要提交到版本控制

```gitignore
# .gitignore
.env
.env.local
*.key
secrets.json
```

#### 代码中避免硬编码

```typescript
// ❌ 错误做法
const apiKey = "sk-ant-api03-xxxxx";

// ✅ 正确做法
const apiKey = process.env.ANTHROPIC_API_KEY;
```

### 3. 代码审查

#### AI生成代码的审查要点

- [ ] 检查是否有安全漏洞（SQL注入、XSS等）
- [ ] 检查是否暴露敏感信息
- [ ] 检查错误处理是否完善
- [ ] 检查是否符合项目规范
- [ ] 检查是否有性能问题

### 4. 数据隐私

#### 不要发送到AI的内容

- 真实的用户密码
- 生产环境密钥
- 个人身份信息（PII）
- 财务敏感数据
- 商业机密

#### 安全处理方式

```typescript
// 使用脱敏数据
const testData = {
  email: "test@example.com",
  password: "******",
  apiKey: "sk-test-xxxxx"
};
```

### 5. 团队协作安全

#### 共享配置

```json
// 创建 .vscode/settings.json（提交到版本控制）
{
  "claudeCode.preferredLocation": "panel",
  "claudeCode.initialPermissionMode": "plan"
}

// API密钥由每个开发者单独配置
```

#### 代码审查流程

1. AI生成代码后，必须经过人工审查
2. 使用Plan模式预览修改
3. 重要文件使用Ask模式确认
4. 定期审计AI生成的代码

---

## 附录

### 附录A：快捷键速查表

| 快捷键 | 功能 | 使用频率 |
|--------|------|----------|
| `Esc` | 中断生成 | ⭐⭐⭐ |
| `Esc` `Esc` | 撤销修改 | ⭐⭐ |
| `Shift+Tab` | 切换权限模式 | ⭐⭐⭐ |
| `Enter` | 发送指令 | ⭐⭐⭐ |
| `Ctrl+G` | 外部编辑框 | ⭐ |
| `Ctrl+R` | 历史记录 | ⭐⭐ |
| `Alt+K` | 精准引用 | ⭐⭐⭐ |

### 附录B：配置参数速查表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ANTHROPIC_AUTH_TOKEN` | string | - | API密钥（必填） |
| `ANTHROPIC_BASE_URL` | string | - | 中转地址 |
| `ANTHROPIC_MODEL` | string | claude-sonnet-4 | 模型选择 |
| `preferredLocation` | string | panel | 面板位置 |
| `initialPermissionMode` | string | plan | 权限模式 |
| `useTerminal` | boolean | false | 终端模式 |
| `showTokenUsageInStatusBar` | boolean | true | Token显示 |
| `enableInlineEditShortcut` | boolean | true | 内联编辑 |
| `autoInsertAtMention` | boolean | true | 自动@引用 |

### 附录C：模型对比表

| 模型 | 速度 | 智能度 | 成本 | 适用场景 |
|------|------|--------|------|----------|
| claude-haiku-3.5 | ⚡⚡⚡ | ⭐⭐ | 💰 | 简单查询、快速迭代 |
| claude-sonnet-4 | ⚡⚡ | ⭐⭐⭐ | 💰💰 | 日常开发、代码补全 |
| claude-opus-4 | ⚡ | ⭐⭐⭐⭐ | 💰💰💰 | 复杂重构、架构设计 |

### 附录D：常用斜杠命令

| 命令 | 用途 | 示例 |
|------|------|------|
| `/fix` | 修复bug | `@file.ts /fix 空指针错误` |
| `/debug` | 调试 | `@module.ts /debug` |
| `/doc` | 生成文档 | `@service.ts /doc` |
| `/test` | 生成测试 | `@utils.ts /test` |
| `/improve` | 优化代码 | `@code.js /improve` |
| `/model` | 切换模型 | `/model opus` |
| `/usage` | Token统计 | `/usage` |
| `/clear` | 清空上下文 | `/clear` |

### 附录E：日常高效工作流

#### 写代码流程

```
1. Alt+K 引用依赖文件
2. 输入清晰结构化指令
3. Plan模式确认修改
4. 查看差异预览
5. 接受或调整
```

#### 改单函数流程

```
1. 选中代码
2. 右键 Inline Edit
3. 输入修改需求
4. 快速局部调整
```

#### 调试bug流程

```
1. @代码片段 /debug
2. 查看分析结果
3. 确认修复方案
4. 执行修复
```

#### 批量重构流程

```
1. @目录 + 明确修改规则
2. 查看修改清单
3. 确认后批量执行
4. 验证结果
```

#### 项目收尾流程

```
1. /doc 生成注释和文档
2. /test 补充测试用例
3. 代码审查
4. 提交代码
```

---

## 结语

本教程涵盖了VSCode Claude Code从入门到进阶的完整使用指南。建议：

1. **新手**：先完成快速入门，熟悉基本操作
2. **进阶**：深入学习提示词模板和批量操作
3. **高级**：掌握性能优化和安全最佳实践

持续学习和实践，让Claude Code成为你的高效编程助手！

---

> **文档维护**
> - 发现问题或有建议？欢迎反馈
> - 定期更新以跟进Claude Code新功能
> - 推荐收藏本教程作为日常参考手册