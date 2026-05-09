# FireSpot HTML 输出模板设计规范

## 版本信息

- **版本**：v5.1
- **提炼自**：oura_ring_case_study_review.html
- **最后更新**：2026-04-29
- **设计理念**：专业、现代、学术风格，完全去AI化

## 核心设计原则

### 1. 去AI化设计（禁止元素）

```
❌ 禁止任何 emoji 表情符号（图片占位符除外）
❌ 禁止左侧彩色边框条（使用粉红色 #e91e63，仅4px）
❌ 禁止渐变背景（仅审核头部使用）
❌ 禁止圆角卡片样式（仅主容器使用12px圆角）
❌ 禁止装饰性图标
```

### 2. 配色方案（纯黑白灰+单强调色）

| 用途 | 颜色 | HEX | 用途说明 |
|------|------|-----|----------|
| **主文本** | 深灰 | #333 | 正文、标题 |
| **次要文本** | 中灰 | #666 | 元数据、参考来源 |
| **辅助文本** | 浅灰 | #999 | 标签、底部信息 |
| **背景色** | 极浅灰 | #f5f5f5 | 页面背景 |
| **容器背景** | 白色 | #fff | 内容卡片 |
| **强调色** | 粉红 | #e91e63 | 左侧边框（H2标题） |
| **成功色** | 绿色 | #00c853 | 审核徽章 |
| **链接色** | 蓝色 | #1565c0 | 引用链接 |
| **头部渐变** | 深蓝→深蓝黑 | #1a1a2e → #16213e | 审核头部 |

### 3. 字体系统

**字体栈**（按优先级）：
```
1. -apple-system (Apple 系统字体)
2. BlinkMacSystemFont (Apple 系统字体)
3. "Segoe UI" (Windows 字体)
4. "PingFang SC" (苹方-简体中文)
5. "Hiragino Sans GB" (冬青黑体)
6. "Microsoft YaHei" (微软雅黑)
7. sans-serif (非衬线字体后备)
```

**字号规范**：
- H1（审核头部标题）：24px
- H2（章节标题）：18px
- H3（参考来源标题）：15px
- 正文段落：15px
- 结语段落：14px
- 元数据标签：13px
- 底部信息：12px
- 引用标记：12px

**行高规范**：
- 总体行高：1.8
- 正文段落：1.9
- 参考来源：1.6

## HTML 结构规范

### 1. 文档结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ARTICLE_TITLE}} - FireSpot 审核稿</title>
    <style>...</style>
</head>
<body>
    <div class="review-header">...</div>
    <div class="container">
        <div class="meta-bar">...</div>
        <div class="content">...</div>
        <div class="review-footer">...</div>
    </div>
    <div class="sources-section">...</div>
</body>
</html>
```

### 2. 审核头部

**结构**：
```html
<div class="review-header">
    <h1>文章标题</h1>
    <div class="subtitle">副标题 · 审核稿</div>
    <div class="review-badge">合规校验 100/100 ✅</div>
</div>
```

**样式特点**：
- 深蓝到深蓝黑渐变背景
- 白色文字
- 底部三角形装饰（CSS实现）
- 居中对齐

### 3. 主容器

**结构**：
```html
<div class="container">
    <div class="meta-bar">元数据栏</div>
    <div class="content">正文内容</div>
    <div class="review-footer">审核底部</div>
</div>
```

**样式特点**：
- 最大宽度：680px
- 居中对齐
- 白色背景
- 12px 圆角
- 阴影效果

### 4. 元数据栏

**结构**：
```html
<div class="meta-bar">
    <span><span class="label">字数：</span>~1,220字</span>
    <span><span class="label">引用：</span>10处</span>
    <span><span class="label">配图：</span>4处锚点</span>
    <span><span class="label">状态：</span>待审核</span>
</div>
```

**样式特点**：
- 浅灰背景 (#fafbfc)
- 底部边框分割
- Flex 布局，自动换行
- 标签灰色，值深灰

### 5. 正文内容

**H2 标题样式**：
```css
.content h2 {
    font-size: 18px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 32px 0 16px;
    padding-left: 12px;
    border-left: 4px solid #e91e63;
}
```

**段落样式**：
```css
.content p {
    font-size: 15px;
    line-height: 1.9;
    margin-bottom: 16px;
    text-align: justify;  /* 两端对齐 */
}
```

**粗体样式**：
```css
.content strong {
    color: #1a1a2e;
    font-weight: 600;
}
```

### 6. 图片占位符

**结构**：
```html
<div class="img-placeholder">
    <span class="icon">📷</span>
    {{IMAGE_DESCRIPTION}}
</div>
```

**样式**：
```css
.img-placeholder {
    background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
    border: 2px dashed #90caf9;
    border-radius: 8px;
    padding: 32px;
    text-align: center;
    margin: 20px 0;
    color: #1565c0;
    font-size: 13px;
    font-weight: 500;
}
```

**图标选项**：
- 📷 封面图
- 📊 数据图表
- ⚖️ 对比图
- 📈 趋势图
- 💡 概念图

### 7. 引用标记

**结构**：
```html
<a class="citation" href="{{URL}}">[1]</a>
```

**样式**：
```css
.citation {
    color: #999;
    font-size: 12px;
    text-decoration: none;
    vertical-align: super;  /* 上标显示 */
    line-height: 0;
}
.citation:hover {
    color: #e91e63;  /* 悬停时变为粉红色 */
}
```

### 8. 结语区域

**结构**：
```html
<div class="closing">
    <h2>写在最后</h2>
    <p>{{CONCLUSION_1}}</p>
    <p>{{CONCLUSION_2}}</p>
    <p>{{CONCLUSION_CTA}}</p>
</div>
```

**样式**：
```css
.closing {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid #eee;
}
.closing p {
    font-size: 14px;
    color: #555;
    line-height: 1.8;
}
```

### 9. 参考来源区域

**结构**：
```html
<div class="sources-section">
    <h3>信源引用（10处）</h3>
    <ul>
        <li>[1] <a href="{{URL}}">{{SOURCE}}</a> — {{DESCRIPTION}}</li>
        ...
    </ul>
</div>
```

**样式**：
```css
.sources-section {
    max-width: 680px;
    margin: 0 auto 40px;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 20px rgba(0,0,0,0.08);
    padding: 24px;
}
.sources-section h3 {
    font-size: 15px;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 12px;
    padding-left: 10px;
    border-left: 3px solid #e91e63;
}
.sources-section li {
    font-size: 12px;
    color: #666;
    padding: 6px 0;
    border-bottom: 1px solid #f5f5f5;
    line-height: 1.6;
}
.sources-section a {
    color: #1565c0;
    text-decoration: none;
}
.sources-section a:hover {
    text-decoration: underline;
}
```

## 响应式设计

### 移动端适配（≤768px）

```css
@media (max-width: 768px) {
    .review-header h1 { font-size: 20px; }
    .container {
        margin: 20px;
        border-radius: 8px;
    }
    .content { padding: 24px 16px; }
    .content h2 { font-size: 16px; }
    .content p { font-size: 14px; }
}
```

## 变量替换规范

### 必需变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `{{ARTICLE_TITLE}}` | 文章标题 | "起底 Oura Ring：一枚戒指估值110亿" |
| `{{WORD_COUNT}}` | 字数 | "~1,220字" |
| `{{CITATION_COUNT}}` | 引用数量 | "10处" |
| `{{IMAGE_COUNT}}` | 配图数量 | "4处锚点" |
| `{{VALIDATION_STATUS}}` | 校验状态 | "合规校验 100/100 ✅" |

### 可选变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `{{SUBTITLE}}` | 副标题 | "FireSpot AI" |
| `{{STATUS}}` | 状态 | "待审核" |
| `{{FOOTER_TEXT}}` | 底部文字 | "FireSpot AI · 阶段6审核稿" |

## 使用示例

### 阶段6生成审核HTML

```python
# 读取模板
template = read_file("skills/public/firespot/assets/html/review_template.html")

# 准备数据
data = {
    "ARTICLE_TITLE": "起底 Oura Ring：一枚戒指估值110亿",
    "SUBTITLE": "FireSpot AI · 爆款案例拆解",
    "WORD_COUNT": "~1,220字",
    "CITATION_COUNT": "10处",
    "IMAGE_COUNT": "4处锚点",
    "STATUS": "待审核",
    "VALIDATION_STATUS": "合规校验 100/100 ✅",
    # ... 更多变量
}

# 替换变量
html = template
for key, value in data.items():
    html = html.replace(f"{{{{ {key} }}}}", value)

# 保存文件
write_file("/mnt/user-data/outputs/stage6_review.html", html)
```

## 设计检查清单

### 必须满足

- [ ] 使用指定的字体栈
- [ ] 配色方案符合规范
- [ ] H2 标题有左侧 4px 粉红边框
- [ ] 正文段落两端对齐
- [ ] 图片占位符使用渐变背景
- [ ] 引用标记上标显示
- [ ] 参考来源独立卡片展示
- [ ] 审核头部使用渐变背景
- [ ] 容器最大宽度 680px
- [ ] 响应式适配移动端

### 禁止出现

- [ ] emoji 表情符号（图片占位符除外）
- [ ] 左侧彩色边框条（仅 H2 标题允许）
- [ ] 装饰性图标
- [ ] 非指定的渐变背景
- [ ] 过度的圆角样式
- [ ] 任何 AI 特征的视觉元素

## 版本历史

- **v5.1** (2026-04-29)：提炼自 oura_ring_case_study_review.html，建立规范化设计标准
- 后续版本将基于实际使用反馈持续优化

---

**参考文档**：
- 模板来源：`/backend/.deer-flow/threads/29803723-aace-4f72-a346-bf05251af035/user-data/outputs/oura_ring_case_study_review.html`
- 设计原则：参考 `backend/packages/harness/deerflow/agents/firespot/config.py` 中的 `FIRESPOT_OUTPUT_REQUIREMENTS`
