# FireSpot 4.0 安装指南

## 前置要求

- DeerFlow 框架已安装并运行
- Python 3.12+
- LangGraph API

## 安装步骤

### 1. 安装 Agent 代码

将 `agent/` 目录复制到 DeerFlow 的 agents 目录：

```bash
cp -r agent/* /path/to/deerflow/backend/packages/harness/deerflow/agents/firespot/
```

### 2. 安装 Skills

将 `skills/firespot/` 目录复制到 DeerFlow 的 skills 目录：

```bash
cp -r skills/firespot/ /path/to/deerflow/skills/public/firespot/
```

### 3. 配置 Agent

创建 Agent 配置文件：

```bash
mkdir -p /path/to/deerflow/backend/.deer-flow/agents/firespot/
cp config/firespot.yaml /path/to/deerflow/backend/.deer-flow/agents/firespot/config.yaml
```

### 4. 注册 Graph

在 `backend/langgraph.json` 中添加：

```json
{
  "graphs": {
    "firespot_agent": "deerflow.agents:make_firespot_agent"
  }
}
```

### 5. 重启服务

```bash
# 停止服务
pkill -f "langgraph dev"

# 重启服务
cd /path/to/deerflow/backend
PYTHONPATH=. uv run langgraph dev --no-browser --allow-blocking
```

## 验证安装

访问 http://localhost:2026/workspace/agents/firespot

## 故障排除

详见 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
