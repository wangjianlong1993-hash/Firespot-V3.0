#!/usr/bin/env python3
"""
FireSpot WeChat HTML Generator
===============================
将 Markdown 转换为微信兼容的 HTML 格式

特性：
- CSS 全部转换为内联样式
- 移除微信不支持的标签
- 使用 <section> 标签包裹内容
- 可选移除元信息行

Usage:
    python generate_wechat_html.py \
        --markdown /mnt/user-data/outputs/stage4_draft.md \
        --output /mnt/user-data/outputs/stage6_wechat_draft.html
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import markdown
from ImportError:
    print("Error: markdown module required. Install with: pip install markdown", file=sys.stderr)
    sys.exit(1)


def convert_markdown_to_inline_html(markdown_content: str) -> str:
    """转换 Markdown 为内联样式的 HTML"""

    # 1. Markdown 转 HTML
    html = markdown.markdown(
        markdown_content,
        extensions=['extra', 'nl2br', 'sane_lists']
    )

    # 2. 移除不支持的标签
    # 移除 <style> 标签及其内容
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # 移除 <html>, <head>, <body> 标签（如果有）
    html = re.sub(r'</?html[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?head[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?body[^>]*>', '', html, flags=re.IGNORECASE)

    # 3. 用 <section> 标签包裹内容
    # 检查是否已经被 <section> 包裹
    if not html.strip().startswith('<section'):
        html = f'<section>{html}</section>'

    return html


def replace_image_placeholders(html: str) -> str:
    """
    处理图片占位符
    保留 {{IMG:xxx}} 格式，后续在阶段7替换
    """
    # 确保 {{IMG:xxx}} 独占一行
    html = re.sub(
        r'<p>\s*({{IMG:[^}]+}})\s*</p>',
        r'\1\n',
        html
    )
    return html


def generate_wechat_html(
    markdown_path: Path,
    output_path: Path,
    remove_meta: bool = False
) -> None:
    """生成微信兼容的 HTML"""

    # 读取 Markdown
    with open(markdown_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # 可选：移除元信息行（--- 包围的部分）
    if remove_meta:
        markdown_content = re.sub(
            r'^---\n.*?\n---\n',
            '',
            markdown_content,
            flags=re.DOTALL,
            count=1
        )

    # 转换为 HTML
    html = convert_markdown_to_inline_html(markdown_content)

    # 处理图片占位符
    html = replace_image_placeholders(html)

    # 保存文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    parser = argparse.ArgumentParser(
        description="Generate WeChat-compatible HTML from Markdown"
    )
    parser.add_argument(
        "--markdown",
        required=True,
        help="Path to markdown file (e.g., /mnt/user-data/outputs/stage4_draft.md)"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save HTML file (e.g., /mnt/user-data/outputs/stage6_wechat_draft.html)"
    )
    parser.add_argument(
        "--remove-meta",
        action="store_true",
        help="Remove metadata lines (wrapped in ---)"
    )

    args = parser.parse_args()

    # 验证输入文件
    markdown_path = Path(args.markdown)
    if not markdown_path.exists():
        print(f"Error: Markdown file not found: {args.markdown}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output)

    # 生成 HTML
    try:
        generate_wechat_html(
            markdown_path=markdown_path,
            output_path=output_path,
            remove_meta=args.remove_meta
        )
        print(f"[FIRESPOT] 微信 HTML 已生成")
        print(f"✅ 输入文件：{args.markdown}")
        print(f"✅ 输出文件：{args.output}")
        print(f"✅ 移除元信息：{'是' if args.remove_meta else '否'}")
    except Exception as e:
        print(f"Error: Failed to generate WeChat HTML: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
