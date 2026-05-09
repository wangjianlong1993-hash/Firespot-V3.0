#!/usr/bin/env python3
"""
FireSpot Image Preparation Script
=================================
阶段7图片准备脚本 - 按三通道策略准备图片资产

支持三种图片来源：
- generate: AI生成图片（使用 ModelArts MCP）
- search: 网络搜索图片
- user_provided: 用户上传图片

Usage:
    python prepare_images.py \
        --article /mnt/user-data/workspace/stage4_article.json \
        --output /mnt/user-data/workspace/stage7_uploaded_assets.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List


def prepare_image(asset: Dict, mcp) -> Dict[str, Any]:
    """
    准备单个图片资产

    Args:
        asset: 图片资产配置
        mcp: MCP 工具接口

    Returns:
        上传结果字典
    """
    source_type = asset.get("source_type", "generate")
    upload_policy = asset.get("upload_policy")
    usage = "thumb" if upload_policy == "thumb" else "article_image"

    params = {
        "source_type": source_type,
        "usage": usage,
    }

    # 根据来源类型构建参数
    if source_type == "generate":
        params.update({
            "prompt": asset["prompt"],
            "aspect_ratio": asset.get("aspect_ratio", "16:9"),
            "output_path": f"/mnt/user-data/outputs/{asset['asset_id']}.png"
        })

    elif source_type == "search":
        image_url = asset.get("image_url") or asset.get("source_ref")
        if not image_url:
            raise ValueError(f"search 图片缺少 image_url/source_ref: {asset['asset_id']}")
        params["image_url"] = image_url

    elif source_type == "user_provided":
        if asset.get("image_url"):
            params["image_url"] = asset["image_url"]
        elif asset.get("image_base64"):
            params["image_base64"] = asset["image_base64"]
            params["content_type"] = asset.get("content_type", "image/png")
        elif asset.get("source_ref"):
            params["image_base64"] = asset["source_ref"]
            params["content_type"] = asset.get("content_type", "image/png")
        else:
            raise ValueError(f"user_provided 图片缺少可用来源: {asset['asset_id']}")
    else:
        raise ValueError(f"不支持的 source_type: {source_type}")

    # 调用 MCP 工具
    result = mcp.call_tool("wechat-publisher", "mcp_wechat_prepare_image", params)

    if not result.get("ok"):
        raise ValueError(f"图片准备失败: {asset['asset_id']} -> {result}")

    return result


def main():
    parser = argparse.ArgumentParser(description="FireSpot Image Preparation")
    parser.add_argument(
        "--article",
        required=True,
        help="Path to stage4_article.json"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to save uploaded assets JSON"
    )

    args = parser.parse_args()

    # 读取文章配置
    article_path = Path(args.article)
    if not article_path.exists():
        print(f"Error: Article file not found: {args.article}", file=sys.stderr)
        sys.exit(1)

    with open(article_path, 'r', encoding='utf-8') as f:
        article_meta = json.load(f)

    images = article_meta.get("images", [])
    if not images:
        print("Error: No images found in article metadata", file=sys.stderr)
        sys.exit(1)

    # 注意：此脚本需要 MCP 上下文才能运行
    # 实际使用时会在 Agent 上下文中执行
    print(f"[FIRESPOT] 图片准备脚本已加载")
    print(f"✅ 待准备图片数：{len(images)}")
    print(f"⚠️  此脚本需要在 MCP 上下文中执行")
    print(f"⚠️  请通过 Agent 调用，不要直接运行")


if __name__ == "__main__":
    main()
