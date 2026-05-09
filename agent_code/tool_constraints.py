"""
FireSpot Tool Constraint Enforcement
===================================
强制执行 FireSpot 必须使用的工具约束

Author: FireSpot Team
Version: 4.2.0 (Tool Constraint Enforcement)
"""

import logging
from typing import Dict, Any, List, Optional
from langchain.agents.middleware import AgentMiddleware
from langgraph.runtime import Runtime
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage

from ..thread_state import ThreadState
from .config import (
    FIRESPOT_STAGES,
    FIRESPOT_IMAGE_CONFIG,
    FIRESPOT_WECHAT_CONFIG,
    FIRESPOT_MCP_TOOLS
)

logger = logging.getLogger(__name__)

# ============================================================================
# 强制工具约束配置
# ============================================================================

MANDATORY_TOOLS = {
    "stage3_planning": {
        "required_tools": [],
        "description": "内容规划阶段 - 准备图片资产规划"
    },
    "stage4_writing": {
        "required_tools": [],
        "description": "内容创作阶段 - 插入图片锚点"
    },
    "stage5_validation": {
        "required_tools": [],
        "description": "质量校验阶段 - 验证图片锚点完整性"
    },
    "stage7_publish": {
        "required_tools": [
            "mcp_modelarts_generate_image",
            "mcp_wechat_prepare_image",
            "mcp_wechat_create_draft"
        ],
        "description": "发布阶段 - 必须使用 ModelArts 和 WeChat Publisher",
        "enforcement": "strict"
    }
}

# 图片生成强制使用 ModelArts
IMAGE_GENERATION_CONSTRAINTS = {
    "allowed_tools": ["mcp_modelarts_generate_image"],
    "forbidden_alternatives": ["手动上传", "网络搜索", "其他AI服务"],
    "enforcement_message": "⚠️ FireSpot 要求必须使用 ModelArts MCP 服务生成图片"
}

# 微信发布强制使用 Publisher
WECHAT_PUBLISHING_CONSTRAINTS = {
    "allowed_tools": ["mcp_wechat_prepare_image", "mcp_wechat_create_draft"],
    "forbidden_alternatives": ["手动上传", "其他发布方式"],
    "enforcement_message": "⚠️ FireSpot 要求必须使用 wechat-publisher MCP 服务发布"
}


class FireSpotToolConstraintMiddleware(AgentMiddleware[ThreadState]):
    """
    FireSpot 工具约束强制执行中间件

    确保 FireSpot 工作流中必须使用指定的 MCP 工具：
    - 图片生成必须使用 ModelArts
    - 微信发布必须使用 wechat-publisher
    """

    def __init__(self):
        super().__init__()
        self.constraint_violations = []

    def before_model(self, state: ThreadState, runtime: Runtime) -> Dict[str, Any]:
        """
        在模型调用前检查和约束工具使用

        对于 stage7_publish，强制注入必须使用特定工具的指导
        """
        messages = state.get("messages", [])
        if not messages:
            return {}

        # 检查当前是否处于发布阶段
        current_stage = self._detect_current_stage(messages)

        if current_stage == "stage7_publish":
            # 注入强制工具使用约束
            return self._inject_tool_constraints(state)

        return {}

    def after_model(self, state: ThreadState, runtime: Runtime) -> Dict[str, Any]:
        """
        在模型调用后验证工具使用是否遵守约束

        检查是否使用了强制要求的工具
        """
        messages = state.get("messages", [])
        if not messages:
            return {}

        current_stage = self._detect_current_stage(messages)

        if current_stage == "stage7_publish":
            # 验证是否正确使用了必需工具
            violations = self._check_tool_constraints(state, messages)

            if violations:
                self.constraint_violations.extend(violations)
                # 可以选择返回错误消息或警告
                logger.warning(
                    f"⚠️ FireSpot 工具约束违规: {violations}",
                    extra={
                        "firespot_event": "tool_constraint_violation",
                        "violations": violations,
                        "stage": current_stage
                    }
                )

        return {}

    def _detect_current_stage(self, messages: List[BaseMessage]) -> Optional[str]:
        """检测当前工作流阶段"""
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                content = msg.content
                if isinstance(content, str):
                    # 检查阶段标识
                    if "阶段 7" in content or "stage7" in content.lower():
                        return "stage7_publish"
                    elif "阶段 6" in content or "stage6" in content.lower():
                        return "stage6_review"
                    # 可以添加更多阶段检测
        return None

    def _inject_tool_constraints(self, state: ThreadState) -> Dict[str, Any]:
        """在发布阶段注入强制工具使用约束"""
        constraint_guidance = """

═══════════════════════════════════════════════════════════
  🔧 FireSpot 工具使用强制约束
═══════════════════════════════════════════════════════════

【重要】本阶段（阶段7：自动发布）必须使用以下 MCP 工具：

🎨 图片生成：
  • 必须使用：mcp_modelarts_generate_image
  • 禁止使用：手动上传图片、网络搜索图片或其他AI服务
  • 原因：保证图片质量和风格一致性

📱 微信发布：
  • 必须使用：mcp_wechat_prepare_image（准备图片素材）
  • 必须使用：mcp_wechat_create_draft（创建草稿）
  • 禁止使用：手动复制粘贴或其他发布方式
  • 原因：确保发布流程完整可追踪

【验证】系统将检查工具调用是否符合上述要求。

═══════════════════════════════════════════════════════════
"""

        # 在最后一个消息后添加约束指导
        messages = state.get("messages", []).copy()
        if messages:
            # 在系统消息中添加约束指导
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                original_content = last_message.content
                if isinstance(original_content, str):
                    enhanced_content = original_content + constraint_guidance
                    messages[-1] = AIMessage(content=enhanced_content)
                    return {"messages": messages}

        return {}

    def _check_tool_constraints(self, state: ThreadState, messages: List[BaseMessage]) -> List[str]:
        """检查工具调用是否遵守约束"""
        violations = []

        # 检查阶段7是否使用了必需的工具
        current_stage = self._detect_current_stage(messages)

        if current_stage == "stage7_publish":
            required_tools = MANDATORY_TOOLS["stage7_publish"]["required_tools"]
            used_tools = self._get_used_tools(messages)

            # 检查是否所有必需工具都被使用
            for required_tool in required_tools:
                if required_tool not in used_tools:
                    violations.append(f"未使用必需工具: {required_tool}")

            # 检查是否使用了禁止的工具（如果可以检测到的话）
            # 这里可以添加更多的检查逻辑

        return violations

    def _get_used_tools(self, messages: List[BaseMessage]) -> List[str]:
        """提取已使用的工具列表"""
        used_tools = []

        for msg in messages:
            if isinstance(msg, AIMessage):
                # 检查 tool_calls
                if hasattr(msg, 'content') and isinstance(msg.content, list):
                    for item in msg.content:
                        if isinstance(item, dict) and 'tool_use' in item:
                            tool_name = item['tool_use'].get('name', '')
                            if tool_name:
                                used_tools.append(tool_name)
                elif hasattr(msg, 'tool_calls'):
                    for tool_call in msg.tool_calls:
                        tool_name = tool_call.get('name', '')
                        if tool_name:
                            used_tools.append(tool_name)

        return used_tools


def get_mandatory_tools_for_stage(stage_id: str) -> List[str]:
    """获取指定阶段的必需工具列表"""
    stage_config = MANDATORY_TOOLS.get(stage_id, {})
    return stage_config.get("required_tools", [])


def check_image_generation_constraint(tool_name: str) -> bool:
    """检查图片生成工具是否符合约束"""
    allowed_tools = IMAGE_GENERATION_CONSTRAINTS["allowed_tools"]
    return tool_name in allowed_tools


def check_wechat_publishing_constraint(tool_name: str) -> bool:
    """检查微信发布工具是否符合约束"""
    allowed_tools = WECHAT_PUBLISHING_CONSTRAINTS["allowed_tools"]
    return tool_name in allowed_tools