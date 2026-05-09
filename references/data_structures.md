# FireSpot 数据结构定义

本文档定义 FireSpot 工作流中各阶段使用的数据结构。

## Stage 1: Research（阶段1研究数据）

### 文件路径
`/mnt/user-data/workspace/stage1_research.json`

### JSON Schema

```json
{
  "research_date": "2026-04-29",
  "topic": "AI与人类的本质差异",
  "direction": "从伦理学角度分析",
  "platforms": {
    "wechat_mp": {
      "source_count": 8,
      "top_articles": [
        {
          "title": "文章标题",
          "url": "https://mp.weixin.qq.com/s/xxx",
          "key_points": ["核心观点1", "观点2"],
          "data": "支撑数据",
          "engagement": "10万+阅读"
        }
      ],
      "trending_keywords": ["AI伦理", "人机关系"],
      "content_gaps": ["未被充分讨论的角度"],
      "unique_opportunities": ["差异化机会"]
    },
    "xiaohongshu": {
      "source_count": 12,
      "top_notes": [
        {
          "title": "笔记标题",
          "url": "https://xiaohongshu.com/xxx",
          "user_pain_points": ["用户痛点"],
          "engagement": "5万+点赞"
        }
      ],
      "user_demands": ["用户需求总结"],
      "content_angles": ["内容角度"]
    },
    "bilibili": {
      "source_count": 6,
      "top_videos": [
        {
          "title": "视频标题",
          "url": "https://bilibili.com/video/xxx",
          "view_count": "50万+播放",
          "key_moments": ["高光时刻/时间戳"],
          "danmaku_keywords": ["弹幕高频词"]
        }
      ],
      "up_opinions": ["UP主观点"],
      "audience_questions": ["观众疑问"]
    },
    "douyin": {
      "source_count": 0,
      "trending_hashtags": ["话题标签"],
      "viral_content": ["爆款内容特征"],
      "user_comments": ["用户评论"]
    },
    "youtube": {
      "source_count": 5,
      "top_videos": [
        {
          "title": "视频标题",
          "url": "https://youtube.com/watch?v=xxx",
          "views": "100万+观看",
          "international_angle": "国际视角"
        }
      ],
      "global_trends": ["全球趋势"]
    },
    "twitter_x": {
      "source_count": 10,
      "top_threads": [
        {
          "author": "作者",
          "url": "https://x.com/xxx/status/xxx",
          "key_arguments": ["核心论点"],
          "engagement": "5万+互动"
        }
      ],
      "debate_topics": ["争议话题"]
    },
    "tiktok": {
      "source_count": 0,
      "trending_sounds": ["热门BGM"],
      "creative_formats": ["创意形式"],
      "gen_z_perspectives": ["Z世代观点"]
    },
    "industry_reports": {
      "source_count": 3,
      "key_reports": [
        {
          "source": "报告来源",
          "url": "报告链接",
          "key_data": "关键数据",
          "insights": ["洞察"]
        }
      ]
    }
  },
  "cross_platform_insights": {
    "common_themes": ["跨平台共同主题"],
    "regional_differences": ["地域差异"],
    "demographic_preferences": ["人群偏好"],
    "content_format_trends": ["内容格式趋势"]
  },
  "strategic_recommendations": {
    "content_angle": "推荐内容角度",
    "target_audience": "目标受众",
    "differentiation": "差异化策略",
    "timing": "发布时机建议"
  }
}
```

## Stage 2: Analysis（阶段2分析数据）

### 文件路径
`/mnt/user-data/workspace/stage2_analysis.json`

### JSON Schema

```json
{
  "core_thesis": "核心主张（一句话，明确、有力、有价值）",
  "unique_angle": "与主流观点的差异化（你的独特视角）",
  "platform_insights": {
    "wechat_success_patterns": "微信公众号成功模式",
    "xiaohongshu_user_needs": "小红书用户需求",
    "video_content_gold": "视频内容金矿（B站/抖音/YouTube）",
    "international_perspectives": "国际视角差异"
  },
  "supporting_points": [
    {
      "point": "论据1：小标题",
      "evidence": "支撑数据或观点（来自研究数据）",
      "source_platform": "数据来源平台",
      "data_backing": "具体数据或案例"
    },
    {
      "point": "论据2：小标题",
      "evidence": "支撑数据或观点",
      "source_platform": "数据来源平台",
      "data_backing": "具体数据或案例"
    },
    {
      "point": "论据3：小标题",
      "evidence": "支撑数据或观点",
      "source_platform": "数据来源平台",
      "data_backing": "具体数据或案例"
    }
  ],
  "tone_style": "语气风格描述（如：理性分析中带温度，学术但不晦涩）",
  "content_structure": [
    "开篇：场景/数据引入",
    "第一部分：论点1展开",
    "第二部分：论点2展开",
    "第三部分：论点3或实践建议",
    "结语：升华主题+行动号召"
  ],
  "target_audience": "目标受众描述（基于各平台用户画像）",
  "value_proposition": "这篇文章给读者带来的价值",
  "seo_keywords": ["关键词1", "关键词2", "关键词3"],
  "viral_potential": "传播潜力分析（为什么会被转发）"
}
```

## Stage 3: Outline（阶段3框架数据）

### 文件路径
`/mnt/user-data/workspace/stage3_outline.json`

### JSON Schema

```json
{
  "title_options": [
    {
      "type": "悬念体",
      "title": "备选标题1（设置悬念，引发好奇）",
      "characteristics": "引人入胜，制造疑问"
    },
    {
      "type": "数字体",
      "title": "备选标题2（数字清单，清晰明确）",
      "characteristics": "结构清晰，实用性强"
    },
    {
      "type": "共情体",
      "title": "备选标题3（情感共鸣，贴近读者）",
      "characteristics": "情感连接，引发认同"
    }
  ],
  "recommended_title": "最推荐的标题（考虑传播性和点击率）",
  "hook": "开篇钩子（50-80字）：用场景、数据或金句切入",
  "sections": [
    {
      "section_id": "section_1",
      "heading": "小标题1：{论据1的提炼}",
      "key_point": "该段核心内容（1-2句话）",
      "word_count_target": "300-400",
      "content_elements": ["要点1", "要点2", "要点3"],
      "transition": "如何过渡到下一段",
      "image_asset_ref": "inline_01"
    },
    {
      "section_id": "section_2",
      "heading": "小标题2：{论据2的提炼}",
      "key_point": "该段核心内容（1-2句话）",
      "word_count_target": "300-400",
      "content_elements": ["要点1", "要点2", "要点3"],
      "transition": "如何过渡到下一段",
      "image_asset_ref": "inline_02"
    },
    {
      "section_id": "section_3",
      "heading": "小标题3：{论据3或实践建议}",
      "key_point": "该段核心内容（1-2句话）",
      "word_count_target": "300-400",
      "content_elements": ["要点1", "要点2", "要点3"],
      "transition": "如何过渡到结语",
      "image_asset_ref": "quote_01"
    }
  ],
  "conclusion": "结语方向（50-100字）：升华主题，给出启发性思考",
  "cta": "行动号召：引导读者互动（点赞、在看、转发、评论）",
  "estimated_word_count": "预估总字数",
  "publishing_plan": {
    "cover": {
      "asset_id": "cover_01",
      "role": "cover",
      "insert_anchor": "article_cover",
      "description": "封面图描述（主视觉+标题文字）",
      "style": "设计风格建议",
      "aspect_ratio": "2.35:1",
      "required": true,
      "upload_policy": "thumb",
      "source_type": "generate",
      "source_ref": "关键词或描述",
      "prompt": "英文提示词"
    },
    "images": [
      {
        "asset_id": "inline_01",
        "role": "inline",
        "insert_anchor": "after_section_1",
        "description": "第一段后的内容配图描述",
        "style": "扁平插画/实景照片/信息图",
        "aspect_ratio": "16:9",
        "required": true,
        "upload_policy": "article_image",
        "source_type": "search",
        "source_ref": "搜索关键词",
        "prompt": "英文提示词"
      },
      {
        "asset_id": "inline_02",
        "role": "inline",
        "insert_anchor": "after_section_2",
        "description": "第二段后的数据图或场景图描述",
        "style": "信息图表/数据可视化",
        "aspect_ratio": "16:9",
        "required": true,
        "upload_policy": "article_image",
        "source_type": "generate",
        "source_ref": "描述",
        "prompt": "英文提示词"
      },
      {
        "asset_id": "quote_01",
        "role": "quote",
        "insert_anchor": "quote_block_1",
        "description": "金句图文字内容 + 视觉设计建议",
        "style": "文字海报/极简设计",
        "aspect_ratio": "4:5",
        "required": true,
        "upload_policy": "article_image",
        "source_type": "generate",
        "source_ref": "金句文字",
        "prompt": "英文提示词"
      }
    ]
  }
}
```

## Stage 4: Article（阶段4文章数据）

### 文件路径
`/mnt/user-data/workspace/stage4_article.json`

### JSON Schema

```json
{
  "title": "推荐标题",
  "digest": "120字内摘要",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "markdown_body": "完整 markdown 正文",
  "images": [
    {
      "asset_id": "cover_01",
      "role": "cover",
      "insert_anchor": "article_cover",
      "description": "封面图描述",
      "style": "设计风格",
      "aspect_ratio": "2.35:1",
      "required": true,
      "upload_policy": "thumb",
      "source_type": "generate",
      "source_ref": "关键词或描述",
      "prompt": "英文提示词"
    }
  ]
}
```

## Stage 5: Validation（阶段5校验数据）

### 文件路径
`/mnt/user-data/workspace/stage5_validation.json`

### JSON Schema

```json
{
  "score": 85,
  "word_count": 1250,
  "full_word_count": 1350,
  "paragraph_count": 15,
  "heading_count": 4,
  "image_token_count": 4,
  "asset_count": 4,
  "issues": [
    {
      "level": "error",
      "category": "字数不足",
      "msg": "正文字数不足：750字（最低800字）",
      "suggestion": "建议增加论证"
    }
  ],
  "warnings": [
    {
      "level": "warning",
      "category": "禁用句式",
      "msg": "发现陈词滥调的开场白（出现1次）",
      "suggestion": "替换为更具体的表达"
    }
  ],
  "status": "pass"
}
```

**字段说明**：
- `score`: 综合评分（0-100）
- `status`: 校验状态（`pass` ≥80分且无error，`review` 其他情况）

## Stage 6: Review（阶段6审核数据）

### 文件路径
`/mnt/user-data/workspace/stage6_review_summary.json`

### JSON Schema

```json
{
  "title": "文章标题",
  "summary": "阶段6审核稿已生成，请先审核 HTML 再决定是否发布。",
  "score": 85,
  "word_count": 1250,
  "issue_count": 0,
  "warning_count": 2,
  "asset_count": 4,
  "validation_status": "pass"
}
```

## Stage 7: Publish（阶段7发布数据）

### 文件路径
`/mnt/user-data/workspace/stage7_publish_assets.json`

### JSON Schema

```json
{
  "title": "文章标题",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "thumb_media_id": "微信封面图media_id",
  "review_html": "/mnt/user-data/outputs/stage6_review.html",
  "uploaded_assets": {
    "cover_01": {
      "type": "thumb",
      "thumb_media_id": "xxx",
      "source_type": "generate",
      "file_path": "/mnt/user-data/outputs/cover_01.png"
    },
    "inline_01": {
      "type": "article_image",
      "url": "微信素材URL",
      "source_type": "search",
      "origin_url": "原始图片URL",
      "file_path": "/mnt/user-data/outputs/inline_01.png"
    }
  },
  "draft_result": {
    "media_id": "草稿media_id",
    "created_at": "创建时间"
  }
}
```
