#!/usr/bin/env python3
"""
FireSpot Review HTML Generator
===============================
阶段6审核HTML生成脚本 - 将Markdown转换为浏览器预览版本

Usage:
    python generate_review_html.py \
        --draft /mnt/user-data/outputs/stage4_draft.md \
        --article /mnt/user-data/workspace/stage4_article.json \
        --validation /mnt/user-data/workspace/stage5_validation.json \
        --output /mnt/user-data/outputs/stage6_review.html
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Any

try:
    import markdown
except ImportError:
    print("Error: markdown module required. Install with: pip install markdown", file=sys.stderr)
    sys.exit(1)


def load_article_data(draft_path: Path, article_path: Path, validation_path: Path) -> tuple:
    """加载文章数据"""
    with open(draft_path, 'r', encoding='utf-8') as f:
        article = f.read()

    with open(article_path, 'r', encoding='utf-8') as f:
        article_meta = json.load(f)

    with open(validation_path, 'r', encoding='utf-8') as f:
        validation = json.load(f)

    return article, article_meta, validation


def extract_title(article: str, article_meta: Dict) -> str:
    """提取文章标题"""
    # 优先使用元数据中的标题
    title = article_meta.get("title")
    if title:
        return title

    # 从markdown中提取
    match = re.search(r'^#\s+(.+)$', article, re.MULTILINE)
    if match:
        return match.group(1)

    return "未命名文章"


def generate_html_body(article: str, article_meta: Dict) -> str:
    """生成HTML正文"""
    markdown_body = article_meta.get("markdown_body", article)
    html_body = markdown.markdown(markdown_body)
    # 将h1转换为h2（因为外面已经有标题了）
    html_body = html_body.replace("<h1>", "<h2>").replace("</h1>", "</h2>")
    return html_body


def build_review_html(title: str, html_body: str, article_meta: Dict, validation: Dict) -> str:
    """构建审核HTML"""
    review_meta = {
        "title": title,
        "summary": "阶段6审核稿已生成，请先审核 HTML 再决定是否发布。",
        "score": validation.get("score"),
        "word_count": validation.get("word_count"),
        "issue_count": len(validation.get("issues", [])),
        "warning_count": len(validation.get("warnings", [])),
        "asset_count": len(article_meta.get("images", [])),
        "validation_status": validation.get("status"),
    }

    review_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} - FireSpot 审核稿</title>
    <style>
      body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; background: #f5f7fb; color: #1f2937; }}
      .wrap {{ max-width: 900px; margin: 0 auto; padding: 32px 20px 64px; }}
      .card {{ background: #fff; border-radius: 16px; box-shadow: 0 8px 30px rgba(15, 23, 42, 0.08); padding: 28px; margin-bottom: 24px; }}
      h1 {{ font-size: 32px; line-height: 1.25; margin: 0 0 16px; }}
      p, li {{ font-size: 16px; line-height: 1.8; }}
      img {{ max-width: 100%; height: auto; border-radius: 8px; }}
      ul {{ padding-left: 20px; }}
      .meta {{ color: #475569; }}
      .badge {{ display: inline-block; padding: 4px 10px; border-radius: 999px; background: #e0f2fe; color: #0369a1; font-size: 13px; margin-right: 8px; }}
      .content p {{ margin: 16px 0; }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <div class="card">
        <div class="meta"><span class="badge">FireSpot Stage 6</span>待审核 HTML</div>
        <h1>{title}</h1>
        <ul>
          <li><strong>合规评分：</strong>{review_meta['score']}</li>
          <li><strong>正文字数：</strong>{review_meta['word_count']}</li>
          <li><strong>问题数：</strong>{review_meta['issue_count']}</li>
          <li><strong>警告数：</strong>{review_meta['warning_count']}</li>
          <li><strong>图片资产数：</strong>{review_meta['asset_count']}</li>
          <li><strong>校验状态：</strong>{review_meta['validation_status']}</li>
        </ul>
      </div>
      <div class="card content">{html_body}</div>
    </div>
  </body>
</html>"""

    return review_html


def save_review_summary(meta: Dict, output_path: Path) -> None:
    """保存审核摘要"""
    summary_path = output_path.parent / "stage6_review_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="FireSpot Review HTML Generator")
    parser.add_argument("--draft", required=True, help="Path to stage4_draft.md")
    parser.add_argument("--article", required=True, help="Path to stage4_article.json")
    parser.add_argument("--validation", required=True, help="Path to stage5_validation.json")
    parser.add_argument("--output", required=True, help="Path to save review HTML")

    args = parser.parse_args()

    # 验证输入文件存在
    draft_path = Path(args.draft)
    article_path = Path(args.article)
    validation_path = Path(args.validation)

    for path in [draft_path, article_path, validation_path]:
        if not path.exists():
            print(f"Error: File not found: {path}", file=sys.stderr)
            sys.exit(1)

    # 加载数据
    article, article_meta, validation = load_article_data(draft_path, article_path, validation_path)

    # 生成审核HTML
    title = extract_title(article, article_meta)
    html_body = generate_html_body(article, article_meta)
    review_html = build_review_html(title, html_body, article_meta, validation)

    # 保存文件
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(review_html)

    # 保存摘要
    review_meta = {
        "title": title,
        "summary": "阶段6审核稿已生成，请先审核 HTML 再决定是否发布。",
        "score": validation.get("score"),
        "word_count": validation.get("word_count"),
        "issue_count": len(validation.get("issues", [])),
        "warning_count": len(validation.get("warnings", [])),
        "asset_count": len(article_meta.get("images", [])),
        "validation_status": validation.get("status"),
    }
    save_review_summary(review_meta, output_path)

    # 输出摘要
    print(f"[FIRESPOT | 阶段6完成] 已生成审核 HTML")
    print(f"✅ 审核HTML：{args.output}")
    print(f"✅ 摘要文件：{output_path.parent / 'stage6_review_summary.json'}")
    print(f"✅ 请等待用户回复 approve / revise / detail / cancel")


if __name__ == "__main__":
    main()
