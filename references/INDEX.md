# FireSpot References Index

FireSpot Agent Skill 的参考文档索引。

## 📚 文档导航

### 快速开始

如果你是第一次使用 FireSpot，建议按以下顺序阅读：

1. **[workflow.md](workflow.md)** - 工作流程规范（必读）
2. **[data_structures.md](data_structures.md)** - 数据结构定义（必读）
3. **[html_design_system.md](html_design_system.md)** - HTML 设计系统（推荐）

### 按功能分类

#### 🔄 工作流程相关

- **[workflow.md](workflow.md)**
  - 原7阶段工作流详细说明（保留参考）
  
- **[workflow_v7.2.md](workflow_v7.2.md)** 🆕
  - 新9阶段工作流详细说明
  - 阶段依赖关系
  - 文件路径规范
  - 退出条件

#### 📊 数据结构相关

- **[data_structures.md](data_structures.md)**
  - Stage 1-7 完整数据结构
  - JSON Schema 定义
  - 字段说明和示例

#### 🖼️ 图片资产相关

- **[image_asset_guide.md](image_asset_guide.md)**
  - 图片类型和角色
  - 图片来源策略
  - Prompt 模板
  - MCP 工具使用

#### ✅ 质量控制相关

- **[validation_rules.md](validation_rules.md)**
  - 合规校验规则
  - 评分系统
  - 最佳实践

#### 🔧 工具使用相关

- **[mcp_tools_guide.md](mcp_tools_guide.md)**
  - ZhipuArts MCP 使用
  - wechat-publisher MCP 使用
  - 完整工作流示例

#### 🎨 设计系统相关

- **[html_design_system.md](html_design_system.md)**
  - HTML 输出模板规范
  - 配色方案
  - 字体系统
  - 组件规范

## 📖 文档详细说明

### workflow_v7.2.md - 工作流程规范 🆕

**适用阶段**：所有阶段（v7.2版本）

**主要内容**：
- 阶段0：参数收集
- 阶段1：多平台热点研究
- 阶段2：内容分析
- 阶段3：内容规划 + 图片规划
- 阶段4：内容创作
- 阶段5：合规校验
- 阶段6：人工审核
- 阶段7：AI生图
- 阶段8：图文合并
- 阶段9：自动发布

**何时查阅**：
- 需要了解v7.2版本的工作流程
- 需要查看新的阶段依赖关系

### workflow.md - 工作流程规范（旧版）

**适用阶段**：所有阶段（v7.1版本，保留参考）

**主要内容**：
- 原7阶段工作流说明
- 阶段0-6详细流程
- 已被workflow_v7.2.md取代

**何时查阅**：
- 需要了解某个阶段的详细流程
- 需要查看阶段间的依赖关系
- 需要理解文件路径规范

### data_structures.md - 数据结构定义

**适用阶段**：所有阶段

**主要内容**：
- Stage 1: Research JSON Schema
- Stage 2: Analysis JSON Schema
- Stage 3: Outline JSON Schema
- Stage 4: Article JSON Schema
- Stage 5: Validation JSON Schema
- Stage 6: Review JSON Schema
- Stage 7: Publish JSON Schema

**何时查阅**：
- 需要创建或修改某个阶段的输出文件
- 需要理解字段含义和格式要求
- 需要验证数据结构的正确性

### image_asset_guide.md - 图片资产规划规范

**适用阶段**：阶段3、阶段7

**主要内容**：
- 图片类型（封面、正文、金句）
- 图片来源策略（user_provided > search > generate）
- Prompt 模板（封面、正文、金句）
- 图片锚点规范
- MCP 工具使用

**何时查阅**：
- 阶段3 规划图片资产时
- 阶段7 生成和上传图片时
- 需要编写图片生成 Prompt 时

### validation_rules.md - 合规校验规则

**适用阶段**：阶段4、阶段5

**主要内容**：
- 字数检查规则
- 禁用句式列表
- 图片锚点检查
- 段落结构检查
- 评分系统
- 最佳实践

**何时查阅**：
- 阶段4 写作时确保合规
- 阶段5 理解校验结果
- 需要调整校验规则时

### mcp_tools_guide.md - MCP 工具使用规范

**适用阶段**：阶段7

**主要内容**：
- ModelArts MCP 工具
- wechat-publisher MCP 工具
- 完整工作流示例
- 错误处理
- 配置检查

**何时查阅**：
- 阶段7 执行自动发布时
- 需要调试 MCP 工具调用时
- 需要理解 MCP 工具参数时

### html_design_system.md - HTML 设计系统规范

**适用阶段**：阶段6

**主要内容**：
- 设计原则（去AI化）
- 配色方案
- 字体系统
- HTML 结构规范
- 组件样式
- 响应式设计
- 变量替换规范

**何时查阅**：
- 阶段6 生成审核 HTML 时
- 需要自定义 HTML 样式时
- 需要理解设计规范时

## 🔍 按问题查找文档

### "我想知道某个阶段的详细流程"

→ 查看 **[workflow.md](workflow.md)**

### "我需要创建/修改某个阶段的输出文件"

→ 查看 **[data_structures.md](data_structures.md)**

### "我需要规划或生成图片"

→ 查看 **[image_asset_guide.md](image_asset_guide.md)**

### "我想知道文章是否合规"

→ 查看 **[validation_rules.md](validation_rules.md)**

### "我需要发布到微信公众号"

→ 查看 **[mcp_tools_guide.md](mcp_tools_guide.md)**

### "我需要生成或修改 HTML"

→ 查看 **[html_design_system.md](html_design_system.md)**

## 📝 文档维护

### 更新频率

- **workflow.md**：工作流变更时更新
- **data_structures.md**：数据结构变更时更新
- **image_asset_guide.md**：图片相关变更时更新
- **validation_rules.md**：校验规则变更时更新
- **mcp_tools_guide.md**：MCP 工具变更时更新
- **html_design_system.md**：HTML 设计变更时更新

### 版本控制

所有文档遵循 Semantic Versioning：
- **MAJOR**：结构性变更，不兼容旧版
- **MINOR**：新增功能，向后兼容
- **PATCH**：bug 修复，小改进

当前版本：v7.2

### 贡献指南

如需修改或新增文档：

1. 确保文档遵循 Markdown 规范
2. 使用清晰的标题层次
3. 提供具体的示例
4. 包含使用场景说明
5. 更新本索引（INDEX.md）

---

**最后更新**：2026-05-09
**文档版本**：v7.2
**维护者**：FireSpot Team
