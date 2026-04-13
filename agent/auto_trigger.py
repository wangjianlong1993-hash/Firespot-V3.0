"""
FireSpot Auto-Trigger Middleware for DeerFlow
==============================================

This middleware automatically detects FireSpot 4.0 trigger keywords
in user messages and forces the 7-stage workflow.

Author: FireSpot Team
Version: 4.0.1 (Auto-Trigger Enhancement)
"""

import logging
import re
from typing import Dict, Any, Optional
from langchain.agents.middleware import AgentMiddleware
from langgraph.runtime import Runtime
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import BaseMessage, HumanMessage

from ..thread_state import ThreadState


logger = logging.getLogger(__name__)


# FireSpot 4.0 Trigger Patterns
FIRESPOT_TRIGGERS = {
    "direct_writing": [
        r"帮我写",
        r"写一篇",
        r"创作",
        r"撰写",
        r"做.*文章",
    ],
    "weixin_related": [
        r"公众号",
        r"微信公众号",
        r"推文",
        r"微信推文",
    ],
    "perspective_analysis": [
        r"从.*角度.*写",
        r"从.*角度.*分析",
        r"从.*角度.*是什么",
        r"关于.*的分析",
    ],
    "explicit_mention": [
        r"firespot",
        r"firespot-wechat",
        r"FireSpot",
        r"Firespot",
    ],
}


def should_trigger_firespot(message_content) -> bool:
    """
    Check if the message content contains FireSpot trigger keywords.

    Args:
        message_content: The user's message content (str or list for structured content)

    Returns:
        True if FireSpot workflow should be triggered, False otherwise
    """
    # Handle structured content (list with text/image blocks)
    if isinstance(message_content, list):
        # Extract text content from structured messages
        text_parts = []
        for block in message_content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif "text" in block:
                    text_parts.append(block["text"])
            elif isinstance(block, str):
                text_parts.append(block)
        message_content = " ".join(text_parts)

    # Ensure we have a string
    if not isinstance(message_content, str):
        return False

    content_lower = message_content.lower()

    # Check each trigger pattern
    for category, patterns in FIRESPOT_TRIGGERS.items():
        for pattern in patterns:
            if re.search(pattern, message_content, re.IGNORECASE):
                logger.info(
                    f"🔥 FireSpot auto-triggered by pattern: {pattern} (category: {category})",
                    extra={
                        "firespot_event": "auto_trigger",
                        "trigger_category": category,
                        "trigger_pattern": pattern,
                        "message_preview": message_content[:100],
                    }
                )
                return True

    return False


def inject_firespot_activation_message(original_message) -> str:
    """
    Inject FireSpot activation message into the user's message.

    This ensures the LLM knows it must follow the 7-stage workflow.

    Args:
        original_message: The original user message (str or list)

    Returns:
        Enhanced message with FireSpot activation (always str)
    """
    # Convert structured content to string if needed
    if isinstance(original_message, list):
        text_parts = []
        for block in original_message:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif "text" in block:
                    text_parts.append(block["text"])
            elif isinstance(block, str):
                text_parts.append(block)
        message_text = " ".join(text_parts)
    else:
        message_text = str(original_message) if original_message else ""

    activation_prompt = """
─────────────────────────────────────────────────────────────
  FireSpot 4.0 Workflow
─────────────────────────────────────────────────────────────

Content creation detected. Professional workflow activated.

SEVEN STAGE PROCESS

  01  Research      Investigate trends and gather insights
  02  Analysis      Deep dive into subject matter
  03  Planning      Structure and outline content
  04  Writing       Craft the narrative
  05  Validation   Verify quality and accuracy
  06  Review       Request user approval
  07  Publishing   Prepare for distribution

REQUIREMENTS

  • Execute stages sequentially
  • Output format: ## Stage X: [Name]
  • Word count: 800–1500
  • Stage 6: Use ask_clarification for user review
  • Complete all stages without skipping

Starting Stage 1...

─────────────────────────────────────────────────────────────

Original Request:
"""

    return activation_prompt + message_text


class FireSpotAutoTriggerMiddleware(AgentMiddleware[ThreadState]):
    """
    Middleware to automatically detect and trigger FireSpot 4.0 workflow.

    This middleware intercepts user messages and checks for trigger keywords.
    If a trigger is detected, it injects activation instructions to force the
    LLM to follow the 7-stage workflow.
    """

    def __init__(self):
        super().__init__()
        self.triggered_threads = set()

    def before_model(self, state: ThreadState, runtime: Runtime) -> Dict[str, Any]:
        """
        Called before model invocation.

        Checks if the user's message contains FireSpot trigger keywords.
        If triggered, injects activation instructions into the conversation.
        """
        messages = state.get("messages", [])
        # Get thread_id from runtime context
        thread_id = runtime.context.get("thread_id") if runtime.context else None
        if not thread_id:
            return {}

        if not messages:
            return {}

        # Get the last human message
        last_human_message = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_human_message = msg
                break

        if not last_human_message:
            return {}

        # Check if already triggered for this thread
        if thread_id in self.triggered_threads:
            return {}

        # Check if FireSpot should be triggered
        content = last_human_message.content
        if should_trigger_firespot(content):
            # Mark as triggered
            self.triggered_threads.add(thread_id)

            # Inject activation message
            enhanced_content = inject_firespot_activation_message(content)

            # Replace the message content in state
            # Note: This modifies the state before it reaches the model
            modified_messages = messages.copy()
            for i, msg in enumerate(modified_messages):
                if isinstance(msg, HumanMessage) and msg == last_human_message:
                    # Create new message with enhanced content
                    modified_messages[i] = HumanMessage(content=enhanced_content)
                    break

            logger.info(
                f"✨ FireSpot 4.0 auto-triggered for thread {thread_id}",
                extra={
                    "firespot_event": "auto_triggered",
                    "thread_id": thread_id,
                    "original_message": content[:200],
                }
            )

            return {"messages": modified_messages}

        return {}

    def after_model(self, state: ThreadState, runtime: Runtime) -> Dict[str, Any]:
        """
        Called after model invocation.

        Currently no post-processing needed.
        """
        return {}


# Export
__all__ = [
    "FireSpotAutoTriggerMiddleware",
    "should_trigger_firespot",
    "inject_firespot_activation_message",
    "FIRESPOT_TRIGGERS",
]
