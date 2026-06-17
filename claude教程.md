# VSCode Claude Code 使用教程<sup>1</sup>
## 目录
- 前置校验与基础安装
- API 密钥 / 代理完整配置（settings.json 最优配置）
- 面板打开、核心快捷键体系
- 核心基础功能：@文件引用、内联编辑、权限模式
- 内置斜杠/命令全解（开发高频工具）
- 分场景高效提示词模板（写代码 / 调试 / 重构 / 文档）
- 项目级批量操作、多文件重构进阶用法
- 全局规则文件CLAUDE.md固化项目规范
- 性能优化、Token 节省、卡顿解决
- 全开发流程实战（新建项目→调试→测试→上线文档）
- 避坑清单与安全规范
## 一、前置校验与安装
之前出过一期Claude Code安装的详细可行教程，通过CC Switch配置API Key以及前后环境配置，有不懂的可以翻一下。
### 1. 环境要求
- VSCode 版本 ≥ 1.98.0，旧版会出现功能缺失、面板打不开
- Anthropic 官方账号，或合规中转 API Key
### 2. VSCode安装内置插件
这个也在安装Claude Code教程中讲过：
- Claude Code for VS Code
- Chinese(Simplified)(简体中文)
然后重启VS Code生效
## 二、完整 API 与全局配置
### 1.打开配置文件：
- 快捷键`ctrl`+`,`进入设置；
- 搜索:
`Claude Code: Edit in settings.json`
后在任务栏向下滑找到蓝色字体标识的一行`在settings.json中编辑`，点击打开json文件；
- 复制粘贴配置文件：
```
{
  // 1. 基础连接配置
  "claudeCode.environmentVariables": [
    {
      "name": "ANTHROPIC_AUTH_TOKEN",
      "value": "sk-你的API密钥"
    },
    // 官方直连删除本行；中转平台填写对应地址
    {
      "name": "ANTHROPIC_BASE_URL",
      "value": "https://中转域名/v1"
    },
    {
      "name": "ANTHROPIC_MODEL",
      "value": "claude-opus-4-6" // 最强代码模型；轻量用claude-haiku-3
    }
  ],
  // 2. 界面与默认行为
  "claudeCode.preferredLocation": "panel", // panel底部面板 / sidebar侧边栏
  "claudeCode.initialPermissionMode": "plan", // 默认先出修改计划，确认后改代码（最安全）
  "claudeCode.useTerminal": false, // false图形聊天面板，true终端模式
  "claudeCode.showTokenUsageInStatusBar": true, // 底部状态栏显示Token消耗
  // 3. 上下文&生成参数（效率核心）
  "claudeCode.maxContextLength": 8000, // 单次最大上下文Token，项目级可调至12000
  "claudeCode.contextHistoryCount": 12, // 保留最近12轮对话，防止上下文爆炸
  "claudeCode.temperature": 0.2, // 代码开发固定0.1~0.3，越低逻辑越严谨
  "claudeCode.topP": 0.8,
  "claudeCode.frequencyPenalty": 0.3, // 减少重复代码
  // 4. 效率快捷键开关
  "claudeCode.enableInlineEditShortcut": true,
  "claudeCode.autoInsertAtMention": true
}
```
如果之前用到了CC Switch接入中转，这里可以不用再配置API Key，只需要在使用Claude Code时后台挂CC Switch即可。然后配置文件相对应写局内一些模式参数：
```
{
  "claudeCode.preferredLocation": "panel",
  "editor.dropIntoEditor.preferences": [],
  "claudeCode.initialPermissionMode": "plan",
  "claudeCode.useTerminal": false,
  "claudeCode.showTokenUsageInStatusBar": true,
  "claudeCode.maxContextLength": 8000,
  "claudeCode.contextHistoryCount": 12,
  "claudeCode.temperature": 0.2,
  "claudeCode.topP": 0.8,
  "claudeCode.frequencyPenalty": 0.3,
  "claudeCode.enableInlineEditShortcut": true,
  "claudeCode.autoInsertAtMention": true
}
```
解释：
- `claudeCode.preferredLocation`设置对话窗口展示在底部面板
- `editor.dropIntoEditor.preferences`采用默认文件拖拽规则
- `claudeCode.initialPermissionMode` 变更代码前先展示修改方案确认
- `claudeCode.useTerminal` 禁止插件自动调用终端执行命令
- `claudeCode.showTokenUsageInStatusBar` 状态栏展示 token 消耗信息
- `claudeCode.maxContextLength` 限定单次对话上下文承载量
- `claudeCode.contextHistoryCount` 留存指定轮数对话历史用于参考
- `claudeCode.temperature` 降低生成随机性，输出代码更严谨稳定
- `claudeCode.topP `配合温度参数平衡代码生成灵活度
- `claudeCode.frequencyPenalty `减少代码语句与内容重复
- `claudeCode.enableInlineEditShortcut` 启用选中代码快速编辑快捷键
- `claudeCode.autoInsertAtMention `输入 @自动检索并插入项目文件引用
- 对于新手而言，这套配置比较友好，后面可能根据项目大小需要修改单次token是8000的限制，可以按上述操作修改或删减解除限制。
## 三、面板打开方式 + 全套核心快捷键
### 打开 Claude 面板 2 种方式
1.编辑器右上角Spark火花图标（最快）
2.底部状态栏点击Claude Code标识
### 快捷键
- `Esc`中断 AI 当前生成，停止输出
- `Shift`+`Tab`循环切换权限模式：`Plan`→`Auto`→`Ask`→`Edit auto`
- `Enter`发送提示词指令
- `Ctrl`+`G`打开外部编辑框写长提示词
- `Ctrl`+`R`检索历史对话命令
- `Esc` `Esc`回溯对话，撤销上一轮代码修改
- `Alt`+`K`插入`@文件#行号`精准引用代码片段
## 四、核心基础功能
### 1. @文件引用系统
AI 自动读取你指定文件 / 目录，精准理解项目上下文，不用复制粘贴代码。
- 单文件引用：输入`@main.py`，AI 读取整个文件
- 精准代码片段：选中代码 → `Alt`+`K`，自动生成`@main.py#25-48`限定行范围
- 文件夹批量引用：`@src/components`，读取整个目录所有代码
- 多文件组合：`@utils/db.ts` `@types/index.d.ts`同时传入多个依赖文件
- 示例指令：
```
@server/index.ts#10-35
这段接口存在数据库并发冲突，帮我加分布式锁，只修改选中函数，输出完整可运行代码，附带注释
```
### 2. 内联编辑 Inline Edit（单函数极速修改)
不用打开聊天面板，选中代码直接局部重写，打断思路最少。
操作：选中代码 → 右键 → 
`Claude Code: Inline Edit`，输入修改需求。
适用场景：重构函数、修复单处 bug、优化算法、补充注释。
示例需求：
```
将该同步函数改为async/await，增加异常捕获，返回统一格式Result
```
### 3. 三种权限模式（安全分级）
输入框底部切换，全局默认用`plan`，批量重构临时切换 `auto`：
- Ask before edits（编辑前询问）
每次要修改代码前，都会弹窗请求你的确认，不会直接改动文件，安全性最高，适合担心误改项目代码的场景。
- Edit automatically（自动编辑）
无需确认，直接修改选中代码或整个文件，操作效率最高，信任 AI 改码时使用。
- Plan mode（方案预览模式）
改动前先完整输出一套修改思路与代码变更方案，看完方案后手动确认才会应用修改，对应配置里的 plan 权限模式。
- Auto mode（自动适配模式）
插件自行判断任务类型，自动切换上面三种模式，简单小修改直接自动编辑，复杂重构则先出方案或询问。
- Effort (High)
不属于编辑权限模式，是 AI 思考强度档位，档位越高 AI 思考更细致、输出代码更完善，但消耗 token 更多、响应速度变慢。
- 代码差异预览
AI 修改文件后弹出左右分栏对比：左侧原代码，右侧 AI 修改；可单独接受某几行、全部接受、全部拒绝、发送指令让 AI 二次调整。
## 五、内置斜杠/命令大全（开发效率工具集）
聊天输入框输入/唤起命令菜单，覆盖调试、文档、模型切换、Token 统计：
- `/fix` 一键修复选中代码 bug
示例：
```
@api/login.ts /fix 接口500报错，定位空指针
```
- `/debug` 完整调试流程：定位问题→复现步骤→修复→单元测试
- `/doc` 自动生成 JSDoc / 注释、接口文档、README
- `/test` 为选中函数生成单元测试（Jest/Pytest/go test）
- `/model` 切换模型：opus4.6（复杂项目）/haiku（轻量快速）
- `/usage `查看当前会话 Token 消耗，控制成本
- `/clear` 清空当前对话上下文，消除历史干扰
- `/file` 快速追加文件到上下文（等价手动 @引用）
- `/improve` 代码优化：性能、可读性、规范、减少冗余
## 六、分场景标准化提示词模板（直接复制使用，降低 Token、提升准确率）
模板通用公式：`@精准代码 + 明确任务 + 约束规则 + 输出格式`
### 场景 1：从零生成完整功能模块
```
@src/types/user.ts @src/utils/request.ts
任务：创建用户注册接口模块，包含参数校验、密码加密、数据库写入
约束：
1. 使用Typescript，严格类型定义，禁止any
2. 捕获所有异常，统一返回{code,msg,data}格式
3. 密码使用bcrypt加密，增加重复邮箱校验
4. 只生成service+controller两个文件，不改动已有工具代码
输出：完整文件代码+简短使用说明
```
### 场景 2：Bug 调试（/debug 命令搭配
```
@main.py#60-90 /debug
现象：循环读取CSV时内存持续暴涨，程序10分钟崩溃
约束：
1. 定位内存泄漏点，解释泄漏原因
2. 给出2套优化方案：极简修改版、高性能迭代版
3. 补充一行性能测试代码验证优化效果
4. 不修改文件其他无关逻辑
```
### 场景 3：大规模代码重构（批量文件）
```
@src/views 整个目录重构需求
1. 将所有Class Vue组件改为Composition API + <script setup>
2. 统一导入路径别名@/，删除相对../../导入
3. 提取重复弹窗逻辑至hooks/modal.ts公共钩子
4. 先输出修改清单，确认后批量执行修改
```
### 场景 4：代码优化 + 规范整改
```
@utils/calc.js /improve
优化要求：
1. 简化嵌套if，使用卫语句提前return
2. 增加入参合法性校验，抛出明确错误信息
3. 删除冗余console.log，替换为日志工具logger
4. 补充边界值测试用例
```
### 场景 5：生成项目文档 / 注释
```
@整个项目src目录 /doc
生成完整README.md，包含：环境依赖、启动命令、目录结构、接口清单、部署步骤，简洁专业，无多余废话
```
##  七、进阶：项目级批量操作（大型项目效率核心）
### 1. 批量文件修改
通过`@文件夹`让 AI 一次性处理数十个文件，替代手动逐个修改：
示例指令：
```
@src/components
批量修改：所有组件onMounted生命周期增加路由离开销毁监听，清除定时器，防止内存泄漏；只修改vue文件，跳过测试文件
```
### 2. 跨文件依赖分析
适合接手陌生项目、排查循环依赖：
```
@src 整个项目
分析项目模块依赖，找出循环导入文件，输出依赖图谱，给出拆分重构方案
```
### 3. 新建整套文件结构
无需手动创建文件夹，AI 自动生成目录 + 代码：
```
新建后台权限模块，目录结构：
src/permission
├── types.ts 权限类型定义
├── service.ts 接口请求
├── store.ts pinia状态管理
└── index.ts 统一导出
使用Vue3+TS+Pinia，遵循项目现有代码风格
```
## 八、固化项目规范：CLAUDE.md（永久统一 AI 输出风格)
在项目根目录新建`CLAUDE.md`，AI 每次对话自动读取，不用每次重复写规范约束，节省 Token。
### CLAUDE.md 模板示例
```
# 本项目编码强制规范
## 技术栈
Vue3 + TypeScript + Vite + Pinia + Element Plus

## 代码规则
1. 禁止any，所有变量/函数必须显式定义类型
2. 接口返回统一格式：{ code: number; msg: string; data: T | null }
3. 异步函数全部async/await，拒绝.then嵌套
4. 工具函数统一放入src/utils，组件逻辑抽至hooks
5. 注释：复杂逻辑加单行注释，函数头部加JSDoc

## 输出要求
1. 修改代码只输出变更部分，不要完整复制全文件
2. 每次修改前说明改动目的、影响范围
3. 不自动删除原有业务逻辑，仅优化、新增功能
4. 生成测试用例使用vitest框架
```
创建后无需额外操作，任何对话 AI 都会自动遵循文档规则
## 九、性能优化、Token 节省、卡顿解决方案
###  1. 减少 Token 消耗（省钱 + 提速)
- 优先`@文件#行号`片段引用，不要传入完整大文件
- 无关文件不要 `@`引用，限定作用域（只传当前业务目录）
- 使用`CLAUDE.md`固化规范，提示词不用重复写约束
- 复杂任务分多轮拆解，不要一次性丢整个项目代码
- 温度 `temperature` 固定 0.2，减少 AI 冗余解释文字
### 2. 解决响应卡顿、超时
- 中转 API 替换低延迟节点，调整`ANTHROPIC_BASE_URL`
- `settings.json` 调低`maxContextLength`至 6000 以内
- 单次指令只处理一类任务，不要同时要求`重构` + `调试` + `写文档`
- 关闭 `Auto`自动修改，减少大量文件读写 IO
- 网络代理端口核对正确，关闭冲突 VPN 工具
### 3. 上下文混乱问题
对话逻辑跑偏、AI 忘记之前需求：输入`/clear`清空历史对话，重新发起指令。
## 十、日常高效工作流总结（极简版）
- 写代码：`Alt`+`K` 引用依赖文件 → 清晰结构化指令 → `Plan` 模式确认修改
- 改单函数：选中代码 → 右键 `Inline Edit`，快速局部调整
- 调试 bug：`@代码片段 /debug`
- 批量重构：`@目录 + 明确修改规则`，先看清单再执行
- 统一规范：项目根目录 `CLAUDE.md` 固化编码标准
- 收尾：`/doc`生成注释、接口文档、使用说明