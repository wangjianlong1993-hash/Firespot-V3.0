# MCP 工具使用规范

## 概述

FireSpot 在阶段8（AI自动生图）强制要求使用 ZhipuArts MCP 工具来确保图片生成的专业性和稳定性。

## 🚨 重要：阶段8强制要求

阶段8 **必须**使用以下 MCP 工具：

1. **ZhipuArts** - 智谱AI GLM-Image专业科技风格图片生成
2. **wechat-publisher** - 微信发布（阶段10）

### 禁止行为

```python
# ❌ 禁止
- 手动上传图片
- 从网络搜索图片（未通过MCP）
- 使用第三方AI生图服务
- 手动复制粘贴到微信后台
- 绕过MCP直接调用微信API
```

### 正确使用

```python
# ✅ 必须
- mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {...})
- mcp.call_tool("wechat-publisher", "mcp_wechat_prepare_image", {...})
- mcp.call_tool("wechat-publisher", "mcp_wechat_create_draft", {...})
```

---

## 🎨 ZhipuArts MCP 工具（v7.2核心）

### 工具概述

**工具名称**：`mcp_zhipuarts_generate_image`

**提供商**：智谱AI (Zhipu AI)

**模型**：GLM-Image

**特点**：
- ✅ 专业科技风格图片生成
- ✅ 专为FireSpot优化
- ✅ 稳定可靠的API服务
- ✅ 支持多种尺寸和比例
- ✅ 快速生成，高质量输出

### 1. 图片生成

**参数**：

```python
{
    "prompt": str,           # 必需，中英文提示词均可
    "size": str,            # 可选，默认"1280x720"
    "output_path": str,     # 可选，默认自动生成
}
```

**支持的size**：
- `"1280x720"` - 16:9 横版（正文图，推荐）
- `"1920x1080"` - 16:9 高清（正文图）
- `"900x383"` - 2.35:1 电影宽屏（封面图）
- `"1080x1080"` - 1:1 正方形（金句图）
- `"720x1280"` - 9:16 竖版

**示例**：

```python
# 封面图生成
result = mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
    "prompt": "A futuristic visualization of high-dimensional embedding space, dark blue-purple gradient background, glowing word nodes floating in a constellation-like network, tech editorial cover style, 900x383 pixels",
    "size": "900x383",
    "output_path": "/mnt/user-data/outputs/cover_01.png"
})

# 正文图生成
result = mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
    "prompt": "A clean data visualization showing the evolution of embedding dimensions over time, horizontal bar chart style, dark background, gradient color bars from teal to purple, 1280x720 pixels",
    "size": "1280x720",
    "output_path": "/mnt/user-data/outputs/inline_01.png"
})

# 金句图生成
result = mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
    "prompt": "A minimalist quote card with dark background, the quote 'AI不需要理解文字，只需要在高维空间里量距离' in elegant white-gold typography, premium editorial style, 1080x1080 pixels",
    "size": "1080x1080",
    "output_path": "/mnt/user-data/outputs/quote_01.png"
})
```

**返回值**：

```json
{
    "success": true,
    "image_path": "/mnt/user-data/outputs/cover_01.png",
    "image_url": "file:///mnt/user-data/outputs/cover_01.png",
    "model": "glm-image",
    "generation_time": "3.2s"
}
```

### 2. Prompt 最佳实践

#### ZhipuArts Prompt 特点

**中英文均可**：
- ✅ "创建一张关于AI伦理的专业插图，科技风格"
- ✅ "Create a professional illustration about AI ethics, tech style"
- ✅ 混合语言："A futuristic visualization of 高维嵌入空间, dark blue-purple gradient"

**包含关键元素**：
- 主题/内容
- 风格/画风（专业科技风格）
- 配色方案
- 构图/布局
- 氛围/情绪
- 尺寸规格

#### FireSpot 专用模板

**封面图模板**：
```python
cover_prompt = """
A professional, modern cover image for a tech article about {topic}.
Style: Clean tech editorial, dark background, glowing elements.
Layout: Title '{title}' integrated as central holographic label.
Color: Blue-purple gradient (#8B7355 to #5B4D91).
Size: 900x383 pixels.
Composition: Minimalist with data flow particles.
"""
```

**正文图模板**：
```python
inline_prompt = """
A technical infographic showing {concept}.
Style: Clean data visualization, dark background, gradient colors.
Layout: Horizontal bar chart or comparison diagram.
Color: Teal to purple gradient.
Size: 1280x720 pixels (16:9).
Details: Clear labels, modern tech aesthetic.
"""
```

**金句图模板**：
```python
quote_prompt = """
A minimalist quote card for a tech article.
Quote: "{quote_text}"
Style: Premium editorial, dark background, subtle grid lines.
Typography: Large elegant white-gold text.
Size: 1080x1080 pixels (1:1).
Background: Subtle glowing particles representing data points.
"""
```

### 3. 图片类型映射

FireSpot 使用以下图片类型映射：

| 图片类型 | 尺寸 | 用途 | Prompt关键词 |
|----------|------|------|---------------|
| `cover` | 900x383 | 封面图 | cover image, tech editorial, holographic |
| `inline` | 1280x720 | 正文配图 | data visualization, infographic, comparison |
| `quote` | 1080x1080 | 金句图 | quote card, minimalist, typography |

### 4. 错误处理

**检查ZhipuArts可用性**：

```python
# 检查ZhipuArts MCP是否可用
try:
    test_result = mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
        "prompt": "test image",
        "size": "128x720"
    })
    zhipuarts_available = True
except Exception as e:
    zhipuarts_available = False
    print(f"❌ ZhipuArts MCP不可用: {e}")
```

**降级策略**：

如果 ZhipuArts 不可用，可以考虑：
1. 检查API密钥配置
2. 检查网络连接
3. 联系系统管理员

**不推荐降级到ModelArts**：
- ZhipuArts是专为FireSpot优化的解决方案
- ModelArts配置较为复杂
- 优先解决ZhipuArts的可用性问题

### 5. 性能优化

**批量生成**：

```python
# 并发生成多个图片
import asyncio

async def generate_images_batch(prompts):
    tasks = []
    for prompt_data in prompts:
        task = mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
            "prompt": prompt_data["prompt"],
            "size": prompt_data["size"]
        })
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

**缓存策略**：

```python
# 避免重复生成相同图片
import hashlib

def get_image_cache_key(prompt, size):
    return hashlib.md5(f"{prompt}:{size}".encode()).hexdigest()

# 检查缓存
cache_key = get_image_cache_key(prompt, size)
if cache_key in image_cache:
    return image_cache[cache_key]
```

---

## 📱 wechat-publisher MCP 工具

### 1. 图片准备

**工具名称**：`mcp_wechat_prepare_image`

**用途**：上传图片到微信素材库

**参数**：

```python
{
    "image_path": str,       # 必需，本地图片路径
    "type": str,            # 必需，图片类型
}
```

**支持的type**：
- `"thumb"` - 缩略图（封面）
- `"image"` - 正文图片

**示例**：

```python
result = mcp.call_tool("wechat-publisher", "mcp_wechat_prepare_image", {
    "image_path": "/mnt/user-data/outputs/cover_01.png",
    "type": "thumb"
})
```

### 2. 创建草稿

**工具名称**：`mcp_wechat_create_draft`

**用途**：创建微信公众号草稿

**参数**：

```python
{
    "title": str,            # 必需，文章标题
    "content": str,          # 必需，HTML内容
    "cover_url": str,        # 可选，封面图片URL
    "images": list,         # 可选，图片URL列表
}
```

**示例**：

```python
result = mcp.call_tool("wechat-publisher", "mcp_wechat_create_draft", {
    "title": "AI世界观（七）｜Embedding — AI 理解世界的方式",
    "content": "<html>...</html>",
    "cover_url": "https://mmbiz.qpic.cn/...",
    "images": ["https://mmbiz.qpic.cn/..."]
})
```

---

## 🔧 完整工作流示例

### 阶段7完整流程

```python
# 1. 读取阶段4的文章内容，提取图片占位符
import re

article_markdown = read_file("/mnt/user-data/outputs/stage4_draft.md")
image_placeholders = re.findall(r'\{\{IMG:(.+?)\}\}', article_markdown)

# 2. 为每个占位符生成图片
for asset_id in image_placeholders:
    # 确定图片类型
    if asset_id.startswith("cover"):
        size = "900x383"
        prompt_type = "cover"
    elif asset_id.startswith("quote"):
        size = "1080x1080"
        prompt_type = "quote"
    else:
        size = "1280x720"
        prompt_type = "inline"
    
    # 生成Prompt（根据阶段3的规划）
    prompt = generate_prompt_for_asset(asset_id, prompt_type)
    
    # 调用ZhipuArts生成图片
    result = mcp.call_tool("zhipuarts", "mcp_zhipuarts_generate_image", {
        "prompt": prompt,
        "size": size,
        "output_path": f"/mnt/user-data/outputs/{asset_id}.png"
    })
    
    print(f"✅ 生成图片: {asset_id} ({prompt_type})")

# 3. 替换占位符为真实图片路径
final_html = wechat_html
for asset_id in image_placeholders:
    final_html = final_html.replace(
        f"{{{{IMG:{asset_id}}}}",
        f'<img src="/mnt/user-data/outputs/{asset_id}.png" />'
    )

# 4. 保存最终版本
write_file("/mnt/user-data/outputs/stage8_final_with_images.html", final_html)
```

---

## 📊 工具对比

### ZhipuArts vs ModelArts

| 特性 | ZhipuArts | ModelArts |
|------|-----------|-----------|
| **模型** | GLM-Image | Qwen-Image |
| **提供商** | 智谱AI | 华为云 |
| **风格** | 专业科技风格 | 通用风格 |
| **FireSpot优化** | ✅ 是 | ❌ 否 |
| **中英文支持** | ✅ 均可 | ⚠️ 主要是英文 |
| **API稳定性** | ✅ 高 | ⚠️ 中等 |
| **配置复杂度** | ✅ 简单 | ❌ 复杂 |
| **推荐程度** | ⭐⭐⭐⭐⭐ | ⭐⭐ |

### 推荐使用ZhipuArts的理由

1. **专为FireSpot优化**：针对科技内容风格进行调优
2. **中英文友好**：支持中文Prompt，更符合使用习惯
3. **API稳定**：智谱AI企业级服务，稳定性更高
4. **配置简单**：只需配置API密钥，开箱即用
5. **快速生成**：平均3-5秒生成一张图片

---

## 🚨 故障排除

### 常见问题

**1. ZhipuArts MCP不可用**

```
错误信息：mcp.call_tool() failed: zhipuarts not found
```

**解决方案**：
1. 检查`extensions_config.json`中zhipuarts是否启用
2. 检查环境变量`ZHIPUARTS_API_KEY`是否配置
3. 重启DeerFlow服务使配置生效

**2. API密钥无效**

```
错误信息：Authentication failed
```

**解决方案**：
1. 检查`.env`文件中的`ZHIPUARTS_API_KEY`
2. 确认API密钥有效且未过期
3. 重新生成API密钥

**3. 图片生成失败**

```
错误信息：Image generation failed
```

**解决方案**：
1. 检查Prompt是否过长（建议<500字符）
2. 检查网络连接
3. 尝试简化Prompt重新生成

---

## ✅ 最佳实践总结

1. **优先使用ZhipuArts**：专为FireSpot优化的生图方案
2. **使用英文Prompt**：ZhipuArts对英文Prompt理解更好
3. **包含尺寸信息**：在Prompt中明确指定像素尺寸
4. **描述要具体**：包含风格、颜色、构图等要素
5. **批量生成**：使用异步并发提高效率
6. **错误处理**：添加重试机制和降级策略
7. **检查配置**：定期检查MCP工具可用性

---

**最后更新**：2026-05-09
**版本**：v7.2 - ZhipuArts MCP专业生图
**维护者**：FireSpot Team
