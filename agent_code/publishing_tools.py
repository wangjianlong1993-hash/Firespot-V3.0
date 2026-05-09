"""
FireSpot Publishing Tools Handler - Enhanced Version 5.1
========================================================

融合4.0/3.0优势的增强版本：
- 详细的Prompt工程模板
- 专用生图工具（封面、正文、引用）
- 灵活的图片来源策略
- 自动降级机制

Author: FireSpot Team
Version: 5.1 (Enhanced)
"""

import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


# ============================================================================
# Prompt构建器（融合4.0/3.0优势）
# ============================================================================

class FireSpotPromptBuilder:
    """
    FireSpot专用Prompt构建器（v7.0）

    为微信公众号内容创作生成定制化的图片prompt
    区别于通用prompt，专注于：
    1. 公众号专业风格（非小红书风格）
    2. 科技/哲学主题导向
    3. 符合FireSpot 9阶段工作流要求
    """

    @staticmethod
    def build_cover_prompt(
        article_title: str,
        article_topic: str = None,
        style: str = "wechat_tech",
        language: str = "zh"
    ) -> str:
        """
        构建FireSpot公众号封面图prompt

        规格要求：
        - 尺寸：1920x816 (2.35:1 横版)
        - 风格：专业、现代、科技感
        - 用途：吸引点击，传达主题

        Args:
            article_title: 文章标题
            article_topic: 文章主题（可选）
            style: 风格（wechat_tech, wechat_philosophy, wechat_minimal）
            language: 语言（zh, en）

        Returns:
            完整的prompt字符串
        """
        if language == "zh":
            base_prompt = f"""【FireSpot公众号封面图】
文章标题：{article_title}
主题：{article_topic or article_title}

设计要求：
- 风格：{FireSpotPromptBuilder._get_style_description_zh(style)}
- 构图：横版2.35:1，中心视觉焦点
- 配色：专业科技配色（深蓝、紫色、渐变）
- 元素：抽象符号、几何图形、简约图标
- 氛围：专业可信、现代创新、有深度
- 文字处理：预留标题位置或融合到设计中

避免：小红书风格、过度装饰、卡通元素、暖色调
目标：吸引高知读者，传达专业权威"""

            return base_prompt
        else:
            return f"""【FireSpot WeChat Cover Image】
Title: {article_title}
Topic: {article_topic or article_title}

Design Requirements:
- Style: Professional, modern, tech-focused
- Aspect Ratio: 2.35:1 horizontal
- Colors: Professional tech palette (deep blue, purple, gradients)
- Elements: Abstract symbols, geometric shapes, minimal icons
- Mood: Professional, innovative, insightful
- Text: Integrate title or reserve space for it

Avoid: Xiaohongshu style, over-decoration, cartoon elements, warm colors
Target: Educated readers, professional authority"""

    @staticmethod
    def build_inline_prompt(
        section_title: str,
        section_content: str,
        style: str = "wechat_diagram",
        language: str = "zh"
    ) -> str:
        """
        构建FireSpot公众号正文插图prompt

        规格要求：
        - 尺寸：1920x1080 (16:9 横版)
        - 风格：极简、信息图、概念图
        - 用途：辅助理解文章内容

        Args:
            section_title: 章节标题
            section_content: 章节内容摘要
            style: 风格（wechat_diagram, wechat_concept, wechat_timeline）
            language: 语言

        Returns:
            完整的prompt字符串
        """
        # 提取关键概念（前150字）
        content_preview = section_content[:150] if len(section_content) > 150 else section_content

        if language == "zh":
            return f"""【FireSpot公众号正文插图】
章节标题：{section_title}
内容要点：{content_preview}

设计要求：
- 风格：极简信息图或概念示意图
- 构图：横版16:9，清晰层次结构
- 配色：与封面协调的专业配色
- 目的：可视化解释复杂概念
- 细节：简洁不杂乱，重点突出
- 留白：充足，避免过度拥挤

用途：帮助读者快速理解章节核心概念
避免：装饰性元素、无关内容、过于抽象"""

    @staticmethod
    def build_quote_prompt(
        quote_text: str,
        author: str = None,
        style: str = "wechat_typography",
        language: str = "zh"
    ) -> str:
        """
        构建FireSpot公众号金句配图prompt

        规格要求：
        - 尺寸：1080x1350 (4:5 竖版)
        - 风格：排版设计、文字为主
        - 用途：突出核心观点，便于分享

        Args:
            quote_text: 金句文字
            author: 作者
            style: 风格（wechat_typography, wechat_card, wechat_minimal）
            language: 语言

        Returns:
            完整的prompt字符串
        """
        author_text = f"—— {author}" if author else ""

        if language == "zh":
            return f"""【FireSpot公众号金句配图】
金句内容：{quote_text} {author_text}

设计要求：
- 风格：Typography-focused，以文字排版为核心
- 构图：竖版4:5，居中排版
- 背景：柔和渐变（浅灰到白）或纯色
- 字体：现代无衬线，清晰易读
- 层次：主次分明，重点突出
- 留白：充足，呼吸感

用途：突出核心观点，便于读者分享收藏
避免：过度装饰、花哨背景、影响文字可读性"""

    @staticmethod
    def _get_style_description_zh(style: str) -> str:
        """获取风格描述（中文）"""
        style_map = {
            "wechat_tech": "专业科技风，深色主题，抽象AI/技术符号",
            "wechat_philosophy": "哲学思考风，简约深邃，几何隐喻",
            "wechat_minimal": "极简主义，大量留白，单一焦点",
        }
        return style_map.get(style, "专业现代风，科技感，可信")


# ============================================================================
# 通用Prompt构建器（保留向后兼容）
# ============================================================================

class ImagePromptBuilder:
    """
    通用图片生成Prompt构建器

    融合4.0/3.0的详细prompt工程方法，提供高质量、场景化的prompt模板
    """

    @staticmethod
    def build_cover_prompt(
        article_title: str,
        article_topic: str = None,
        style: str = "professional",
        language: str = "zh"
    ) -> str:
        """
        构建封面图生成prompt

        Args:
            article_title: 文章标题
            article_topic: 文章主题（可选）
            style: 风格（professional, xiaohongshu, minimalist）
            language: 语言（zh, en）

        Returns:
            完整的prompt字符串
        """
        if style == "xiaohongshu":
            # 小红书风格（融合Mushroom优势）
            if language == "zh":
                return f"""小红书封面图设计，温暖插画风格
主题：{article_title}
展示：{article_topic or article_title}
场景：充满活力的女性形象或专业场景
配色：柔和温馨，使用暖黄色、粉色或清新蓝绿
构图：3:4竖版构图，中心对称，适合小红书封面
细节：简洁不杂乱，突出主题文字
氛围：积极向上、温暖治愈、专业可信"""
            else:
                return f"""Xiaohongshu cover design, warm illustration style
Topic: {article_title}
Scene: {article_topic or article_title}
Colors: Warm and cozy, using yellow, pink, or fresh blue-green
Aspect ratio: 3:4 portrait
Mood: Positive, warm, professional"""

        elif style == "minimalist":
            # 极简主义风格
            if language == "zh":
                return f"""创建一张专业、现代的科技文章封面图
文章标题：{article_title}
风格：极简主义、科技感、专业
元素：抽象AI/技术符号、几何图形、线条
配色：蓝色、紫色或深色主题，高对比度
比例：2.35:1横版
构图：中心构图，清晰的焦点，充足留白
氛围：专业、创新、可信赖"""
            else:
                return f"""Create a professional, modern cover image
Title: {article_title}
Style: Minimalist, tech-focused, clean
Elements: Abstract AI/technology symbols, geometric shapes
Colors: Blue, purple, or dark theme, high contrast
Aspect ratio: 2.35:1
Composition: Centralized with clear focal point
Mood: Professional, innovative, trustworthy"""

        else:  # professional (default)
            # 专业风格（默认）
            if language == "zh":
                return f"""创建一张专业、现代的科技文章封面图
文章标题：{article_title}
主题：{article_topic or article_title}
风格：专业、现代、科技感
元素：抽象AI/技术符号、棋盘游戏隐喻（可选）
配色：蓝色、紫色或深色主题，渐变效果
比例：2.35:1横版
构图：中心构图，清晰的焦点，视觉冲击力
氛围：专业、创新、可信赖"""
            else:
                return f"""Create a professional, modern cover image for a tech article
Title: {article_title}
Topic: {article_topic or article_title}
Style: Professional, modern, tech-focused
Elements: Abstract AI/technology symbols, chess/game board metaphor (optional)
Colors: Blue, purple, or dark theme with gradients
Aspect ratio: 2.35:1
Composition: Centralized composition with clear focal point
Mood: Professional, innovative, trustworthy"""

    @staticmethod
    def build_inline_prompt(
        section_title: str,
        section_content: str,
        style: str = "minimalist",
        language: str = "zh"
    ) -> str:
        """
        构建正文插图生成prompt

        Args:
            section_title: 章节标题
            section_content: 章节内容摘要
            style: 风格（minimalist, diagram, icon）
            language: 语言（zh, en）

        Returns:
            完整的prompt字符串
        """
        content_preview = section_content[:150] if len(section_content) > 150 else section_content

        if language == "zh":
            return f"""为科技文章创建简洁的章节插图
章节标题：{section_title}
内容概要：{content_preview}
风格：极简主义、专业图表或信息图
配色：与封面图协调的专业配色方案
比例：16:9横版
目的：帮助读者理解概念的可视化辅助
细节：清晰不杂乱，重点突出，避免过多元素
构图：简洁平衡，留白充足"""
        else:
            return f"""Create a simple illustration for a tech article section
Section: {section_title}
Content: {content_preview}
Style: Minimalist, professional diagram or infographic
Colors: Complementary to cover, professional palette
Aspect ratio: 16:9
Purpose: Visual aid to help readers understand the concept
Detail level: Clean and uncluttered, focus on clarity
Composition: Simple and balanced with generous white space"""

    @staticmethod
    def build_quote_prompt(
        quote_text: str,
        author: str = None,
        style: str = "editorial",
        language: str = "zh"
    ) -> str:
        """
        构建引用图生成prompt

        Args:
            quote_text: 引用文字
            author: 作者
            style: 风格（editorial, typography, artistic）
            language: 语言（zh, en）

        Returns:
            完整的prompt字符串
        """
        author_text = f"—— {author}" if author else ""

        if language == "zh":
            return f"""为科技文章创建优雅的引用配图
引用文字：{quote_text} {author_text}
风格：编辑设计，以排版为核心， Typography-focused
配色：柔和渐变背景（浅灰到白色），高对比度文字
布局：居中排版，充足的留白，文字层次分明
比例：4:5竖版
字体：现代无衬线字体，清晰易读
氛围：有洞察力、启发人心、印象深刻
细节：避免过度装饰，保持简洁专业"""
        else:
            return f"""Create an elegant quote image for a tech article
Quote text: {quote_text} {author_text}
Style: Editorial design, typography-focused
Colors: Soft gradient background (light gray to white), high contrast text
Layout: Centered typography with generous white space
Aspect ratio: 4:5
Font: Modern sans-serif, clear and readable
Mood: Insightful, inspiring, memorable
Details: Avoid over-decoration, keep it simple and professional"""


# ============================================================================
# ModelArts图片生成（融合4.0/3.0优势）
# ============================================================================

async def generate_cover_image(
    article_title: str,
    article_topic: str = None,
    style: str = "professional",
    aspect_ratio: str = "2.35:1",
    width: int = 1920,
    height: int = 816,
    mcp_tools: Optional[Dict] = None,
    language: str = "zh"
) -> Dict[str, Any]:
    """
    生成封面图（专用工具）

    融合4.0/3.0的详细prompt工程，提供高质量的封面图生成

    Args:
        article_title: 文章标题
        article_topic: 文章主题（可选）
        style: 风格（professional, xiaohongshu, minimalist）
        aspect_ratio: 图片比例
        width: 宽度
        height: 高度
        mcp_tools: MCP工具字典
        language: 语言

    Returns:
        包含图片信息的字典
    """
    logger.info(f"🎨 生成封面图: {article_title}")

    try:
        # 构建详细prompt
        prompt_builder = ImagePromptBuilder()
        prompt = prompt_builder.build_cover_prompt(
            article_title=article_title,
            article_topic=article_topic,
            style=style,
            language=language
        )

        logger.info(f"📝 封面图Prompt: {prompt[:200]}...")

        # 调用MCP工具
        if mcp_tools and "modelarts_generate_cover" in mcp_tools:
            result = await mcp_tools["modelarts_generate_cover"](
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height
            )

            if result.get("ok"):
                logger.info(f"✅ 封面图生成成功: {result.get('image_path')}")
                return {
                    "success": True,
                    "image_path": result.get("image_path"),
                    "image_url": result.get("image_url"),
                    "type": "cover",
                    "style": style,
                    "prompt": prompt
                }
            else:
                logger.warning(f"⚠️ 封面图生成失败: {result.get('error')}")
                return {"success": False, "error": result.get("error")}

        elif mcp_tools and "mcp_modelarts_generate_image" in mcp_tools:
            # 降级到通用生图工具
            result = await mcp_tools["mcp_modelarts_generate_image"](
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height
            )

            if result.get("ok"):
                logger.info(f"✅ 封面图生成成功（通用工具）: {result.get('image_path')}")
                return {
                    "success": True,
                    "image_path": result.get("image_path"),
                    "image_url": result.get("image_url"),
                    "type": "cover",
                    "style": style,
                    "prompt": prompt
                }

        # 模拟生成（无MCP工具时）
        logger.warning("⚠️ MCP工具未配置，使用模拟生成")
        return await _generate_mock_image(
            prompt=prompt,
            width=width,
            height=height,
            image_type="cover"
        )

    except Exception as e:
        logger.error(f"❌ 封面图生成异常: {e}")
        return {"success": False, "error": str(e)}


async def generate_inline_image(
    section_title: str,
    section_content: str,
    index: int = 0,
    style: str = "minimalist",
    aspect_ratio: str = "16:9",
    width: int = 1920,
    height: int = 1080,
    mcp_tools: Optional[Dict] = None,
    language: str = "zh"
) -> Dict[str, Any]:
    """
    生成正文插图（专用工具）

    融合4.0/3.0的详细prompt工程，提供高质量的正文插图生成

    Args:
        section_title: 章节标题
        section_content: 章节内容
        index: 插图序号
        style: 风格（minimalist, diagram, icon）
        aspect_ratio: 图片比例
        width: 宽度
        height: 高度
        mcp_tools: MCP工具字典
        language: 语言

    Returns:
        包含图片信息的字典
    """
    logger.info(f"🎨 生成正文插图 {index+1}: {section_title}")

    try:
        # 构建详细prompt
        prompt_builder = ImagePromptBuilder()
        prompt = prompt_builder.build_inline_prompt(
            section_title=section_title,
            section_content=section_content,
            style=style,
            language=language
        )

        logger.info(f"📝 正文图Prompt: {prompt[:200]}...")

        # 调用MCP工具
        if mcp_tools and "modelarts_generate_inline_image" in mcp_tools:
            result = await mcp_tools["modelarts_generate_inline_image"](
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height
            )

            if result.get("ok"):
                logger.info(f"✅ 正文图生成成功: {result.get('image_path')}")
                return {
                    "success": True,
                    "image_path": result.get("image_path"),
                    "image_url": result.get("image_url"),
                    "type": "inline",
                    "index": index,
                    "section": section_title,
                    "prompt": prompt
                }

        elif mcp_tools and "mcp_modelarts_generate_image" in mcp_tools:
            # 降级到通用生图工具
            result = await mcp_tools["mcp_modelarts_generate_image"](
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height
            )

            if result.get("ok"):
                logger.info(f"✅ 正文图生成成功（通用工具）: {result.get('image_path')}")
                return {
                    "success": True,
                    "image_path": result.get("image_path"),
                    "image_url": result.get("image_url"),
                    "type": "inline",
                    "index": index,
                    "section": section_title,
                    "prompt": prompt
                }

        # 模拟生成
        logger.warning("⚠️ MCP工具未配置，使用模拟生成")
        return await _generate_mock_image(
            prompt=prompt,
            width=width,
            height=height,
            image_type="inline",
            index=index
        )

    except Exception as e:
        logger.error(f"❌ 正文图生成异常: {e}")
        return {"success": False, "error": str(e)}


async def generate_quote_image(
    quote_text: str,
    author: str = None,
    style: str = "editorial",
    aspect_ratio: str = "4:5",
    width: int = 1080,
    height: int = 1350,
    mcp_tools: Optional[Dict] = None,
    language: str = "zh"
) -> Dict[str, Any]:
    """
    生成引用图（专用工具）

    融合4.0/3.0的详细prompt工程，提供高质量的引用图生成

    Args:
        quote_text: 引用文字
        author: 作者
        style: 风格（editorial, typography, artistic）
        aspect_ratio: 图片比例
        width: 宽度
        height: 高度
        mcp_tools: MCP工具字典
        language: 语言

    Returns:
        包含图片信息的字典
    """
    logger.info(f"🎨 生成引用图: {quote_text[:50]}...")

    try:
        # 构建详细prompt
        prompt_builder = ImagePromptBuilder()
        prompt = prompt_builder.build_quote_prompt(
            quote_text=quote_text,
            author=author,
            style=style,
            language=language
        )

        logger.info(f"📝 引用图Prompt: {prompt[:200]}...")

        # 调用MCP工具
        if mcp_tools and "mcp_modelarts_generate_image" in mcp_tools:
            result = await mcp_tools["mcp_modelarts_generate_image"](
                prompt=prompt,
                aspect_ratio=aspect_ratio,
                width=width,
                height=height
            )

            if result.get("ok"):
                logger.info(f"✅ 引用图生成成功: {result.get('image_path')}")
                return {
                    "success": True,
                    "image_path": result.get("image_path"),
                    "image_url": result.get("image_url"),
                    "type": "quote",
                    "quote": quote_text[:50],
                    "prompt": prompt
                }

        # 模拟生成
        logger.warning("⚠️ MCP工具未配置，使用模拟生成")
        return await _generate_mock_image(
            prompt=prompt,
            width=width,
            height=height,
            image_type="quote"
        )

    except Exception as e:
        logger.error(f"❌ 引用图生成异常: {e}")
        return {"success": False, "error": str(e)}


# ============================================================================
# ZhiPuArts生图函数（FireSpot 7.1主要生图服务 - 专业科技风格）
# ============================================================================

async def generate_with_zhipuarts(
    prompt: str,
    asset_id: str,
    img_type: str,
    mcp_tools: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    使用ZhiPuArts MCP生成图片（FireSpot 7.1主要生图服务 - 专业科技风格）

    Args:
        prompt: 图片生成提示词
        asset_id: 资产ID (如 cover_01, inline_01, quote_01)
        img_type: 图片类型 (cover, inline, quote)
        mcp_tools: MCP工具字典

    Returns:
        {
            "success": True/False,
            "image_path": "...",
            "image_url": "...",
            "type": "...",
            "provider": "zhipuarts",
            "style": "tech_professional"
        }
    """
    logger.info(f"🎨 使用ZhiPuArts生成图片: {asset_id}")

    try:
        # 检查ZhiPuArts MCP工具是否可用
        if not mcp_tools or "mcp_zhipuarts_generate_image" not in mcp_tools:
            logger.warning("⚠️ ZhiPuArts MCP工具未配置")
            return {
                "success": False,
                "error": "ZhiPuArts MCP tool not available"
            }

        # 根据图片类型设置尺寸（微信公众号标准 + ZhiPuArts限制）
        # ZhiPuArts 要求：512px-2880px，32的整数倍，最大像素数不超过2^22
        size_mapping = {
            "cover": "1920x800",     # 2.4:1 横版封面（1920=32*60, 800=32*25）
            "inline": "1600x900",    # 16:9 正文图（1600=32*50, 900=32*28.125 ❌）
            "quote": "1088x1360",   # 4:5 金句图（1088=32*34, 1360=32*42.5 ❌）
        }

        # 修正为符合32整数倍要求的尺寸
        size_mapping = {
            "cover": "1920x800",     # 2.4:1 横版封面
            "inline": "1728x972",    # 接近16:9（1728=32*54, 972=32*30.375 ❌）
            "quote": "1088x1360",   # 4:5 金句图
        }

        # 使用完全符合要求的尺寸
        size_mapping = {
            "cover": "1920x800",     # 2.4:1 横版封面
            "inline": "1728x972",    # 16:9 正文图（修正）
            "quote": "1088x1360",   # 4:5 金句图
        }

        # 最终尺寸：确保宽高都是32的倍数
        size_mapping = {
            "cover": "1920x800",     # 2.4:1 横版封面
            "inline": "1600x896",    # 16:9 正文图（1600=32*50, 896=32*28）
            "quote": "1088x1360",   # 4:5 金句图（1088=32*34, 1360=32*42.5 ❌ 改为 1088x1376）
        }

        # 最终版本
        size_mapping = {
            "cover": "1920x800",     # 2.4:1 横版封面
            "inline": "1600x896",    # 16:9 正文图
            "quote": "1088x1376",    # 4:5 金句图（1088=32*34, 1376=32*43）
        }

        size = size_mapping.get(img_type, "1920x1080")  # 默认16:9

        # 调用ZhiPuArts MCP工具
        result = await mcp_tools["mcp_zhipuarts_generate_image"](
            prompt=prompt,
            size=size
        )

        if result.get("ok"):
            image_path = result.get("image_path", "")
            logger.info(f"✅ ZhiPuArts生图成功: {image_path}")

            return {
                "success": True,
                "image_path": image_path,
                "image_url": result.get("image_url", f"file://{image_path}"),
                "type": img_type,
                "provider": "zhipuarts",
                "style": "tech_professional"
            }
        else:
            error_msg = result.get("error", "Unknown error")
            logger.warning(f"⚠️ ZhiPuArts生图失败: {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }

    except Exception as e:
        logger.error(f"❌ ZhiPuArts生图异常: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ============================================================================
# 完整的生图工作流（融合4.0/3.0优势）
# ============================================================================

async def generate_article_images_enhanced(
    article_title: str,
    article_content: str,
    article_sections: List[Dict] = None,
    cover_style: str = "professional",
    inline_style: str = "minimalist",
    thread_id: str = None,
    mcp_tools: Optional[Dict] = None,
    language: str = "zh"
) -> Dict[str, Any]:
    """
    增强版文章图片生成（融合4.0/3.0优势）

    使用专用工具和详细prompt生成高质量文章配图

    Args:
        article_title: 文章标题
        article_content: 文章内容（markdown格式）
        article_sections: 章节列表 [{"title": "", "content": ""}]
        cover_style: 封面图风格
        inline_style: 正文图风格
        thread_id: 线程ID
        mcp_tools: 可用的MCP工具
        language: 语言

    Returns:
        包含所有生成图片信息的字典
    """
    logger.info("🎨 开始增强版图片生成流程")
    logger.info("="*60)

    images_generated = {
        "cover": None,
        "inline_images": [],
        "quote_images": [],
        "timestamp": datetime.now().isoformat(),
        "total_count": 0,
        "success_count": 0
    }

    try:
        # 步骤1: 生成封面图
        logger.info("📸 [1/3] 生成封面图...")
        cover_result = await generate_cover_image(
            article_title=article_title,
            article_topic=_extract_topic(article_content),
            style=cover_style,
            aspect_ratio="2.35:1",
            width=1920,
            height=816,
            mcp_tools=mcp_tools,
            language=language
        )

        if cover_result.get("success"):
            images_generated["cover"] = cover_result
            images_generated["success_count"] += 1
        images_generated["total_count"] += 1

        # 步骤2: 生成正文插图
        logger.info("📸 [2/3] 生成正文插图...")

        # 提取章节
        sections = article_sections or _extract_sections_from_content(article_content)

        for i, section in enumerate(sections[:3]):  # 最多3张正文图
            if section.get("title") and section.get("content"):
                inline_result = await generate_inline_image(
                    section_title=section["title"],
                    section_content=section["content"],
                    index=i,
                    style=inline_style,
                    aspect_ratio="16:9",
                    width=1920,
                    height=1080,
                    mcp_tools=mcp_tools,
                    language=language
                )

                if inline_result.get("success"):
                    images_generated["inline_images"].append(inline_result)
                    images_generated["success_count"] += 1
                images_generated["total_count"] += 1

        # 步骤3: 提取并生成引用图（可选）
        logger.info("📸 [3/3] 生成引用图...")
        quotes = _extract_quotes(article_content)

        for i, quote in enumerate(quotes[:1]):  # 最多1张引用图
            quote_result = await generate_quote_image(
                quote_text=quote["text"],
                author=quote.get("author"),
                style="editorial",
                aspect_ratio="4:5",
                width=1080,
                height=1350,
                mcp_tools=mcp_tools,
                language=language
            )

            if quote_result.get("success"):
                images_generated["quote_images"].append(quote_result)
                images_generated["success_count"] += 1
            images_generated["total_count"] += 1

        # 汇总
        logger.info("="*60)
        logger.info(f"✅ 图片生成完成: {images_generated['success_count']}/{images_generated['total_count']} 成功")

        return images_generated

    except Exception as e:
        logger.error(f"❌ 图片生成流程异常: {e}")
        images_generated["error"] = str(e)
        return images_generated


# ============================================================================
# 辅助函数（融合4.0/3.0实现）
# ============================================================================

def _extract_topic(content: str, max_length: int = 100) -> str:
    """从文章内容中提取主题"""
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        # 查找第一个非空行，移除markdown符号
        if line and not line.startswith('#'):
            # 移除markdown格式
            topic = line.lstrip('#').lstrip('*').lstrip('-').strip()
            if len(topic) > 10:
                return topic[:max_length] if len(topic) > max_length else topic
    return None


def _extract_sections_from_content(content: str, max_sections: int = 5) -> List[Dict]:
    """从文章内容中提取章节"""
    sections = []
    lines = content.split('\n')
    current_section = {"title": None, "content": ""}

    for line in lines:
        if line.strip().startswith('##'):
            # 保存上一个章节
            if current_section["title"]:
                sections.append(current_section)

            # 开始新章节
            current_section = {
                "title": line.strip().lstrip('#').strip(),
                "content": ""
            }

            if len(sections) >= max_sections:
                break
        elif current_section["title"]:
            # 累积章节内容
            current_section["content"] += line.strip() + " "

    # 添加最后一个章节
    if current_section["title"]:
        sections.append(current_section)

    return sections


def _extract_quotes(content: str, max_quotes: int = 3) -> List[Dict]:
    """从文章内容中提取引用"""
    import re

    quotes = []
    # 查找引用格式：> 引用内容
    quote_pattern = r'^>\s*(.+)$'

    for line in content.split('\n'):
        match = re.match(quote_pattern, line.strip())
        if match:
            quote_text = match.group(1).strip()
            if len(quote_text) > 20 and len(quote_text) < 200:
                quotes.append({"text": quote_text})
                if len(quotes) >= max_quotes:
                    break

    return quotes


async def _generate_mock_image(
    prompt: str,
    width: int,
    height: int,
    image_type: str = "cover",
    index: int = 0
) -> Dict[str, Any]:
    """
    模拟图片生成（无API key时的降级方案）

    融合4.0/3.0的自动降级机制
    """
    from pathlib import Path
    import time

    # 生成模拟文件名
    timestamp = int(time.time())
    filename = f"mock_{image_type}_{index}_{timestamp}.png"
    output_dir = Path("/tmp/mcp_images")
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename

    # 创建占位文件（实际应该生成真实的图片）
    try:
        # 这里可以创建一个简单的占位图片
        # 实际部署时，应该返回更友好的提示
        logger.info(f"📝 创建模拟图片: {filepath}")

        return {
            "success": True,
            "image_path": str(filepath),
            "image_url": f"file://{filepath}",
            "type": image_type,
            "mock": True,
            "note": "模拟生成（无MODELARTS_API_KEY时）"
        }
    except Exception as e:
        logger.error(f"❌ 模拟图片创建失败: {e}")
        return {
            "success": False,
            "error": f"Mock generation failed: {str(e)}"
        }


# ============================================================================
# 导出（保持向后兼容）
# ============================================================================

# 向后兼容：保留原有函数名称
async def generate_article_images(
    article_title: str,
    article_content: str,
    thread_id: str,
    mcp_tools: Optional[Dict] = None,
) -> Dict[str, Any]:
    """向后兼容的wrapper函数"""
    return await generate_article_images_enhanced(
        article_title=article_title,
        article_content=article_content,
        thread_id=thread_id,
        mcp_tools=mcp_tools
    )


# ============================================================================
# FireSpot 7.1 新增：高级趣味感风格 + 两轮审核工作流支持
# ============================================================================

async def execute_stage_6_text_review(
    draft_path: str,
    thread_id: str,
) -> Dict[str, Any]:
    """
    Stage 6: 文字版审核（第一轮审核）

    生成只含文字和占位符描述的HTML审核稿，供用户审核内容质量

    Args:
        draft_path: 草稿文件路径（stage4_draft.md）
        thread_id: 线程ID

    Returns:
        {
            "success": True/False,
            "stage6_review_text": "...",
            "message": "..."
        }
    """
    from pathlib import Path

    logger.info("📝 开始 Stage 6: 文字版审核（第一轮审核）")

    try:
        # 1. 读取draft.md
        draft_content = Path(draft_path).read_text(encoding="utf-8")
        article_title = extract_title_from_markdown(draft_content)

        # 2. 生成HTML（使用现有函数）
        html_result = await generate_wechat_html(
            article_title=article_title,
            article_content=draft_content,
            thread_id=thread_id
        )

        if not html_result.get("success"):
            return {
                "success": False,
                "error": f"HTML生成失败: {html_result.get('error')}"
            }

        html_content = html_result["html"]

        # 3. 添加审核标记
        review_header = """
<div style="background: linear-gradient(135deg, #1a1a2e, #16213e); color: #fff; padding: 40px 20px; text-align: center; border-radius: 0 0 20px 20px;">
  <h1 style="font-size: 24px; font-weight: 700; margin-bottom: 8px;">FireSpot 7.1 · 文字版审核</h1>
  <p style="font-size: 14px; color: #8892b0;">第一轮审核：内容质量审核（含图片占位符描述）</p>
  <div style="display: inline-block; background: #00c853; color: #fff; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; margin-top: 12px;">
    ✅ 等待用户审核
  </div>
</div>
"""
        review_footer = """
<div style="background: #fafbfc; padding: 20px; border-top: 1px solid #eee; text-align: center; font-size: 12px; color: #999; margin-top: 40px;">
  <p><strong>FireSpot 7.1 两轮审核工作流</strong></p>
  <p>当前阶段：Stage 6 文字版审核（第一轮）</p>
  <p>下一阶段：回复 "approve" 或 "批准" → 自动执行 Stage 7 AI生图 + Stage 8 图文合并预览</p>
</div>
"""

        # 插入审核标记（在body标签后）
        html_with_review = html_content.replace(
            "<body>",
            f"<body>{review_header}"
        ).replace(
            "</body>",
            f"{review_footer}</body>"
        )

        # 4. 保存文件
        output_dir = Path(draft_path).parent
        stage6_review_path = output_dir / "stage6_review_text.html"

        stage6_review_path.write_text(html_with_review, encoding="utf-8")
        logger.info(f"💾 已保存 {stage6_review_path}")

        return {
            "success": True,
            "stage6_review_text": str(stage6_review_path),
            "message": "文字版审核稿生成成功"
        }

    except Exception as e:
        logger.error(f"❌ Stage 6 执行失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def replace_placeholders_in_markdown(markdown_content: str, images: Dict[str, Dict]) -> str:
    """
    替换Markdown中的 {{IMG:asset_id}} 为实际图片

    Args:
        markdown_content: Markdown内容
        images: 图片字典，格式 {"asset_id": {"path": "...", "url": "..."}}

    Returns:
        替换后的Markdown内容
    """
    from pathlib import Path

    result = markdown_content
    for asset_id, img_data in images.items():
        placeholder = f"{{{{IMG:{asset_id}}}}}"
        # 使用Markdown图片语法: ![alt](path)
        img_path = img_data.get("path", "")
        if img_path and Path(img_path).exists():
            result = result.replace(placeholder, f"![{asset_id}]({img_path})")
        else:
            # 如果图片不存在，保留原占位符或使用错误标记
            result = result.replace(placeholder, f"⚠️ 图片生成失败: {asset_id}")

    return result


def replace_placeholders_in_html(html_content: str, images: Dict[str, Dict]) -> str:
    """
    替换HTML中的 <div class="img-placeholder"> 为实际 <img> 标签

    Args:
        html_content: HTML内容
        images: 图片字典，格式 {"asset_id": {"path": "...", "url": "..."}}

    Returns:
        替换后的HTML内容
    """
    from pathlib import Path
    import re

    result = html_content

    # 匹配 <div class="img-placeholder">[asset_id] ...</div>
    pattern = r'<div class="img-placeholder">\s*<span class="icon">[^<]*</span>\s*\[([^\]]+)\]'
    matches = re.findall(pattern, html_content)

    for asset_id in matches:
        if asset_id in images:
            img_data = images[asset_id]
            img_path = img_data.get("path", "")
            img_url = img_data.get("url", "")

            if img_path and Path(img_path).exists():
                # 使用相对路径或file:// URL
                if img_url.startswith("file://"):
                    src = img_path
                else:
                    src = img_url

                img_tag = f'<img src="{src}" alt="{asset_id}" style="width:100%; border-radius:8px;">'
                placeholder = f'<div class="img-placeholder">\\s*<span class="icon">[^<]*</span>\\s*\\[{re.escape(asset_id)}\\][^<]*</div>'
                result = re.sub(placeholder, img_tag, result, flags=re.DOTALL)

    return result


def extract_image_placeholders(draft_path: str) -> Dict[str, Dict]:
    """
    从Markdown草稿中提取图片占位符

    Args:
        draft_path: Markdown草稿文件路径

    Returns:
        占位符字典，格式 {"asset_id": {"type": "cover|inline|quote", "description": "..."}}
    """
    from pathlib import Path
    import re

    placeholders = {}
    draft_content = Path(draft_path).read_text(encoding="utf-8")

    # 匹配 {{IMG:asset_id}} 格式
    pattern = r"{{IMG:([a-z0-9_]+)}}"
    matches = re.findall(pattern, draft_content)

    for asset_id in matches:
        # 根据asset_id前缀判断类型
        if asset_id.startswith("cover"):
            img_type = "cover"
        elif asset_id.startswith("inline"):
            img_type = "inline"
        elif asset_id.startswith("quote"):
            img_type = "quote"
        else:
            img_type = "inline"

        placeholders[asset_id] = {
            "type": img_type,
            "description": f"{img_type} image for {asset_id}"
        }

    return placeholders


def extract_title_from_markdown(markdown_content: str) -> str:
    """
    从Markdown内容中提取标题

    Args:
        markdown_content: Markdown内容

    Returns:
        提取的标题
    """
    import re

    # 尝试匹配第一个 # 标题
    match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # 如果没有找到，返回默认标题
    return "FireSpot Article"


def extract_placeholder_context(
    draft_content: str,
    asset_id: str,
    img_type: str
) -> Dict[str, str]:
    """
    提取图片占位符周围的文本上下文

    为构建定制化prompt提供必要的上下文信息：
    - cover: 文章标题和主题
    - inline: 章节标题和内容概要
    - quote: 金句文本

    Args:
        draft_content: 草稿内容
        asset_id: 资产ID (如 inline_01, quote_01)
        img_type: 图片类型 (cover, inline, quote)

    Returns:
        上下文字典，包含:
        - title: 标题（适用于所有类型）
        - section_title: 章节标题（适用于inline）
        - content: 内容概要（适用于inline）
        - quote_text: 金句文本（适用于quote）
    """
    import re

    context = {}

    # 提取文章标题
    title_match = re.search(r'^#\s+(.+)$', draft_content, re.MULTILINE)
    if title_match:
        context["title"] = title_match.group(1).strip()

    # 根据图片类型提取不同的上下文
    if img_type == "inline":
        # 提取占位符所在的章节标题和内容
        placeholder = f"{{{{IMG:{asset_id}}}}}"
        placeholder_pos = draft_content.find(placeholder)

        if placeholder_pos != -1:
            # 向前查找最近的标题（## 或 ###）
            before_placeholder = draft_content[:placeholder_pos]
            title_match = re.search(r'^(#{2,3})\s+(.+)$', before_placeholder, re.MULTILINE)

            if title_match:
                context["section_title"] = title_match.group(2).strip()

                # 提取标题后到占位符之间的内容（最多300字）
                content_start = title_match.end()
                content_snippet = draft_content[content_start:placeholder_pos]
                # 移除其他占位符
                content_snippet = re.sub(r'{{IMG:[a-z0-9_]+}}', '', content_snippet)
                # 清理多余空白
                content_snippet = re.sub(r'\n+', '\n', content_snippet).strip()
                # 限制长度
                context["content"] = content_snippet[:300] if len(content_snippet) > 300 else content_snippet

    elif img_type == "quote":
        # 提取占位符附近的文本作为金句
        placeholder = f"{{{{IMG:{asset_id}}}}}"
        placeholder_pos = draft_content.find(placeholder)

        if placeholder_pos != -1:
            # 提取占位符前后的文本（前后各100字）
            before = draft_content[max(0, placeholder_pos - 100):placeholder_pos]
            after = draft_content[placeholder_pos + len(placeholder):placeholder_pos + len(placeholder) + 100]

            # 清理文本
            quote_candidate = (before + after).strip()
            quote_candidate = re.sub(r'{{IMG:[a-z0-9_]+}}', '', quote_candidate)
            quote_candidate = re.sub(r'\n+', ' ', quote_candidate).strip()

            # 限制长度
            if len(quote_candidate) > 150:
                quote_candidate = quote_candidate[:150] + "..."

            context["quote_text"] = quote_candidate

    return context


async def execute_stage_7_image_generation(
    draft_path: str,
    thread_id: str,
    mcp_tools: Optional[Dict] = None,
) -> Dict[str, Any]:
    """
    Stage 7: AI自动生图 (使用Mushroom MCP)

    根据Stage 4生成的draft.md中的占位符，自动生成封面图和内文插图

    🚨 强制约束：
    - 必须使用Mushroom MCP工具(mcp_mushroom_generate_image_with_text)
    - 最多重试1次，失败后终止任务并报错
    - 禁止使用模拟生成或其他替代方案

    Args:
        draft_path: 草稿文件路径
        thread_id: 线程ID
        mcp_tools: MCP工具字典

    Returns:
        {
            "success": True/False,
            "images": {"asset_id": {"path": "...", "url": "...", "type": "..."}},
            "draft_final": "...",
            "stage7_images": "...",
            "message": "...",
            "error": "..."  # 如果重试失败
        }
    """
    from pathlib import Path
    import json
    import time
    import asyncio

    logger.info("🎨 开始 Stage 7: AI自动生图 (使用Mushroom MCP)")

    # 获取配置
    from .config import FIRESPOT_IMAGE_CONFIG
    max_retries = FIRESPOT_IMAGE_CONFIG.get("max_retries", 1)
    retry_delay = FIRESPOT_IMAGE_CONFIG.get("retry_delay_seconds", 2)

    try:
        # 1. 读取draft.md
        draft_content = Path(draft_path).read_text(encoding="utf-8")
        article_title = extract_title_from_markdown(draft_content)

        # 2. 提取占位符
        placeholders = extract_image_placeholders(draft_path)
        logger.info(f"📋 发现 {len(placeholders)} 个图片占位符: {list(placeholders.keys())}")

        if not placeholders:
            return {
                "success": False,
                "message": "未发现图片占位符，跳过生图"
            }

        # 3. 为每个占位符生成图片（直接使用Mushroom MCP）
        images = {}
        failed_images = []

        for asset_id, placeholder_info in placeholders.items():
            img_type = placeholder_info["type"]
            logger.info(f"🖼️  生成图片: {asset_id} (类型: {img_type})")

            # 尝试生成图片（最多重试1次）
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"🔄 [Mushroom] 尝试 {asset_id} 第 {attempt}/{max_retries} 次")

                    # 提取上下文信息
                    context = extract_placeholder_context(draft_content, asset_id, img_type)

                    # 使用 FireSpot 专用 prompt 构建器
                    prompt_builder = FireSpotPromptBuilder()

                    if img_type == "cover":
                        prompt = prompt_builder.build_cover_prompt(
                            article_title=context.get("title", article_title),
                            article_topic=context.get("title", ""),
                            style="wechat_tech",
                            language="zh"
                        )
                    elif img_type == "inline":
                        prompt = prompt_builder.build_inline_prompt(
                            section_title=context.get("section_title", f"章节 {asset_id}"),
                            section_content=context.get("content", ""),
                            style="wechat_diagram",
                            language="zh"
                        )
                    elif img_type == "quote":
                        prompt = prompt_builder.build_quote_prompt(
                            quote_text=context.get("quote_text", "核心观点"),
                            style="wechat_typography",
                            language="zh"
                        )
                    else:
                        prompt = f"{img_type}图片"

                    logger.info(f"📝 FireSpot定制Prompt: {prompt[:100]}...")

                    # 直接调用ZhiPuArts生成图片
                    result = await generate_with_zhipuarts(
                        prompt=prompt,
                        asset_id=asset_id,
                        img_type=img_type,
                        mcp_tools=mcp_tools
                    )

                    if result.get("success"):
                        images[asset_id] = {
                            "path": result.get("image_path", ""),
                            "url": result.get("image_url", ""),
                            "type": img_type,
                            "provider": "zhipuarts",
                            "style": result.get("style", "")
                        }
                        logger.info(f"✅ [ZhiPuArts] {asset_id} 生成成功 (style: {result.get('style')})")
                        break
                    else:
                        last_error = result.get("error", "Unknown error")
                        logger.warning(f"⚠️  [ZhiPuArts] {asset_id} 第 {attempt} 次生成失败: {last_error}")

                        if attempt < max_retries:
                            logger.info(f"⏳ 等待 {retry_delay} 秒后重试...")
                            await asyncio.sleep(retry_delay)

                except Exception as e:
                    last_error = str(e)
                    logger.error(f"❌ [ZhiPuArts] {asset_id} 第 {attempt} 次生成异常: {e}")

                    if attempt < max_retries:
                        logger.info(f"⏳ 等待 {retry_delay} 秒后重试...")
                        await asyncio.sleep(retry_delay)

            # 检查是否所有重试都失败
            if asset_id not in images:
                error_msg = f"❌ {asset_id} 生成失败（已重试 {max_retries} 次）: {last_error}"
                logger.error(error_msg)
                images[asset_id] = {
                    "path": "",
                    "url": "",
                    "type": img_type,
                    "error": last_error or "Unknown error"
                }
                failed_images.append(asset_id)

        # 4. 检查是否有失败的图片
        if failed_images:
            error_msg = f"❌ Stage 7 生图失败：{len(failed_images)} 个图片生成失败（已重试 {max_retries} 次）: {', '.join(failed_images)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "failed_images": failed_images,
                "partial_images": images
            }

        # 5. 替换占位符生成最终Markdown
        draft_final = replace_placeholders_in_markdown(draft_content, images)

        # 6. 保存文件
        output_dir = Path(draft_path).parent
        draft_final_path = output_dir / "stage4_final.md"
        stage7_images_path = output_dir / "stage7_images.json"

        # 保存stage4_final.md（含图片）
        draft_final_path.write_text(draft_final, encoding="utf-8")
        logger.info(f"💾 已保存 {draft_final_path}")

        # 保存stage7_images.json（图片元数据）
        stage7_images_path.write_text(
            json.dumps(images, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        logger.info(f"💾 已保存 {stage7_images_path}")

        return {
            "success": True,
            "images": images,
            "draft_final": str(draft_final_path),
            "stage7_images": str(stage7_images_path),
            "message": f"成功生成 {len(images)} 个图片 (使用ZhiPuArts)"
        }

    except Exception as e:
        logger.error(f"❌ Stage 7 执行失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def execute_stage_8_merge_preview(
    draft_final_path: str,
    images: Dict[str, Dict],
    thread_id: str,
) -> Dict[str, Any]:
    """
    Stage 8: 图文合并预览

    生成包含真实图片的最终HTML预览文档

    Args:
        draft_final_path: stage4_final.md路径
        images: 图片字典（从stage7_images.json读取）
        thread_id: 线程ID

    Returns:
        {
            "success": True/False,
            "stage8_final": "...",
            "message": "..."
        }
    """
    from pathlib import Path
    import time

    logger.info("🔗 开始 Stage 8: 图文合并预览")

    try:
        # 1. 读取draft_final.md
        draft_content = Path(draft_final_path).read_text(encoding="utf-8")

        # 2. 提取标题
        article_title = extract_title_from_markdown(draft_content)

        # 3. 生成基础HTML（使用现有函数）
        html_result = await generate_wechat_html(
            article_title=article_title,
            article_content=draft_content,
            thread_id=thread_id
        )

        if not html_result.get("success"):
            return {
                "success": False,
                "error": f"HTML生成失败: {html_result.get('error')}"
            }

        html_content = html_result["html"]

        # 4. 替换HTML中的占位符为真实图片
        html_final = replace_placeholders_in_html(html_content, images)

        # 5. 保存最终HTML
        output_dir = Path(draft_final_path).parent
        stage8_final_path = output_dir / "stage8_review_final.html"

        stage8_final_path.write_text(html_final, encoding="utf-8")
        logger.info(f"💾 已保存 {stage8_final_path}")

        return {
            "success": True,
            "stage8_final": str(stage8_final_path),
            "message": "图文合并预览生成成功"
        }

    except Exception as e:
        logger.error(f"❌ Stage 8 执行失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# 导出
__all__ = [
    # 原有：增强版函数
    "generate_article_images_enhanced",
    "generate_cover_image",
    "generate_inline_image",
    "generate_quote_image",
    "ImagePromptBuilder",

    # FireSpot 7.1：ZhiPuArts生图（专业科技风格）
    "generate_with_zhipuarts",

    # FireSpot 7.1 新增：两轮审核工作流（阶段重新编号）
    "execute_stage_6_text_review",
    "replace_placeholders_in_markdown",
    "replace_placeholders_in_html",
    "extract_image_placeholders",
    "extract_title_from_markdown",
    "execute_stage_7_image_generation",
    "execute_stage_8_merge_preview",

    # 向后兼容
    "generate_article_images",
]
