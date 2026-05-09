# 图片资产规划规范

## 概述

FireSpot 的图片资产系统支持灵活的图片来源策略和完整的创作工作流。

## 图片类型和角色

### 1. 封面图 (cover)

**用途**：文章封面，显示在公众号列表和分享卡片

**规格**：
- 尺寸比例：2.35:1
- 默认分辨率：1920x816
- 上传策略：`thumb`（封面图）
- 是否必需：是

**设计要求**：
- 包含文章标题文字
- 使用专业、现代的视觉风格
- 蓝色/紫色/深色主题
- 中心构图，清晰的焦点

**asset_id 格式**：`cover_01`

### 2. 正文配图 (inline)

**用途**：文章内部章节配图，帮助读者理解内容

**规格**：
- 尺寸比例：16:9
- 默认分辨率：1920x1080
- 上传策略：`article_image`（正文图片）
- 建议数量：2-3张

**设计要求**：
- 极简主义风格
- 与章节内容相关
- 专业配色方案
- 清晰不杂乱

**asset_id 格式**：`inline_01`, `inline_02`, `inline_03`

### 3. 金句图 (quote)

**用途**：强化核心观点，便于传播分享

**规格**：
- 尺寸比例：4:5
- 默认分辨率：1080x1350
- 上传策略：`article_image`
- 建议数量：1张

**设计要求**：
- 编辑设计风格，以排版为核心
- 高对比度文字
- 柔和渐变背景
- 充足的留白

**asset_id 格式**：`quote_01`

## 图片来源策略

FireSpot 支持三种图片来源，按优先级排序：

### 1. user_provided（用户上传）

**优先级**：最高

**使用场景**：
- 用户已经准备好图片
- 需要使用特定品牌素材
- 真实照片截图

**配置方式**：
```json
{
  "source_type": "user_provided",
  "source_ref": "/path/to/image.png"  // 或 base64 数据
}
```

### 2. search（网络搜索）

**优先级**：中

**使用场景**：
- 引用真实世界图片
- 人物照片、产品图
- 地点、新闻现场
- 官方海报、截图

**配置方式**：
```json
{
  "source_type": "search",
  "source_ref": "搜索关键词"
}
```

**注意**：需确保运行环境具备搜索和下载图片能力。

### 3. generate（AI生成）

**优先级**：低

**使用场景**：
- 抽象概念可视化
- 封面氛围图
- 金句图
- 无合适真实图片时

**配置方式**：
```json
{
  "source_type": "generate",
  "prompt": "Create a professional illustration about AI ethics",
  "aspect_ratio": "16:9"
}
```

## Prompt 模板

### 封面图 Prompt 模板

**英文版**：
```
Create a professional, modern cover image for a tech article about AI.
Title: {article_title}
Style: Clean, minimalist, tech-focused
Elements: Abstract AI/technology symbols
Colors: Blue, purple, or dark theme
Aspect ratio: {aspect_ratio}
Composition: Centralized composition with clear focal point
Mood: Professional, innovative, trustworthy
```

**中文版**：
```
创建一张专业、现代的科技文章封面图。
文章标题：{article_title}
风格：简洁、极简主义、科技感
元素：抽象AI/技术符号
配色：蓝色、紫色或深色主题
比例：{aspect_ratio}
构图：中心构图，清晰的焦点
氛围：专业、创新、可信赖
```

### 正文图 Prompt 模板

**英文版**：
```
Create a simple illustration for a tech article section.
Section: {section_title}
Content: {section_content}
Style: Minimalist, professional diagram or icon
Colors: Complementary to cover, professional palette
Aspect ratio: {aspect_ratio}
Purpose: Visual aid to help readers understand the concept
Detail level: Clean and uncluttered, focus on clarity
```

**中文版**：
```
为科技文章的章节创建简单的插图。
章节标题：{section_title}
内容概要：{section_content}
风格：极简主义、专业图表或图标
配色：与封面图协调的专业配色方案
比例：{aspect_ratio}
目的：帮助读者理解概念的可视化辅助
细节：清晰不杂乱，重点突出
```

### 金句图 Prompt 模板

**英文版**：
```
Create an elegant quote image for a tech article.
Quote text: {quote_text}
Author: {author}
Style: Editorial design, typography-focused
Colors: Subtle gradient background, high contrast text
Aspect ratio: {aspect_ratio}
Layout: Centered text with generous white space
Mood: Insightful, inspiring, memorable
```

**中文版**：
```
为科技文章创建优雅的引用图。
引用文字：{quote_text}
作者：{author}
风格：编辑设计，以排版为核心
配色：柔和渐变背景，高对比度文字
比例：{aspect_ratio}
布局：居中文字，充足的留白
氛围：有洞察力、启发人心、印象深刻
```

## 图片锚点规范

### Markdown 中的锚点格式

```
{{IMG:asset_id}}
```

### 插入位置

- **封面图**：文章最前面，紧跟标题后
- **正文图**：对应章节内容后
- **金句图**：核心金句或结论处

### 示例

```markdown
# 文章标题

{{IMG:cover_01}}

## 开篇

文章开篇内容...

{{IMG:inline_01}}

## 第一部分

第一部分内容...

{{IMG:inline_02}}

## 第二部分

第二部分内容...

{{IMG:quote_01}}

## 结语

结语内容...
```

## MCP 工具使用

### 1. ZhipuArts 图片生成

```python
mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
    "prompt": "Create a professional illustration...",
    "aspect_ratio": "16:9",
    "output_path": "/mnt/user-data/outputs/inline_01.png"
})
```

### 2. 微信图片准备

```python
mcp.call_tool("wechat-publisher", "mcp_wechat_prepare_image", {
    "source_type": "generate",  # 或 "search", "user_provided"
    "usage": "article_image",    # 或 "thumb"
    "prompt": "Create...",
    "aspect_ratio": "16:9",
    "output_path": "/mnt/user-data/outputs/inline_01.png"
})
```

## 完整配置示例

```json
{
  "publishing_plan": {
    "cover": {
      "asset_id": "cover_01",
      "role": "cover",
      "insert_anchor": "article_cover",
      "description": "AI伦理主题封面图，包含抽象AI符号和文章标题",
      "style": "科技感，蓝色渐变，极简主义",
      "aspect_ratio": "2.35:1",
      "required": true,
      "upload_policy": "thumb",
      "source_type": "generate",
      "source_ref": "",
      "prompt": "Create a professional cover image about AI ethics with abstract technology symbols, blue gradient background, minimalist style, 2.35:1 aspect ratio"
    },
    "images": [
      {
        "asset_id": "inline_01",
        "role": "inline",
        "insert_anchor": "after_section_1",
        "description": "第一部分配图：AI决策流程图",
        "style": "扁平插画，专业图表",
        "aspect_ratio": "16:9",
        "required": true,
        "upload_policy": "article_image",
        "source_type": "generate",
        "source_ref": "",
        "prompt": "Create a simple diagram showing AI decision-making process, minimalist style, professional colors, 16:9 aspect ratio"
      },
      {
        "asset_id": "inline_02",
        "role": "inline",
        "insert_anchor": "after_section_2",
        "description": "第二部分配图：人机协作场景",
        "style": "实景照片风格",
        "aspect_ratio": "16:9",
        "required": true,
        "upload_policy": "article_image",
        "source_type": "search",
        "source_ref": "human AI collaboration",
        "prompt": ""
      },
      {
        "asset_id": "quote_01",
        "role": "quote",
        "insert_anchor": "quote_block_1",
        "description": "金句图：真正的智慧不在于完美决策",
        "style": "文字海报，极简设计",
        "aspect_ratio": "4:5",
        "required": true,
        "upload_policy": "article_image",
        "source_type": "generate",
        "source_ref": "",
        "prompt": "Create an elegant quote image with text '真正的智慧不在于完美决策，而在于从错误中学习', typography-focused design, subtle gradient background, high contrast text, 4:5 aspect ratio, generous white space"
      }
    ]
  }
}
```
