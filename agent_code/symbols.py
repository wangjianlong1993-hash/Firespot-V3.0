"""
FireSpot 符号系统配置
========================

定义FireSpot工作流中使用的符号系统，替代emoji。
"""

# 阶段状态符号
FIRESPOT_SYMBOLS = {
    "pending": "○",      # 待执行：空心圆
    "running": "◐",      # 进行中：半圆
    "completed": "●",     # 完成：实心圆
    "error": "✖",         # 错误：叉号

    # 进度条符号
    "bar_filled": "■",    # 已完成
    "bar_empty": "▫",     # 未完成
    "arrow": "→",         # 箭头

    # 分隔符
    "separator": "━",     # 分隔线
    "bullet": "•",         # 列表符号
    "check": "✓",          # 对号（仅在最终输出使用）
    "cross": "✗",          # 叉号（仅在错误输出使用）
}

# 阶段名称和符号映射
FIRESPOT_STAGES = {
    "initial": {
        "name_cn": "准备",
        "name_en": "Preparation",
        "symbol": "◈",
        "order": 0
    },
    "stage1_research": {
        "name_cn": "研究",
        "name_en": "Research",
        "symbol": "R",
        "order": 1
    },
    "stage2_analysis": {
        "name_cn": "分析",
        "name_en": "Analysis",
        "symbol": "A",
        "order": 2
    },
    "stage3_planning": {
        "name_cn": "规划",
        "name_en": "Planning",
        "symbol": "P",
        "order": 3
    },
    "stage4_writing": {
        "name_cn": "写作",
        "name_en": "Writing",
        "symbol": "W",
        "order": 4
    },
    "stage5_validation": {
        "name_cn": "校验",
        "name_en": "Validation",
        "symbol": "V",
        "order": 5
    },
    "stage6_review": {
        "name_cn": "审核",
        "name_en": "Review",
        "symbol": "R",
        "order": 6
    },
    "stage7_publish": {
        "name_cn": "发布",
        "name_en": "Publish",
        "symbol": "P",
        "order": 7
    },
    "completed": {
        "name_cn": "完成",
        "name_en": "Completed",
        "symbol": "★",
        "order": 8
    }
}

# 进度条模板
def generate_progress_bar(current, total, width=30):
    """生成进度条

    Args:
        current: 当前进度（1-based）
        total: 总数
        width: 进度条宽度（字符数）

    Returns:
        str: 进度条字符串
    """
    if total == 0:
        return "[" + "▫" * width + "]"

    filled = int((current / total) * width)
    empty = width - filled

    bar = "[" + "■" * filled + "▫" * empty + "]"
    percent = int((current / total) * 100)

    return f"{bar} {percent}%"

# 阶段显示模板
def format_stage_header(stage_id, stage_name, status="running"):
    """格式化阶段标题

    Args:
        stage_id: 阶段ID (如 "stage1_research")
        stage_name: 阶段名称
        status: 状态 ("pending", "running", "completed", "error")

    Returns:
        str: 格式化的阶段标题
    """
    symbols = FIRESPOT_SYMBOLS
    stage_info = FIRESPOT_STAGES.get(stage_id, {})

    stage_num = stage_info.get("order", 0)
    total_stages = 7

    status_symbol = symbols.get(status, "?")
    progress = generate_progress_bar(stage_num, total_stages)

    return f"""
{'━' * 70}
{status_symbol} Stage {stage_num}/{total_stages}: {stage_name} {progress}
{'━' * 70}
"""

def format_startup_message():
    """格式化工作流启动消息"""
    return f"""
{'━' * 70}
FireSpot 工作流已启动
{'━' * 70}

任务执行计划 (7个阶段):

  ○ Stage 1: Research (热点研究)
  ○ Stage 2: Analysis (深度分析)
  ○ Stage 3: Planning (结构规划)
  ○ Stage 4: Writing (内容写作)
  ○ Stage 5: Validation (质量校验)
  ○ Stage 6: Review (人工审核)
  ○ Stage 7: Publish (自动发布)

{'━' * 70}
开始执行任务...
{'━' * 70}
"""

def format_stage_completion_summary():
    """格式化阶段完成总结"""
    return f"""
{'━' * 70}
所有阶段已完成
{'━' * 70}

  ● Stage 1: Research (热点研究)      完成
  ● Stage 2: Analysis (深度分析)      完成
  ● Stage 3: Planning (结构规划)      完成
  ● Stage 4: Writing (内容写作)       完成
  ● Stage 5: Validation (质量校验)   完成
  ● Stage 6: Review (人工审核)        完成
  ● Stage 7: Publish (自动发布)       完成

{'━' * 70}
"""

# 导出符号和函数
__all__ = [
    'FIRESPOT_SYMBOLS',
    'FIRESPOT_STAGES',
    'generate_progress_bar',
    'format_stage_header',
    'format_startup_message',
    'format_stage_completion_summary'
]
