# FireSpot 工作流程规范

## 概述

FireSpot 采用 7 阶段标准化工作流完成微信公众号内容创作，从热点研究到自动发布。

## 阶段定义

### 阶段0：参数收集

**目标**：识别用户意图，收集创作所需参数

**参数清单**：
1. **选题词**：本次内容的主题
2. **思考方向**：核心观点或切入角度
3. **目标字数**：建议800-1500字（默认1200字）
4. **品牌人设**：账号语气、目标受众（可选）
5. **发布平台**：默认微信公众号
6. **图片需求**：是否需要图片资产锚点（默认是）

### 阶段1：多平台热点研究

**目标**：在主流社交平台搜索相关话题讨论

**平台覆盖**：
- **国内平台**：微信公众号、小红书、B站、抖音
- **国际平台**：YouTube、X (Twitter)、TikTok
- **行业深度**：行业报告、新闻分析

**输出文件**：`/mnt/user-data/workspace/stage1_research.json`

**数据结构**：参见 `data_structures.md#stage1-research`

### 阶段2：内容分析

**目标**：基于研究结果进行深度分析和洞察提取

**核心任务**：
1. 确定核心主张和差异化角度
2. 整合跨平台洞察
3. 提取支撑论据和数据
4. 定义语气风格和目标受众

**输出文件**：`/mnt/user-data/workspace/stage2_analysis.json`

**数据结构**：参见 `data_structures.md#stage2-analysis`

### 阶段3：内容规划 + 图片规划

**目标**：生成文章结构框架 + 可执行图片资产规划

**核心任务**：
1. 生成多个标题备选
2. 设计开篇钩子
3. 规划3个核心段落
4. 定义结语方向
5. **规划图片资产**（封面、正文配图、金句图）

**输出文件**：`/mnt/user-data/workspace/stage3_outline.json`

**数据结构**：参见 `data_structures.md#stage3-outline`

### 阶段4：内容创作 + 图片锚点

**目标**：撰写高质量文章并插入图片锚点

**核心要求**：
1. **字数控制**：800-1500字
2. **禁用句式**：避免模板化表达
3. **段落节奏**：每段3-5行，有呼吸感
4. **图片锚点**：使用 `{{IMG:asset_id}}` 格式

**输出文件**：
- `/mnt/user-data/outputs/stage4_draft.md` - Markdown草稿
- `/mnt/user-data/workspace/stage4_article.json` - 发布数据

**数据结构**：参见 `data_structures.md#stage4-article`

### 阶段5：合规校验

**目标**：执行质量校验和合规检查

**校验维度**：
1. **字数检查**：800-2000字
2. **禁用句式**：检测陈词滥调
3. **图片锚点**：确保完整且正确
4. **段落结构**：检查段落节奏
5. **标题长度**：不超过64字

**执行方式**：使用 `scripts/validate_article.py`

**输出文件**：`/mnt/user-data/workspace/stage5_validation.json`

### 阶段6：人工审核

**目标**：生成审核HTML并等待用户批准

**用户响应选项**：
- `approve` - 批准，进入阶段7
- `revise` - 修改，回到阶段4
- `detail` - 查看详情，重新展示审核HTML
- `cancel` - 取消，结束任务

**输出文件**：
- `/mnt/user-data/outputs/stage6_review.html` - 审核HTML
- `/mnt/user-data/workspace/stage6_review_summary.json` - 审核摘要

**执行方式**：使用 `scripts/generate_review_html.py`

### 阶段7：自动发布

**目标**：AI生图并发布到微信公众号草稿箱

**核心任务**：
1. 按三通道策略准备图片资产
2. 生成图片（使用 ModelArts MCP）
3. 上传图片到微信素材库
4. 替换图片锚点为最终图片
5. 创建草稿箱文章

**前置要求**：
- 用户在阶段6明确回复 `approve`
- `/mnt/user-data/outputs/stage6_review.html` 已存在
- MCP 工具可用（ModelArts 和 wechat-publisher）

**输出文件**：`/mnt/user-data/workspace/stage7_publish_assets.json`

## 阶段依赖关系

```
Stage 0 → Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
         (必需)    (必需)    (必需)    (必需)    (必需)    (用户approve)
                                                      ↓
                                                   Stage 4 (revise)
```

## 退出条件

- **正常完成**：阶段7成功创建草稿
- **用户取消**：阶段6用户回复 `cancel`
- **修改循环**：阶段6用户回复 `revise`，回到阶段4

## 文件路径规范

所有文件使用虚拟路径，由 Sandbox 系统映射到物理路径：

```
/mnt/user-data/workspace/  →  backend/.deer-flow/threads/{thread_id}/user-data/workspace/
/mnt/user-data/outputs/    →  backend/.deer-flow/threads/{thread_id}/user-data/outputs/
```
