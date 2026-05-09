"""
FireSpot 7.1 统一配置文件
============================
集中管理所有 FireSpot 相关配置，避免分散维护

版本 7.1 更新 (重大版本 - 高级趣味感风格):
- ✅ **🎨 行文风格升级**：从"表面口语化"到"高级趣味感"
- ✅ **🚫 严格禁止低级AI味**：去除"说白了"、"说人话就是"、"绝了"、"离谱"等表达
- ✅ **📊 真实案例优先**：用历史事件、新闻报道、真实人物故事替代虚构例子
- ✅ **🎯 具体数据说话**："1.2亿"而不是"很多"，让事实和数据说话
- ✅ **✨ 生动细节描写**：让读者"看见"画面，具体人物、行为、场景、时间
- ✅ **🧠 高信息密度**：每句话都有信息量，删除废话、重复、说教
- ✅ 阶段重新编号：Stage 6.5→7, 6.8→8, 7→9
- ✅ 按钮式审核：Stage 6采用交互式按钮(Approve/Revise/Cancel)
- ✅ ZhiPuArts生图：生图使用智谱AI GLM-Image（专业科技风格）
- ✅ 两轮审核机制：文字审核 → AI生图 → 图文合并
- ✅ 自动生图触发：用户批准文字稿后自动执行Stage 7/8
- ✅ 占位符系统：{{IMG:asset_id}} 替换为真实图片
- ✅ 三阶段审核：Stage 6(文字) → Stage 7(生图) → Stage 8(合并)
- ✅ Agent协议版本：5.0
- ✅ 双输出体系 (stage4_final.md + stage8_review_final.html)
- ✅ 完整的工具函数集成 (publishing_tools.py)

v7.1 高级趣味感核心理念：
用真实案例、具体数据、生动细节，让有趣的内容自己说话，而不是用词汇包装空洞的内容。

一个检验标准：
删除所有例子和形容词后，是否依然有有趣的信息？
- 如果否 → 说明趣味性依赖词汇包装
- 如果是 → 说明内容本身有趣

核心优势（继承自7.0 + 新增）:
1. 两轮审核：先审文字质量，批准后自动生图并合并
2. 自动化工作流：用户一次"approve"触发完整生图+合并流程
3. 灵活的占位符系统：支持Markdown和HTML双格式
4. 完整的错误处理：单个图片失败不影响整体流程
5. **高级趣味感**：内容设计精妙，避免表面口语化的AI味

版本 7.0 更新 (重大版本 - 阶段重新编号 + 按钮式审核):
- ✅ 阶段重新编号：Stage 6.5→7, 6.8→8, 7→9
- ✅ 按钮式审核：Stage 6采用交互式按钮(Approve/Revise/Cancel)
- ✅ ModelArts强制约束：生图必须使用ModelArts MCP，3次失败后终止
- ✅ 两轮审核机制：文字审核 → AI生图 → 图文合并
- ✅ 自动生图触发：用户批准文字稿后自动执行Stage 7/8
- ✅ 占位符系统：{{IMG:asset_id}} 替换为真实图片
- ✅ 三阶段审核：Stage 6(文字) → Stage 7(生图) → Stage 8(合并)
- ✅ Agent协议版本：5.0
- ✅ 双输出体系 (stage4_final.md + stage8_review_final.html)
- ✅ 完整的工具函数集成 (publishing_tools.py)

版本 5.1 更新 (融合增强版):
- ✅ 融合4.0/3.0的详细Prompt工程模板
- ✅ 增强图片生成配置（专用工具、详细prompt、自动降级）
- ✅ 双输出体系 (Draft MD + Review HTML)
- ✅ 预制按钮批准流程优化
- ✅ 完整的去AI化设计规范
- ✅ 灵活的图片来源策略

版本 5.0 更新 (重大版本):
- 实现三输出体系 (Draft MD + Review HTML + WeChat HTML)
- 强制输出规范，工作流必须生成三个文件
- 自动HTML转微信格式转换
- 完整的去AI化设计规范
- 三输出验证和完整性检查

版本 4.2 更新:
- 移除所有emoji，使用ASCII符号
- 添加实时进度追踪
- 优化阶段标记和完成状态显示
"""

from typing import List, Dict, Any

# ============================================================================
# FireSpot 版本信息
# ============================================================================
FIRESPOT_VERSION = "7.1"
FIRESPOT_AGENT_HEADER = "5.0"  # Agent协议版本标识
FIRESPOT_DESCRIPTION = "AI-powered content research, creation, and publishing agent with high-quality writing style (v7.1). Features: Real cases over fictional examples, specific data over vague descriptions, vivid details over abstract summaries, objective description over emotional hype. Strictly avoids low-level AI expressions and mechanical sentence patterns: '说白了', '说人话就是', '绝了', '离谱', '不在...而在...', '不是...而是...', '第一...第二...第三...', '一个容易被忽视的'. 2-round review workflow (Text → Images → Merged). Auto-generate images after text approval, then merge for final preview. Stage 6 uses interactive approval buttons (Approve/Revise/Cancel). Stage 7 uses ZhiPuArts (GLM-Image) for image generation (professional tech style). Merged advantages from v4.0/3.0/5.1/7.0/7.1: detailed image generation, flexible fallback, professional quality, and advanced writing style."

# ============================================================================
# 触发关键词配置 (统一数据源)
# ============================================================================
FIRESPOT_TRIGGERS: Dict[str, List[str]] = {
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
        r"FireSpot",
        r"Firespot",
        r"firespot-wechat",
    ],
}

# ============================================================================
# 7阶段工作流配置 (统一阶段定义)
# ============================================================================
FIRESPOT_STAGES: Dict[str, Dict[str, str]] = {
    "stage1_research": {
        "id": "stage1_research",
        "name_cn": "阶段1：热点研究",
        "name_en": "Stage 1: Research",
        "output_format": "## 阶段 1: 🔍 Research (热点研究)",
        "description": "多平台热点研究和数据收集",
        "duration_minutes": 5,
    },
    "stage2_analysis": {
        "id": "stage2_analysis",
        "name_cn": "阶段2：深度分析",
        "name_en": "Stage 2: Analysis",
        "output_format": "## 阶段 2: 📊 Analysis (深度分析)",
        "description": "内容深度分析和洞察提取",
        "duration_minutes": 3,
    },
    "stage3_planning": {
        "id": "stage3_planning",
        "name_cn": "阶段3：内容规划",
        "name_en": "Stage 3: Planning",
        "output_format": "## 阶段 3: 📋 Planning (内容规划)",
        "description": "文章结构规划和图片资产规划",
        "duration_minutes": 2,
    },
    "stage4_writing": {
        "id": "stage4_writing",
        "name_cn": "阶段4：内容创作",
        "name_en": "Stage 4: Writing",
        "output_format": "## 阶段 4: ✍️ Writing (内容创作)",
        "description": "高质量文章撰写和图片锚点插入",
        "duration_minutes": 10,
    },
    "stage5_validation": {
        "id": "stage5_validation",
        "name_cn": "阶段5：质量校验",
        "name_en": "Stage 5: Validation",
        "output_format": "## 阶段 5: ✅ Validation (质量校验)",
        "description": "文章质量校验和合规检查",
        "duration_minutes": 2,
    },
    "stage6_review": {
        "id": "stage6_review",
        "name_cn": "阶段6：人工审核",
        "name_en": "Stage 6: Review",
        "output_format": "## 阶段 6: 👁️ Review (人工审核)",
        "description": "生成审核HTML并等待用户批准",
        "duration_minutes": 5,
    },
    "stage6_text_review": {
        "id": "stage6_text_review",
        "name_cn": "阶段6：文字版审核",
        "name_en": "Stage 6: Text Review",
        "output_format": "## 阶段 6: 👁️ Text Review (文字版审核)",
        "description": "生成纯文字版HTML审核稿，等待用户通过按钮批准(Approve/Revise/Cancel)",
        "duration_minutes": 2,
    },
    "stage7_image_generation": {
        "id": "stage7_image_generation",
        "name_cn": "阶段7：AI自动生图",
        "name_en": "Stage 7: AI Image Generation",
        "output_format": "## 阶段 7: 🎨 AI Image Generation (AI自动生图)",
        "description": "强制使用ModelArts MCP工具生成封面图、正文图、金句图，最多重试3次",
        "duration_minutes": 2,
    },
    "stage8_merge_preview": {
        "id": "stage8_merge_preview",
        "name_cn": "阶段8：图文合并预览",
        "name_en": "Stage 8: Merge & Preview",
        "output_format": "## 阶段 8: 📄 Merge & Preview (图文合并预览)",
        "description": "将文字内容与真实图片合并，生成最终预览文档",
        "duration_minutes": 1,
    },
    "stage9_publish": {
        "id": "stage9_publish",
        "name_cn": "阶段9：微信发布",
        "name_en": "Stage 9: WeChat Publishing",
        "output_format": "## 阶段 9: 📱 WeChat Publishing (微信发布)",
        "description": "发布到微信公众号草稿箱（可选功能）",
        "duration_minutes": 2,
    },
}

# 阶段执行顺序
FIRESPOT_STAGE_ORDER: List[str] = [
    "initial",
    "stage1_research",
    "stage2_analysis",
    "stage3_planning",
    "stage4_writing",
    "stage5_validation",
    "stage6_text_review",      # 第一轮审核：文字版（按钮式Approve/Revise/Cancel）
    "stage7_image_generation",  # AI自动生图（强制ModelArts MCP，3次重试）
    "stage8_merge_preview",     # 第二轮审核：图文合并版
    "stage9_publish",           # 可选：微信发布
    "completed",
]

# ============================================================================
# 内容生成配置
# ============================================================================
FIRESPOT_CONTENT_CONFIG: Dict[str, Any] = {
    "min_word_count": 800,
    "max_word_count": 1500,
    "target_word_count": 1200,
    "forbidden_phrases": [
        "大家好，今天给大家分享",
        "首先...其次...最后",
        "相信很多小伙伴都",
        "话不多说，直接上干货",
    ],
    "required_sections": [
        "title", "lead", "body", "conclusion"
    ]
}

# ============================================================================
# 图片资产配置
# ============================================================================
FIRESPOT_IMAGE_CONFIG: Dict[str, Any] = {
    "enabled": True,
    "api_provider": "zhipuarts",  # 使用ZhiPuArts作为生图服务（专业科技风格）
    "model": "GLM-Image",  # 智谱AI GLM-Image模型
    "fallback_to_mock": False,  # 禁用模拟生成，必须使用真实API工具
    "max_retries": 3,  # ZhiPuArts重试次数（最多3次）
    "retry_delay_seconds": 2,  # 重试延迟
    "default_sources": [
        "user_provided",    # 用户上传图片 (优先级1)
        "generate",         # AI生成图片 (优先级2) - 使用ZhiPuArts
    ],
    "required_assets": {
        "cover": {
            "count": 1,
            "aspect_ratio": "2.35:1",
            "role": "cover",
            "upload_policy": "thumb",
            "default_width": 1920,
            "default_height": 816,
        },
        "inline": {
            "count": 3,
            "aspect_ratio": "16:9",
            "role": "inline",
            "upload_policy": "article_image",
            "default_width": 1920,
            "default_height": 1080,
        },
        "quote": {
            "count": 1,
            "aspect_ratio": "4:5",
            "role": "quote",
            "upload_policy": "article_image",
            "default_width": 1080,
            "default_height": 1350,
        }
    }
}

# ============================================================================
# 图片生成Prompt模板（融合4.0/3.0优势）
# ============================================================================
FIRESPOT_IMAGE_PROMPTS: Dict[str, str] = {
    # 封面图Prompt模板
    "cover_template": """Create a professional, modern cover image for a tech article about AI.
Title: {article_title}
Style: Clean, minimalist, tech-focused
Elements: Abstract AI/technology symbols, chess/game board metaphor (optional)
Colors: Blue, purple, or dark theme
Aspect ratio: {aspect_ratio}
Composition: Centralized composition with clear focal point
Mood: Professional, innovative, trustworthy""",

    # 封面图Prompt模板（中文版）
    "cover_template_zh": """创建一张专业、现代的科技文章封面图。
文章标题：{article_title}
风格：简洁、极简主义、科技感
元素：抽象AI/技术符号、棋盘游戏隐喻（可选）
配色：蓝色、紫色或深色主题
比例：{aspect_ratio}
构图：中心构图，清晰的焦点
氛围：专业、创新、可信赖""",

    # 正文图Prompt模板
    "inline_template": """Create a simple illustration for a tech article section.
Section: {section_title}
Content: {section_content}
Style: Minimalist, professional diagram or icon
Colors: Complementary to cover, professional palette
Aspect ratio: {aspect_ratio}
Purpose: Visual aid to help readers understand the concept
Detail level: Clean and uncluttered, focus on clarity""",

    # 正文图Prompt模板（中文版）
    "inline_template_zh": """为科技文章的章节创建简单的插图。
章节标题：{section_title}
内容概要：{section_content}
风格：极简主义、专业图表或图标
配色：与封面图协调的专业配色方案
比例：{aspect_ratio}
目的：帮助读者理解概念的可视化辅助
细节：清晰不杂乱，重点突出""",

    # 引用图Prompt模板
    "quote_template": """Create an elegant quote image for a tech article.
Quote text: {quote_text}
Author: {author}
Style: Editorial design, typography-focused
Colors: Subtle gradient background, high contrast text
Aspect ratio: {aspect_ratio}
Layout: Centered text with generous white space
Mood: Insightful, inspiring, memorable""",

    # 引用图Prompt模板（中文版）
    "quote_template_zh": """为科技文章创建优雅的引用图。
引用文字：{quote_text}
作者：{author}
风格：编辑设计，以排版为核心
配色：柔和渐变背景，高对比度文字
比例：{aspect_ratio}
布局：居中文字，充足的留白
氛围：有洞察力、启发人心、印象深刻""",
}

# ============================================================================
# 微信发布配置
# ============================================================================
FIRESPOT_WECHAT_CONFIG: Dict[str, Any] = {
    "enabled": True,
    "auto_publish": False,  # 需要用户明确 approve
    "draft_create_enabled": True,
    "required_approval": True,
    "approval_keywords": ["approve", "确认发布", "同意发布"],
    "max_retries": 3
}

# ============================================================================
# MCP 工具配置
# ============================================================================
FIRESPOT_MCP_TOOLS: Dict[str, Any] = {
    "zhipuarts": {
        "enabled": True,
        "server_name": "zhipuarts",
        "tools": [
            "mcp_zhipuarts_generate_image"
        ]
    },
    "wechat_publisher": {
        "enabled": True,
        "server_name": "wechat-publisher",
        "tools": [
            "mcp_wechat_prepare_image",
            "mcp_wechat_create_draft"
        ]
    }
}

# ============================================================================
# 文件路径配置
# ============================================================================
FIRESPOT_PATHS: Dict[str, str] = {
    "workspace": "/mnt/user-data/workspace",
    "outputs": "/mnt/user-data/outputs",
    "images": "/mnt/user-data/images",
    "stage1_research": "/mnt/user-data/workspace/stage1_research.json",
    "stage2_analysis": "/mnt/user-data/workspace/stage2_analysis.json",
    "stage3_outline": "/mnt/user-data/workspace/stage3_outline.json",
    "stage4_draft": "/mnt/user-data/outputs/stage4_draft.md",
    "stage4_article": "/mnt/user-data/workspace/stage4_article.json",
    "stage4_final": "/mnt/user-data/outputs/stage4_final.md",
    "stage5_validation": "/mnt/user-data/workspace/stage5_validation.json",
    "stage6_text_review": "/mnt/user-data/outputs/stage6_review_text.html",
    "stage7_images": "/mnt/user-data/workspace/stage7_images.json",
    "stage6_review": "/mnt/user-data/outputs/stage6_review.html",
    "stage8_final": "/mnt/user-data/outputs/stage8_review_final.html",
    "stage9_publish": "/mnt/user-data/workspace/stage9_publish_assets.json",
}

# ============================================================================
# 工作流输出约束 - 强制要求 (基于任务 fae0def8-4597-46bc-a575-48710c30c1b9 优秀案例)
# ============================================================================
FIRESPOT_OUTPUT_REQUIREMENTS: Dict[str, Any] = {
    "enabled": True,
    "version": "3.0",
    "description": "双输出体系 - Draft MD + Review HTML",
    "output_count": 2,  # 必须输出两个文件

    # Stage 4: Writing - 必须输出纯文本Markdown草稿
    "stage4_draft_md": {
        "required": True,
        "file_path": "/mnt/user-data/outputs/stage4_draft.md",
        "format": "markdown",
        "encoding": "utf-8",
        "purpose": "编辑、版本控制、后续处理",
        "reference_task": "fae0def8-4597-46bc-a575-48710c30c1b9",
        "content_requirements": {
            "title_format": "# 文章标题 (h1格式，#后空一格)",
            "section_format": "## 章节标题 (h2格式，##后空一格)",
            "image_placeholders": "{{IMG:asset_id}} 独占一行，前后空行",
            "citations": "[n] 上标格式，紧跟引用内容后",
            "bold_text": "**文本** 双星号包裹",
            "italic_text": "*标题* 单星号（用于引用的标题）",
            "reference_section": "--- 分隔线后，按序号列出参考来源",
            "forbidden_content": [
                "禁止任何HTML标签（<p>, <div>, <style>, <h1>, <h2>等）",
                "禁止emoji表情符号",
                "禁止CSS样式代码",
            ],
        },
        "example_format": """
# 文章标题

{{IMG:cover_01}}

文章开篇第一段内容，介绍背景和主题[1]。

第二段展开说明，使用**粗体**强调重点内容[2]。

## 一、章节标题

章节正文内容，详细阐述观点[3]。

{{IMG:inline_01}}

继续展开论述[4]。

## 二、另一章节

更多内容...

## 结语

总结全文，升华主题[10]。

---

**参考来源**

[1] 作者. (年份). *文章标题*. 来源.
[2] Author. (Year). *Article Title*. Source.
""",
        "quality_checks": {
            "word_count": "800-3000字（根据文章类型调整）",
            "citation_count": "至少10处独立引用",
            "image_anchors": "至少4个图片锚点 (cover_01/inline_01/inline_02/quote_01)",
            "forbidden_phrases": "禁止使用模板化句式（如'大家好今天给大家分享'）",
        },
    },

    # Stage 6-Output-1: Review HTML - 浏览器预览版本
    # 参考任务: fae0def8-4597-46bc-a575-48710c30c1b9/stage6_review.html
    "stage6_review_html": {
        "required": True,
        "file_path": "/mnt/user-data/outputs/stage6_review.html",
        "format": "html",
        "encoding": "utf-8",
        "purpose": "浏览器预览、审核、展示效果",
        "design_philosophy": "专业学术风格 - 参考 fae0def8-4597-46bc-a575-48710c30c1b9",
        "reference_task": "fae0def8-4597-46bc-a575-48710c30c1b9",
        "html_structure": {
            "doctype": "<!DOCTYPE html>",
            "html_tag": '<html lang="zh-CN">',
            "head_tag": "<head>",
            "meta_charset": '<meta charset="UTF-8">',
            "title_tag": "<title>文章标题</title>",
            "body_tag": "<body>",
            "article_wrapper": '<article style="...">',
        },
        "html_style_requirements": {
            # 布局容器 - 使用 <article> 标签
            "article_style": "max-width:680px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#1a1a1a;line-height:1.8;font-size:16px;padding:20px;",

            # 字体系统（完整字体栈）
            "font_family": "-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif",

            # 颜色方案 - 蓝色主题 (#2b5797)
            "color_scheme": {
                "text_primary": "#1a1a1a",
                "text_secondary": "#666",
                "accent_blue": "#2b5797",  # 主色调
                "border_color": "#ddd",
            },

            # H1 标题样式（居中，蓝色底边框）
            "h1_style": "text-align:center;font-size:22px;font-weight:700;color:#1a1a1a;margin-bottom:24px;border-bottom:2px solid #2b5797;padding-bottom:12px;",

            # 作者/元信息行样式（居中，灰色）
            "author_line_style": "text-align:center;color:#888;font-size:13px;margin-bottom:30px;",

            # H2 章节标题样式（左侧蓝色边框）
            "h2_style": "font-size:18px;color:#2b5797;border-left:4px solid #2b5797;padding-left:10px;margin-top:32px;",

            # 正文段落样式
            "p_style": "margin:12px 0;text-align:justify;font-size:16px;",

            # 分隔线样式
            "hr_style": "border:none;border-top:1px solid #ddd;margin:30px 0;",

            # 参考来源区域样式（灰色背景）
            "ref_section_style": "background:#f7f8fa;padding:16px 20px;border-radius:6px;font-size:13px;color:#666;line-height:1.9;",

            # 参考来源标题样式
            "ref_title_style": "font-weight:600;color:#333;margin-bottom:8px;font-size:14px;",

            # 参考来源条目样式
            "ref_item_style": "margin:8px 0;",
        },
        "html_example": """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>文章标题</title>
</head>
<body>
<article style="max-width:680px;margin:0 auto;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;color:#1a1a1a;line-height:1.8;font-size:16px;padding:20px;">

<h1 style="text-align:center;font-size:22px;font-weight:700;color:#1a1a1a;margin-bottom:24px;border-bottom:2px solid #2b5797;padding-bottom:12px;">文章标题</h1>

<p style="text-align:center;color:#888;font-size:13px;margin-bottom:30px;">FireSpot AI · 2026</p>

{{IMG:cover_01}}

<p>文章正文第一段内容...</p>

<h2 style="font-size:18px;color:#2b5797;border-left:4px solid #2b5797;padding-left:10px;margin-top:32px;">一、章节标题</h2>

<p>章节正文内容...</p>

<hr style="border:none;border-top:1px solid #ddd;margin:30px 0;">

<section style="background:#f7f8fa;padding:16px 20px;border-radius:6px;font-size:13px;color:#666;line-height:1.9;">
<p style="font-weight:600;color:#333;margin-bottom:8px;font-size:14px;">参考来源</p>
<p>[1] 作者. (年份). <em>文章标题</em>. 来源.</p>
</section>

</article>
</body>
</html>""",
        "quality_checks": {
            "doctype_present": "必须包含 <!DOCTYPE html>",
            "charset_utf8": "必须包含 <meta charset=\"UTF-8\">",
            "article_tag": "必须使用 <article> 标签包裹内容",
            "inline_styles": "所有样式必须是内联的 (style=\"...\")",
            "color_scheme": "必须使用 #2b5797 作为主色调",
            "no_style_tag": "不使用 <style> 标签（所有样式内联）",
            "image_placeholders": "图片占位符格式 {{IMG:asset_id}}",
        },
    },

    # Stage 6: 最终产出清单
    "final_outputs": {
        "mandatory": [
            {
                "type": "draft_md",
                "description": "纯文本Markdown草稿（包含图片占位符）",
                "file": "stage4_draft.md",
                "purpose": "编辑、版本控制、后续处理",
                "stage": "Stage 4",
            },
            {
                "type": "review_html",
                "description": "HTML排版预览版本（浏览器预览）",
                "file": "stage6_review.html",
                "purpose": "浏览器预览、审核、展示效果",
                "stage": "Stage 6",
                "features": ["保留<style>标签", "完整HTML结构", "专业排版样式"],
            },
        ],
        "validation": {
            "all_required": "两个文件都必须输出，缺一不可",
            "check_point": "Stage 6结束时必须确认两个文件都存在",
            "error_message": "输出不完整：缺少 stage4_draft.md 或 stage6_review.html",
            "order": "Stage 4生成draft.md → Stage 6生成review.html",
        },
    },
}

# ============================================================================
# 辅助函数
# ============================================================================
def get_stage_info(stage_id: str) -> Dict[str, str]:
    """获取阶段信息"""
    return FIRESPOT_STAGES.get(stage_id, {})

def get_all_stage_names() -> List[str]:
    """获取所有阶段名称列表"""
    return [FIRESPOT_STAGES[stage]["name_cn"] for stage in FIRESPOT_STAGE_ORDER if stage in FIRESPOT_STAGES]

def is_trigger_word(content: str) -> bool:
    """检查是否包含触发关键词 (简化版本，供其他模块使用)"""
    import re
    content_lower = content.lower()

    for patterns in FIRESPOT_TRIGGERS.values():
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
    return False

def get_config_summary() -> Dict[str, Any]:
    """获取配置摘要"""
    return {
        "version": FIRESPOT_VERSION,
        "description": FIRESPOT_DESCRIPTION,
        "trigger_categories": len(FIRESPOT_TRIGGERS),
        "total_stages": len([s for s in FIRESPOT_STAGE_ORDER if s != "initial" and s != "completed"]),
        "image_generation_enabled": FIRESPOT_IMAGE_CONFIG["enabled"],
        "wechat_publishing_enabled": FIRESPOT_WECHAT_CONFIG["enabled"],
        "mcp_tools_count": len([t for t in FIRESPOT_MCP_TOOLS.values() if t["enabled"]])
    }

# 导出主要配置
__all__ = [
    "FIRESPOT_VERSION",
    "FIRESPOT_DESCRIPTION",
    "FIRESPOT_TRIGGERS",
    "FIRESPOT_STAGES",
    "FIRESPOT_STAGE_ORDER",
    "FIRESPOT_CONTENT_CONFIG",
    "FIRESPOT_IMAGE_CONFIG",
    "FIRESPOT_IMAGE_PROMPTS",  # 新增：图片生成Prompt模板
    "FIRESPOT_WECHAT_CONFIG",
    "FIRESPOT_MCP_TOOLS",
    "FIRESPOT_PATHS",
    "FIRESPOT_OUTPUT_REQUIREMENTS",  # 新增：输出约束配置
    "get_stage_info",
    "get_all_stage_names",
    "is_trigger_word",
    "get_config_summary",
]