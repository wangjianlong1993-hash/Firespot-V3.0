# FireSpot V4.0 设计方案

## 📋 方案概述

**设计目标**：通过 Agent + Skill 协作，确保 FireSpot 执行 7 阶段工作流时的确定性和完整性

**核心思路**：
- **FireSpot Agent** = 项目经理（负责流程控制、质量监督、错误恢复）
- **FireSpot Skill** = 执行专家（负责具体内容创作、MCP 工具调用）
- **状态机** = 流程保障（确保每个阶段按顺序完成，不跳步、不跑偏）

---

## 🏗️ 整体架构

```
┌─────────────────────────────────────────────────────────┐
│              FireSpot Agent (项目经理)                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  状态机 (State Machine) - 流程控制器            │  │
│  │  - 阶段 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7        │  │
│  │  - 每个阶段有明确的进入/退出条件                │  │
│  │  - 阶段间有状态检查点 (Checkpoints)            │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↓                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  编排器 (Orchestrator) - 任务分发               │  │
│  │  - 将阶段拆解为具体任务                        │  │
│  │  - 决定是自己执行还是委托 Skill                 │  │
│  │  - 监督执行质量和进度                          │  │
│  └───────────────────────────────────────────────────┘  │
│                         ↓                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │  验证器 (Validator) - 质量把关                  │  │
│  │  - 检查每个阶段的输出完整性                     │  │
│  │  - 验证数据文件存在且格式正确                   │  │
│  │  - 决定是否进入下一阶段或重试                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         ↓ 调用
┌─────────────────────────────────────────────────────────┐
│           FireSpot Skill (执行专家)                     │
│  - 执行具体的内容创作任务                            │
│  - 调用 MCP 工具（搜索、图片生成、发布）             │
│  - 按照规范输出结果                                  │
└─────────────────────────────────────────────────────────┘
                         ↓ 使用
┌─────────────────────────────────────────────────────────┐
│              MCP 工具 & 基础工具                        │
│  - web_search, web_fetch                             │
│  - read_file, write_file                             │
│  - task (子任务代理)                                  │
│  - mcp_wechat_* (微信发布)                            │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 核心设计原则

### 1. 职责分离原则

| 组件 | 职责 | 不做什么 |
|------|------|----------|
| **FireSpot Agent** | 流程控制、质量监督、错误恢复 | 不直接创作内容 |
| **FireSpot Skill** | 内容创作、工具调用、规范输出 | 不控制流程 |
| **MCP 工具** | 执行具体操作 | 不知道业务逻辑 |

### 2. 状态机保障原则

```
每个阶段必须：
1. 明确的进入条件（前置阶段完成）
2. 明确的执行动作（调用 Skill 或自己执行）
3. 明确的验证标准（检查输出文件）
4. 明确的退出条件（验证通过 → 下一阶段，不通过 → 重试）
```

### 3. 数据持久化原则

```
每个阶段必须：
1. 读取前一阶段的输出文件
2. 执行本阶段的处理逻辑
3. 保存本阶段的输出文件
4. 更新状态文件 (firespot_state.json)
```

---

## 📐 详细设计

### 阶段 0：参数收集（Agent 自己执行）

```python
# 状态：initial
# 动作：解析用户输入，收集参数
# 输出：/mnt/user-data/workspace/stage0_params.json
# 验证：参数完整性检查
# 下一状态：stage1_research

状态转换：
initial → (解析成功) → stage1_research
        → (参数不足) → initial (询问用户)
```

**关键点**：
- Agent 直接解析用户输入
- 如果信息不足，生成参数收集模板并等待用户回复
- 参数完整后保存到 `stage0_params.json`

### 阶段 1：多平台热点研究（Agent 委托 Skill）

```python
# 状态：stage1_research
# 动作：调用 FireSpot Skill 的研究能力
# 输入：stage0_params.json
# 输出：/mnt/user-data/workspace/stage1_research.json
# 验证：文件存在，包含 platforms 字段
# 下一状态：stage2_analysis

Agent 操作：
1. 读取 stage0_params.json
2. 调用 task() 工具，传入 Skill 的阶段1提示词
3. 等待子任务完成
4. 验证输出文件
5. 更新状态
```

**关键点**：
- Agent 使用 `task()` 工具启动子任务
- 子任务加载 FireSpot Skill
- Skill 执行具体的多平台搜索
- Agent 验证结果完整性

### 阶段 2：内容分析（Agent 自己执行）

```python
# 状态：stage2_analysis
# 动作：Agent 自己读取研究文件并分析
# 输入：stage1_research.json
# 输出：/mnt/user-data/workspace/stage2_analysis.json
# 验证：JSON 包含 core_thesis, supporting_points
# 下一状态：stage3_planning

Agent 操作：
1. read_file("/mnt/user-data/workspace/stage1_research.json")
2. 使用 LLM 进行深度分析（应用分析框架）
3. write_file("/mnt/user-data/workspace/stage2_analysis.json")
4. 验证输出结构
```

**关键点**：
- Agent 直接使用 LLM 能力分析
- 不委托给 Skill（这是 Agent 的核心价值：高级推理）
- 生成结构化的分析报告

### 阶段 3：内容规划+图片规划（Agent 自己执行）

```python
# 状态：stage3_planning
# 动作：基于分析结果生成文章框架和图片规划
# 输入：stage2_analysis.json
# 输出：/mnt/user-data/workspace/stage3_outline.json
# 验证：包含 title_options, sections, publishing_plan
# 下一状态：stage4_writing

Agent 操作：
1. 读取分析结果
2. 使用 LLM 生成详细大纲
3. 规划图片资产（封面、配图、金句图）
4. 保存框架文件
```

**关键点**：
- Agent 结合分析结果生成结构化大纲
- 图片规划要符合微信发布规范
- 确保 `asset_id` 的唯一性

### 阶段 4：内容创作（Agent 委托 Skill）

```python
# 状态：stage4_writing
# 动作：调用 Skill 撰写文章
# 输入：stage0_params.json, stage1_research.json, stage2_analysis.json, stage3_outline.json
# 输出：/mnt/user-data/outputs/stage4_draft.md, /mnt/user-data/workspace/stage4_article.json
# 验证：字数 800-1500，包含图片锚点
# 下一状态：stage5_validation

Agent 操作：
1. 读取所有前置文件
2. 调用 task() 工具，传入 Skill 的阶段4提示词
3. 等待子任务完成
4. 验证输出（字数、锚点、格式）
```

**关键点**：
- 委托给 Skill 执行具体写作
- Agent 监督质量，验证结果
- 不合格则要求 Skill 重写

### 阶段 5：合规校验（Agent 自己执行）

```python
# 状态：stage5_validation
# 动作：执行自动化合规检查
# 输入：stage4_draft.md, stage4_article.json
# 输出：/mnt/user-data/workspace/stage5_validation.json
# 验证：评分 >= 80 且无 error 级别问题
# 下一状态：stage6_review (通过) / stage4_writing (不通过)

Agent 操作：
1. 使用 bash() 工具执行 Python 校验脚本
2. 解析校验结果
3. 决定下一阶段
4. 如果不通过，回到阶段4并附上修改意见
```

**关键点**：
- Agent 执行自动化质量检查
- 不依赖 Skill 的自我评估
- 客观评分机制

### 阶段 6：人工审核（Agent 自己执行）

```python
# 状态：stage6_review
# 动作：生成审核 HTML，展示给用户，等待确认
# 输入：stage4_draft.md, stage4_article.json, stage5_validation.json
# 输出：/mnt/user-data/outputs/stage6_review.html
# 验证：用户明确回复 "approve"
# 下一状态：stage7_publish (approve) / stage4_writing (revise) / end (cancel)

Agent 操作：
1. 读取草稿和校验结果
2. 生成审核 HTML
3. 使用 present_files() 展示给用户
4. 等待用户回复（approve / revise / detail / cancel）
5. 根据回复决定下一步
```

**关键点**：
- Agent 作为界面和用户交互
- 明确等待用户确认
- 支持修订、查看详情、取消操作

### 阶段 7：自动发布（Agent 委托 MCP）

```python
# 状态：stage7_publish
# 动作：调用微信 MCP 发布草稿
# 输入：stage6_review.html, stage4_article.json, stage3_outline.json
# 输出：/mnt/user-data/workspace/stage7_publish_assets.json
# 验证：draft_result 包含 media_id
# 下一状态：completed

Agent 操作：
1. 读取审核后的文件
2. 调用 mcp.call_tool("wechat-publisher", "mcp_wechat_prepare_image", ...)
3. 逐张准备和上传图片
4. 调用 mcp.call_tool("wechat-publisher", "mcp_wechat_create_draft", ...)
5. 保存发布摘要
6. 通知用户登录微信后台最终确认
```

**关键点**：
- Agent 编排整个发布流程
- 逐步调用 MCP 工具
- 处理可能的错误（图片上传失败、草稿创建失败）

---

## 🔧 Agent 配置文件结构

### 文件位置
```
/Users/garywong/deer-flow/backend/agents/firespot/config.yaml
```

### 配置内容
```yaml
# FireSpot Agent 配置
agent_id: firespot
agent_name: FireSpot Content Creator
display_name: FireSpot 内容创作专家
description: |
  专业的微信公众号内容创作 Agent。
  按照 7 阶段标准化工作流完成从热点研究到自动发布的全流程。

# 状态机配置
state_machine:
  initial_state: initial

  states:
    initial:
      entry_actions:
        - parse_user_input
        - check_parameters
      transitions:
        - target: stage1_research
          condition: parameters_complete
        - target: initial
          condition: parameters_incomplete
          action: ask_for_parameters

    stage1_research:
      entry_actions:
        - delegate_to_skill
          skill: firespot
          stage: 1
          input_files: [stage0_params.json]
          output_files: [stage1_research.json]
      exit_actions:
        - validate_research_data
      transitions:
        - target: stage2_analysis
          condition: validation_passed

    stage2_analysis:
      entry_actions:
        - analyze_research_data
      exit_actions:
        - validate_analysis
      transitions:
        - target: stage3_planning
          condition: validation_passed

    stage3_planning:
      entry_actions:
        - generate_outline
        - plan_image_assets
      exit_actions:
        - validate_outline
      transitions:
        - target: stage4_writing
          condition: validation_passed

    stage4_writing:
      entry_actions:
        - delegate_to_skill
          skill: firespot
          stage: 4
          input_files:
            - stage0_params.json
            - stage1_research.json
            - stage2_analysis.json
            - stage3_outline.json
          output_files:
            - stage4_draft.md
            - stage4_article.json
      exit_actions:
        - validate_article
      transitions:
        - target: stage5_validation
          condition: validation_passed
        - target: stage4_writing
          condition: validation_failed
          action: request_revision

    stage5_validation:
      entry_actions:
        - run_compliance_check
      exit_actions:
        - evaluate_score
      transitions:
        - target: stage6_review
          condition: score_above_80
        - target: stage4_writing
          condition: score_below_80
          action: provide_improvement_feedback

    stage6_review:
      entry_actions:
        - generate_review_html
        - present_to_user
        - await_user_confirmation
      transitions:
        - target: stage7_publish
          condition: user_approved
        - target: stage4_writing
          condition: user_requested_revision
        - target: completed
          condition: user_cancelled

    stage7_publish:
      entry_actions:
        - prepare_images
        - upload_to_wechat
        - create_draft
      transitions:
        - target: completed
          condition: publish_success

    completed:
      entry_actions:
        - generate_summary
        - notify_user

# 工作空间配置
workspace:
  base_path: /mnt/user-data/workspace
  outputs_path: /mnt/user-data/outputs

# 中间文件映射
artifacts:
  stage0_params:
    path: stage0_params.json
    required: true

  stage1_research:
    path: stage1_research.json
    required: true
    schema:
      platforms: object
      cross_platform_insights: object

  stage2_analysis:
    path: stage2_analysis.json
    required: true
    schema:
      core_thesis: string
      supporting_points: array

  stage3_outline:
    path: stage3_outline.json
    required: true
    schema:
      title_options: array
      sections: array
      publishing_plan:
        cover: object
        images: array

  stage4_draft:
    path: ../outputs/stage4_draft.md
    required: true
    validation:
      min_word_count: 800
      max_word_count: 2000

  stage4_article:
    path: stage4_article.json
    required: true
    schema:
      title: string
      markdown_body: string
      images: array

  stage5_validation:
    path: stage5_validation.json
    required: true
    schema:
      score: number
      status: string
      issues: array

  stage6_review:
    path: ../outputs/stage6_review.html
    required: true

  stage7_publish:
    path: stage7_publish_assets.json
    required: true

# 质量阈值配置
quality_thresholds:
  min_word_count: 800
  max_word_count: 2000
  min_validation_score: 80
  required_image_anchors:
    - cover_01
  min_inline_images: 2

# MCP 工具依赖
mcp_dependencies:
  - wechat-publisher

# Skill 依赖
skill_dependencies:
  - firespot

# 超时配置
timeouts:
  stage1_research: 600  # 10分钟
  stage2_analysis: 300   # 5分钟
  stage3_planning: 300   # 5分钟
  stage4_writing: 900   # 15分钟
  stage5_validation: 60  # 1分钟
  stage6_review: 60     # 1分钟（生成）+ 无限等待用户确认
  stage7_publish: 600    # 10分钟
```

---

## 🤖 Agent 实现示例

### 核心状态机逻辑

```python
# backend/agents/firespot/graph.py

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class FireSpotState(TypedDict):
    user_input: str
    current_stage: str
    stage_outputs: dict
    validation_results: dict
    user_confirmation: str | None
    error_message: str | None
    should_retry: bool
    retry_count: int

def create_firespot_graph():
    graph = StateGraph(FireSpotState)

    # 初始状态
    graph.add_node("initial", initialize_stage)
    graph.add_node("stage1_research", execute_stage1)
    graph.add_node("stage2_analysis", execute_stage2)
    graph.add_node("stage3_planning", execute_stage3)
    graph.add_node("stage4_writing", execute_stage4)
    graph.add_node("stage5_validation", execute_stage5)
    graph.add_node("stage6_review", execute_stage6)
    graph.add_node("stage7_publish", execute_stage7)
    graph.add_node("completed", finalize)

    # 状态转换
    graph.add_edge("initial", "stage1_research")
    graph.add_edge("stage1_research", "stage2_analysis")
    graph.add_edge("stage2_analysis", "stage3_planning")
    graph.add_edge("stage3_planning", "stage4_writing")
    graph.add_edge("stage4_writing", "stage5_validation")

    # 条件转换：阶段5 → 阶段6 或 回到阶段4
    graph.add_conditional_edges(
        "stage5_validation",
        should_proceed_to_review,
        {
            "proceed": "stage6_review",
            "retry": "stage4_writing"
        }
    )

    # 条件转换：阶段6 → 阶段7 或 回到阶段4 或 结束
    graph.add_conditional_edges(
        "stage6_review",
        handle_user_decision,
        {
            "approve": "stage7_publish",
            "revise": "stage4_writing",
            "cancel": "completed"
        }
    )

    graph.add_edge("stage7_publish", "completed")
    graph.add_edge("completed", END)

    return graph.compile()

def should_proceed_to_review(state: FireSpotState) -> Literal["proceed", "retry"]:
    score = state["validation_results"].get("score", 0)
    errors = state["validation_results"].get("errors", [])

    if score >= 80 and len(errors) == 0:
        return "proceed"
    else:
        return "retry"

def handle_user_decision(state: FireSpotState) -> Literal["approve", "revise", "cancel"]:
    confirmation = state.get("user_confirmation", "").lower().strip()

    if confirmation == "approve":
        return "approve"
    elif confirmation == "cancel":
        return "cancel"
    else:
        return "revise"
```

### 阶段执行示例

```python
# backend/agents/firespot/stages.py

async def execute_stage1(state: FireSpotState, config):
    """执行阶段1：多平台热点研究"""

    # 1. 读取参数
    params = read_file("/mnt/user-data/workspace/stage0_params.json")

    # 2. 委托给 Skill 执行
    research_result = await task(
        description=f"""
你是 FireSpot 技能的执行者。

请执行 FireSpot 工作流的阶段1：多平台热点研究

**参数：**
{params}

**要求：**
1. 按照 FireSpot Skill v3.0 的阶段1规范执行
2. 使用可用的搜索工具（web_search）
3. 输出到 /mnt/user-data/workspace/stage1_research.json
4. 确保覆盖至少5个平台

完成后返回：[FIRESPOT | 阶段1完成] 的输出
"""
    )

    # 3. 验证输出
    validation = await validate_stage1_output()

    # 4. 更新状态
    state["stage_outputs"]["stage1"] = research_result
    state["current_stage"] = "stage2_analysis"

    return state

async def validate_stage1_output():
    """验证阶段1输出"""
    import json
    from pathlib import Path

    output_file = Path("/mnt/user-data/workspace/stage1_research.json")

    if not output_file.exists():
        raise ValueError("阶段1输出文件不存在")

    data = json.loads(output_file.read_text())

    # 验证必需字段
    required_fields = ["research_date", "topic", "platforms", "cross_platform_insights"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"缺少必需字段: {field}")

    # 验证平台数据
    platforms = data.get("platforms", {})
    if len(platforms) < 3:
        raise ValueError(f"研究平台不足，至少需要3个，当前: {len(platforms)}")

    return {"valid": True, "platforms": len(platforms)}
```

---

## 🎯 Agent-Skill 协作机制

### 协作模式 1：委托模式（阶段 1、4）

```
Agent (项目经理)                Skill (执行专家)
     |                                |
     |--- 1. 准备参数 -------------->|
     |                                |
     |--- 2. 启动任务 -------------->|
     |    task(description)          |
     |                                |
     |                                |-- 3. 执行搜索/写作
     |                                |-- 4. 调用工具
     |                                |
     |<-- 5. 返回结果 ----------------|
     |                                |
     |--- 6. 验证质量
     |--- 7. 更新状态
     |--- 8. 进入下一阶段
```

### 协作模式 2：自主执行模式（阶段 2、3、5、6、7）

```
Agent (项目经理)
     |
     |--- 1. 读取前置文件
     |--- 2. 应用业务逻辑
     |--- 3. 调用 LLM
     |--- 4. 调用工具（bash, read_file, write_file）
     |--- 5. 验证输出
     |--- 6. 更新状态
     |--- 7. 进入下一阶段
```

### 协作模式 3：编排模式（阶段 7）

```
Agent (编排者)                MCP Tools (执行者)
     |                                |
     |--- 1. 读取资产规划 -------->|
     |                                |
     |--- 2. 逐张准备图片 --------->|
     |    mcp.call_tool(...)          |
     |                                |
     |                                |-- 生成图片
     |                                |-- 上传图片
     |                                |
     |<-- 3. 返回 media_id ----------|
     |                                |
     |--- 4. 替换图片锚点
     |--- 5. 创建草稿 -------------->|
     |    mcp.call_tool(...)          |
     |                                |
     |                                |-- 创建草稿
     |                                |
     |<-- 6. 返回草稿 ID ------------|
     |                                |
     |--- 7. 保存发布摘要
     |--- 8. 通知用户
```

---

## 🛡️ 确定性保障机制

### 1. 状态检查点

每个阶段结束时检查：
```python
checkpoints = {
    "stage0": ["params_complete"],
    "stage1": ["research_file_exists", "min_3_platforms"],
    "stage2": ["thesis_defined", "3_supporting_points"],
    "stage3": ["outline_complete", "image_plan_complete"],
    "stage4": ["word_count_ok", "anchors_placed"],
    "stage5": ["score_80_plus", "no_errors"],
    "stage6": ["html_generated", "user_confirmed"],
    "stage7": ["draft_created", "media_id_obtained"]
}
```

### 2. 错误恢复机制

```python
error_recovery = {
    "stage1": {
        "max_retries": 2,
        "fallback": "use_internal_search_only",
        "on_failure": "report_error_to_user"
    },
    "stage4": {
        "max_retries": 2,
        "fallback": "simplify_requirements",
        "on_failure": "request_revision"
    },
    "stage5": {
        "max_retries": 1,
        "fallback": "publish_with_warnings",
        "on_failure": "ask_user_override"
    }
}
```

### 3. 数据完整性验证

每个阶段结束时验证：
```python
async def validate_stage_artifacts(stage_id: str):
    """验证阶段产物的完整性"""

    artifacts = STAGE_ARTIFACTS[stage_id]

    for artifact in artifacts:
        # 1. 文件存在性检查
        if not artifact["path"].exists():
            raise FileNotFoundError(f"缺少文件: {artifact['path']}")

        # 2. 格式验证
        if artifact.get("schema"):
            validate_schema(artifact["path"], artifact["schema"])

        # 3. 内容验证
        if artifact.get("validation"):
            validate_content(artifact["path"], artifact["validation"])

    return True
```

---

## 📂 文件组织结构

```
backend/agents/firespot/
├── __init__.py                 # Agent 导出
├── config.yaml                 # Agent 配置（如上所示）
├── graph.py                    # 状态机定义
├── stages/
│   ├── __init__.py
│   ├── stage0_params.py        # 阶段0：参数收集
│   ├── stage1_research.py      # 阶段1：热点研究
│   ├── stage2_analysis.py      # 阶段2：内容分析
│   ├── stage3_planning.py      # 阶段3：内容规划
│   ├── stage4_writing.py       # 阶段4：内容创作
│   ├── stage5_validation.py    # 阶段5：合规校验
│   ├── stage6_review.py        # 阶段6：人工审核
│   └── stage7_publish.py       # 阶段7：自动发布
├── validators/
│   ├── __init__.py
│   ├── artifacts.py            # 产物验证
│   ├── quality.py              # 质量验证
│   └── consistency.py          # 一致性验证
├── utils/
│   ├── __init__.py
│   ├── file_ops.py             # 文件操作工具
│   ├── llm_calls.py            # LLM 调用工具
│   └── mcp_client.py            # MCP 客户端封装
└── README.md                    # Agent 文档
```

---

## 🚀 实施计划

### Phase 1: 核心框架（第1-2周）

1. ✅ 创建 Agent 目录结构
2. ✅ 实现状态机基础框架
3. ✅ 实现阶段0（参数收集）
4. ✅ 实现阶段1（热点研究）
5. ✅ 测试 Agent-Skill 委托

### Phase 2: 完整流程（第3-4周）

6. ✅ 实现阶段2-3（分析+规划）
7. ✅ 实现阶段4（写作）
8. ✅ 实现阶段5（校验）
9. ✅ 实现阶段6（审核）
10. ✅ 实现阶段7（发布）

### Phase 3: 质量保障（第5周）

11. ✅ 实现验证器
12. ✅ 实现错误恢复
13. ✅ 完善日志和监控
14. ✅ 端到端测试

### Phase 4: 优化提升（第6周）

15. ✅ 性能优化
16. ✅ 用户体验优化
17. ✅ 文档完善
18. ✅ 生产环境部署

---

## 💡 使用示例

### 示例 1：完整流程

```
用户：使用 FireSpot 写一篇关于 AI 伦理的公众号文章

Agent 响应：
[FIRESPOT | Agent 启动]
→ 阶段0：参数收集
  ✅ 选题：AI 伦理
  ✅ 角度：伦理学分析
  ✅ 字数：1200字
  ✅ 图片需求：是

→ 阶段1：多平台热点研究
  🔄 调用 FireSpot Skill 执行研究
  ✅ 覆盖平台：7个
  ✅ 数据源：23个

→ 阶段2：内容分析
  ✅ 核心主张：AI 伦理是人类价值体系的延伸
  ✅ 差异化角度：从道德哲学角度而非技术角度

→ 阶段3：内容规划
  ✅ 文章框架：3个核心段落
  ✅ 图片规划：封面+3张配图+1张金句图

→ 阶段4：内容创作
  🔄 调用 FireSpot Skill 撰写文章
  ✅ 草稿：stage4_draft.md
  ✅ 元数据：stage4_article.json

→ 阶段5：合规校验
  ✅ 综合评分：92/100
  ✅ 字数：1258字
  ✅ 问题数：0

→ 阶段6：人工审核
  ✅ 审核 HTML：stage6_review.html
  ⏸️ 等待用户确认...

用户：approve

→ 阶段7：自动发布
  ✅ 准备图片：5张
  ✅ 上传图片：5/5
  ✅ 创建草稿：media_id=xxx
  ✅ 发布摘要：stage7_publish_assets.json

[FIRESPOT | 完成] 草稿已创建，请登录微信后台最终确认
```

---

## 📊 与 V3.0 的对比

| 特性 | V3.0 (Skill Only) | V4.0 (Agent + Skill) |
|------|-------------------|----------------------|
| 流程控制 | Skill 内部控制 | Agent 外部控制 |
| 确定性 | 依赖 LLM 遵守指令 | 状态机强制执行 |
| 错误恢复 | Skill 自行处理 | Agent 监督恢复 |
| 质量保证 | Skill 自我评估 | Agent 客观验证 |
| 可观测性 | 日志分散 | 统一状态追踪 |
| 可扩展性 | 修改 Skill 文件 | 修改配置/代码 |

---

## ⚠️ 风险与缓解

### 风险 1：复杂度增加

**缓解措施**：
- 清晰的职责分离
- 完善的文档和注释
- 逐步实施，每个阶段独立测试

### 风险 2：性能问题

**缓解措施**：
- 合理的超时配置
- 异步执行不阻塞
- 缓存中间结果

### 风险 3：Skill 与 Agent 冲突

**缓解措施**：
- 明确的接口定义
- Agent 拥有最终决策权
- Skill 作为执行者而非决策者

---

## 🎯 预期效果

实施 FireSpot V4.0 后：

1. ✅ **流程确定性**：7 个阶段严格按照顺序执行，不跳步
2. ✅ **质量保障**：每个阶段都有客观验证，不合格必重做
3. ✅ **可观测性**：实时状态追踪，清晰的进度展示
4. ✅ **可维护性**：清晰的代码结构，易于修改和扩展
5. ✅ **用户体验**：自动化程度高，人工干预点明确

---

## 📞 下一步行动

**立即可执行**：

1. 创建 Agent 目录结构
2. 实现基础状态机框架
3. 实现阶段0（参数收集）
4. 测试 Agent 激活机制

**需要您的确认**：

- [ ] 是否采用此设计方案？
- [ ] 是否需要调整某些部分？
- [ ] 是否立即开始实施？
- [ ] 优先级：完整实现 vs 核心功能先上线？
