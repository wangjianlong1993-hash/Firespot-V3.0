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

class ImagePromptBuilder:
    """
    图片生成Prompt构建器

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


# 导出
__all__ = [
    # 新增：增强版函数
    "generate_article_images_enhanced",
    "generate_cover_image",
    "generate_inline_image",
    "generate_quote_image",
    "ImagePromptBuilder",

    # 向后兼容
    "generate_article_images",
]
