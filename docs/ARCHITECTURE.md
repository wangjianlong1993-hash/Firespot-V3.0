# FireSpot 4.0 架构文档

## 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                   DeerFlow Framework                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │              FireSpot 4.0 Agent                 │   │
│  │                                                  │   │
│  │  ┌────────────────────────────────────────┐    │   │
│  │  │    Auto-Trigger Middleware             │    │   │
│  │  │    - Keyword Detection                 │    │   │
│  │  │    - Pattern Matching                  │    │   │
│  │  └────────────────────────────────────────┘    │   │
│  │                      ↓                           │   │
│  │  ┌────────────────────────────────────────┐    │   │
│  │  │    7-Stage Workflow Prompt            │    │   │
│  │  │    1. Research (热点研究)              │    │   │
│  │  │    2. Analysis (深度分析)              │    │   │
│  │  │    3. Planning (结构规划)              │    │   │
│  │  │    4. Writing (文章撰写)              │    │   │
│  │  │    5. Validation (质量验证)            │    │   │
│  │  │    6. Review (内容审校)                │    │   │
│  │  │    7. Publishing (自动发布)            │    │   │
│  │  └────────────────────────────────────────┘    │   │
│  │                      ↓                           │   │
│  │  ┌────────────────────────────────────────┐    │   │
│  │  │    Tool Integration                    │    │   │
│  │  │    - web_search (with retry)           │    │   │
│  │  │    - web_reader                        │    │   │
│  │  │    - publish_to_wechat                 │    │   │
│  │  └────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         MCP Servers                             │   │
│  │  - WeChat MCP (publishing)                      │   │
│  │  - Web Search MCP                               │   │
│  │  - Web Reader MCP                               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Auto-Trigger Middleware

**文件**: `agent/auto_trigger.py`

**功能**:
- 检测用户输入中的触发关键词
- 自动激活 FireSpot 工作流
- 传递触发上下文信息

**触发模式**:
```python
FIRESPOT_TRIGGERS = {
    "direct_writing": [r"帮我写", r"写一篇", r"创作"],
    "weixin_related": [r"公众号", r"推文"],
    "perspective_analysis": [r"从.*角度.*写"],
    "explicit_mention": [r"firespot", r"FireSpot"]
}
```

### 2. 7-Stage Workflow Prompt

**文件**: `agent/__init__.py`

**功能**:
- 定义强制性的 7 阶段工作流
- 每个阶段有明确的输出要求
- 系统提示词确保工作流执行

**流程控制**:
```python
FIRESPOT_SYSTEM_PROMPT = """
## ⚠️ CRITICAL: YOU MUST FOLLOW THE 7-STAGE WORKFLOW STRICTLY ⚠️

STAGE 1: 🔍 Research (Hot Topic Research) - MANDATORY
STAGE 2: 📊 Analysis (Deep Content Analysis) - MANDATORY
STAGE 3: 📋 Planning (Content Structure Planning) - MANDATORY
STAGE 4: ✍️ Writing (Article Generation) - MANDATORY
STAGE 5: ✅ Validation (Quality Validation) - MANDATORY
STAGE 6: 👀 Review (Content Review) - MANDATORY
STAGE 7: 🚀 Publishing (Auto-Publishing) - MANDATORY
"""
```

### 3. Search Retry Mechanism

**文件**: `agent/search_retry.py`

**功能**:
- 包装 web_search 工具
- 自动重试失败的搜索
- 指数退避策略
- 详细日志记录

**重试策略**:
```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((Exception,))
)
def firespot_search_with_retry(query: str, max_results: int = 5):
    # 搜索逻辑
```

### 4. Publishing Tools

**文件**: `agent/publishing_tools.py`

**功能**:
- 集成微信 MCP 服务器
- 发布文章到草稿箱
- 处理发布错误

**工具接口**:
```python
def publish_to_wechat_draft(
    title: str,
    content: str,
    summary: str = ""
) -> dict:
    # 发布逻辑
```

## 数据流

```
用户输入
   ↓
Auto-Trigger 检测
   ↓ (如果触发)
激活 FireSpot Agent
   ↓
执行 7 阶段工作流
   ↓
├─→ Search (web_search with retry)
├─→ Read (web_reader)
├─→ Plan (internal)
├─→ Write (LLM generation)
├─→ Validate (internal)
├─→ Review (LLM refinement)
└─→ Publish (WeChat MCP)
   ↓
输出结果 + 发布确认
```

## 配置

### Agent 配置

**文件**: `config/firespot.yaml`

```yaml
name: firespot
description: FireSpot 4.0 - AI-powered content research...
graph: firespot_agent
model: null
tool_groups: null
skills: null
```

### LangGraph 注册

**文件**: `backend/langgraph.json`

```json
{
  "graphs": {
    "firespot_agent": "deerflow.agents:make_firespot_agent"
  }
}
```

## 扩展性

### 添加新的触发模式

编辑 `agent/auto_trigger.py`:

```python
FIRESPOT_TRIGGERS = {
    "your_category": [r"pattern1", r"pattern2"]
}
```

### 添加新的工作流阶段

编辑 `agent/__init__.py` 中的 `FIRESPOT_SYSTEM_PROMPT`

### 集成新的发布平台

1. 在 `agent/publishing_tools.py` 添加新工具
2. 更新工作流第 7 阶段

## 性能优化

1. **搜索重试**: 减少网络故障影响
2. **并行搜索**: 可配置多个搜索源
3. **缓存机制**: 避免重复搜索
4. **批处理发布**: 支持批量发布

## 安全性

1. **输入验证**: 检测恶意输入
2. **发布审核**: 草稿箱需人工审核
3. **错误处理**: 优雅降级
4. **日志记录**: 完整操作审计

## 监控

- 每个阶段的执行时间
- 搜索成功率
- 发布成功率
- 错误日志

详见 [MONITORING.md](docs/MONITORING.md)
