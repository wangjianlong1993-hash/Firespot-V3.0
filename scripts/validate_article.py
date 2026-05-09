#!/usr/bin/env python3
"""
FireSpot Article Validation Script
===================================
阶段5合规校验脚本 - 检查文章质量、字数、图片锚点、禁用句式等

Usage:
    python validate_article.py \
        --draft /mnt/user-data/outputs/stage4_draft.md \
        --article /mnt/user-data/workspace/stage4_article.json \
        --output /mnt/user-data/workspace/stage5_validation.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any


def validate_word_count(content: str, main_body: str) -> Dict[str, Any]:
    """验证字数"""
    word_count = len(main_body)
    full_word_count = len(content)

    issues = []
    score = 100

    if word_count < 800:
        issues.append({
            "level": "error",
            "category": "字数不足",
            "msg": f"正文字数不足：{word_count}字（最低800字）",
            "suggestion": "建议增加论证"
        })
        score -= 20
    elif word_count > 2000:
        issues.append({
            "level": "warning",
            "category": "字数偏多",
            "msg": f"字数偏多：{word_count}字（建议≤2000字）",
            "suggestion": "考虑精简，突出核心观点"
        })
        score -= 5

    return {
        "word_count": word_count,
        "full_word_count": full_word_count,
        "issues": issues,
        "score_impact": 20 if word_count < 800 else (5 if word_count > 2000 else 0)
    }


def validate_forbidden_phrases(content: str) -> List[Dict[str, Any]]:
    """检查禁用句式"""
    forbidden_patterns = [
        (r"大家好，今天给大家分享", "陈词滥调的开场白"),
        (r"首先.*?其次.*?最后", "机械的过渡词"),
        (r"相信很多小伙伴", "套话表达"),
        (r"话不多说，直接上干货", "网络用语"),
        (r"让我们一起来看看", "无意义的过渡"),
        (r"众所周知", "缺乏具体性"),
        (r"毋庸置疑", "缺乏论证")
    ]

    issues = []
    score_impact = 0

    for pattern, description in forbidden_patterns:
        if re.search(pattern, content):
            count = len(re.findall(pattern, content))
            issues.append({
                "level": "warning",
                "category": "禁用句式",
                "msg": f"发现{description}（出现{count}次）",
                "suggestion": "替换为更具体的表达"
            })
            score_impact += 5 * count

    return issues


def validate_image_anchors(content: str, images: List[Dict]) -> Dict[str, Any]:
    """验证图片锚点"""
    issues = []
    score_impact = 0

    # 检查markdown中的图片锚点
    image_tokens = re.findall(r'\{\{IMG:([a-zA-Z0-9_-]+)\}\}', content)

    if len(image_tokens) == 0:
        issues.append({
            "level": "error",
            "category": "缺少图片锚点",
            "msg": "未发现图片锚点",
            "suggestion": "至少插入 cover 和 2-3 个正文图片锚点"
        })
        score_impact += 15
        return {"anchors": image_tokens, "issues": issues, "score_impact": score_impact}

    # 检查资产列表
    asset_ids = [img.get('asset_id') for img in images if img.get('asset_id')]
    unique_asset_ids = set(asset_ids)

    if len(asset_ids) != len(unique_asset_ids):
        issues.append({
            "level": "error",
            "category": "资产重复",
            "msg": "stage4_article.json 中存在重复 asset_id",
            "suggestion": "确保每张图使用唯一 asset_id"
        })
        score_impact += 15

    if 'cover_01' not in asset_ids:
        issues.append({
            "level": "error",
            "category": "缺少封面资产",
            "msg": "stage4_article.json 未包含 cover_01",
            "suggestion": "必须在 publishing_plan 中保留封面图资产"
        })
        score_impact += 15

    # 检查锚点和资产是否匹配
    missing_tokens = [token for token in image_tokens if token not in unique_asset_ids]
    if missing_tokens:
        issues.append({
            "level": "error",
            "category": "锚点未定义",
            "msg": f"以下锚点未在 stage4_article.json 中声明：{', '.join(missing_tokens)}",
            "suggestion": "让 markdown 中的锚点与 images[] 一一对应"
        })
        score_impact += 15

    # 检查正文配图数量
    inline_count = len([token for token in image_tokens if token.startswith('inline_')])
    if inline_count < 2:
        issues.append({
            "level": "warning",
            "category": "正文配图不足",
            "msg": "正文配图少于2张",
            "suggestion": "建议至少保留2-3张正文配图"
        })
        score_impact += 5

    # 检查金句图
    if 'quote_01' not in image_tokens:
        issues.append({
            "level": "info",
            "category": "金句图缺失",
            "msg": "未发现 quote_01 锚点",
            "suggestion": "建议保留1张金句图强化传播"
        })

    return {
        "anchors": image_tokens,
        "assets": asset_ids,
        "issues": issues,
        "score_impact": score_impact
    }


def validate_paragraph_structure(content: str, main_body: str) -> Dict[str, Any]:
    """验证段落结构"""
    issues = []

    paragraphs = [p.strip() for p in main_body.split('\n\n') if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p) > 300]

    if len(long_paragraphs) > 3:
        issues.append({
            "level": "info",
            "category": "段落节奏",
            "msg": f"{len(long_paragraphs)}个长段落",
            "suggestion": "建议拆分"
        })

    headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)

    if title_match and len(title_match.group(1)) > 64:
        issues.append({
            "level": "warning",
            "category": "标题过长",
            "msg": f"标题：{len(title_match.group(1))}字",
            "suggestion": "精简标题"
        })

    return {
        "paragraph_count": len(paragraphs),
        "heading_count": len(headings),
        "issues": issues
    }


def main():
    parser = argparse.ArgumentParser(description="FireSpot Article Validation")
    parser.add_argument("--draft", required=True, help="Path to stage4_draft.md")
    parser.add_argument("--article", required=True, help="Path to stage4_article.json")
    parser.add_argument("--output", required=True, help="Path to save validation result")

    args = parser.parse_args()

    # 读取文件
    draft_path = Path(args.draft)
    article_path = Path(args.article)

    if not draft_path.exists():
        print(f"Error: Draft file not found: {args.draft}", file=sys.stderr)
        sys.exit(1)

    if not article_path.exists():
        print(f"Error: Article JSON file not found: {args.article}", file=sys.stderr)
        sys.exit(1)

    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()

    with open(article_path, 'r', encoding='utf-8') as f:
        article_meta = json.load(f)

    # 分离正文和元数据
    parts = content.split('---')
    main_body = max(parts, key=len)

    # 执行各项验证
    score = 100
    all_issues = []
    all_warnings = []

    # 字数验证
    word_result = validate_word_count(content, main_body)
    score -= word_result['score_impact']
    all_issues.extend([i for i in word_result['issues'] if i['level'] == 'error'])
    all_warnings.extend([i for i in word_result['issues'] if i['level'] in ['warning', 'info']])

    # 禁用句式验证
    phrase_issues = validate_forbidden_phrases(content)
    score -= sum(5 for i in phrase_issues if i['level'] == 'warning')
    all_warnings.extend(phrase_issues)

    # 图片锚点验证
    image_result = validate_image_anchors(content, article_meta.get('images', []))
    score -= image_result['score_impact']
    all_issues.extend([i for i in image_result['issues'] if i['level'] == 'error'])
    all_warnings.extend([i for i in image_result['issues'] if i['level'] in ['warning', 'info']])

    # 段落结构验证
    structure_result = validate_paragraph_structure(content, main_body)
    all_warnings.extend(structure_result['issues'])

    # 构建结果
    result = {
        "score": max(0, score),
        "word_count": word_result['word_count'],
        "full_word_count": word_result['full_word_count'],
        "paragraph_count": structure_result['paragraph_count'],
        "heading_count": structure_result['heading_count'],
        "image_token_count": len(image_result['anchors']),
        "asset_count": len(image_result['assets']),
        "issues": all_issues,
        "warnings": all_warnings,
        "status": "pass" if score >= 80 and len([i for i in all_issues if i['level'] == 'error']) == 0 else "review"
    }

    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 输出摘要
    print(f"[FIRESPOT | 阶段5完成] 合规校验")
    print(f"✅ 综合评分：{result['score']}/100")
    print(f"✅ 字数：{result['word_count']}字")
    print(f"✅ 图片锚点：{result['image_token_count']}个")
    print(f"✅ 图片资产：{result['asset_count']}个")
    print(f"✅ 问题数：{len(result['issues'])}个")
    print(f"✅ 警告数：{len(result['warnings'])}个")
    print(f"✅ 校验文件：{args.output}")

    # 如果有严重问题，返回非零退出码
    if result['status'] == 'review':
        sys.exit(1)


if __name__ == "__main__":
    main()
