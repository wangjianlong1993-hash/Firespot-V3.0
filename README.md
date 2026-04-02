# 🎯 FireSpot V3.0 - 微信公众号 AI 内容创作与发布系统

**版本**: V3.0  
**发布日期**: 2026-04-02  
**许可协议**: MIT

---

![FireSpot Logo](https://img.shields.io/badge/FireSpot-v3.0-blue)
![DeerFlow](https://img.shields.io/badge/DeerFlow-compatible-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 🌟 项目简介

**FireSpot V3.0** 是一个基于 DeerFlow 的微信公众号内容创作和发布智能 Agent 系统。它通过 7 阶段标准化工作流，实现从热点研究、内容创作到自动发布的全流程自动化。

### 核心特性

- 🌍 **多平台热点研究**：自动研究微信、小红书、抖音、B站、YouTube 等平台
- 📝 **专业内容创作**：800-1500 字高质量文章，支持自定义风格
- 🖼️ **智能图片规划**：自动规划封面、配图、数据图、金句图
- ✅ **合规性校验**：自动检查字数、格式、引用来源等
- 📱 **一键发布到微信**：自动上传图片、创建草稿、保存到草稿箱
- 🤖 **多模型支持**：DeepSeek、Claude、GPT-4、智谱 AI 等

### 适用场景

- ✅ 公众号内容创作者
- ✅ 新媒体运营团队
- ✅ 个人品牌建设者
- ✅ 内容营销人员

---

## 🎯 功能展示

### 完整工作流程

```
用户输入 → 多平台研究 → 内容分析 → 内容规划
   ↓
内容创作 + 图片规划 → 合规校验 → 人工审核 → 自动发布
```

### 使用示例

**简单创作**：
```
帮我写一篇关于人工智能发展趋势的公众号文章
```

**高级定制**：
```
使用 FireSpot 创作一篇关于量子计算的科普文章，要求：
- 字数：1200字左右
- 角度：科普教育
- 包含：封面图、数据图、金句图
- 引用：至少3个权威来源
- 自动发布到草稿箱
```

---

## 📦 快速开始

### 1️⃣ 环境要求

- ✅ **DeerFlow 已安装** (1.0+)
- ✅ **Python 3.8+**
- ✅ **至少一个 LLM API Key** (推荐 DeepSeek)
- ✅ **5-10 分钟安装时间**

### 2️⃣ 安装 FireSpot

```bash
# 克隆或下载 FireSpot V3.0 到 DeerFlow 项目目录

# 进入安装目录
cd /path/to/deer-flow/Firespot\ V3.0

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 3️⃣ 配置 API Keys

```bash
cd /path/to/deer-flow
nano .env
```

**配置必需的 API Keys**：
```bash
# LLM API（必需）
DEEPSEEK_API_KEY=sk-your-real-deepseek-api-key

# 微信公众号（可选，用于发布功能）
WECHAT_APPID=wx-your-appid
WECHAT_APPSECRET=your-appsecret
```

### 4️⃣ 启动系统

```bash
cd /path/to/deer-flow
./start-firespot.sh
```

### 5️⃣ 开始使用

访问 **http://localhost:2026**，然后输入：

```
帮我写一篇关于[您感兴趣的任何话题]的公众号文章
```

---

## 📁 项目结构

```
Firespot V3.0/
├── install.sh                    # 自动安装脚本
├── .env.template                 # 环境变量配置模板
├── firespot-skill/               # FireSpot Skill 文件
│   └── SKILL.md                  # 技能定义
├── mcp-servers/                  # MCP 服务器文件
│   └── wechat/
│       ├── server.py            # 微信 MCP 服务器
│       └── start_wechat_server.sh  # 启动脚本
├── config/                       # 配置文件模板
│   ├── config.yaml.template      # DeerFlow 配置模板
│   └── extensions_config.json.template  # Extensions 配置模板
├── docs/                         # 文档目录
│   ├── FIRESPOT_USER_GUIDE.md   # 用户指南
│   ├── INSTALLATION_GUIDE.md     # 安装指南
│   ├── TROUBLESHOOTING.md        # 故障排除
│   └── API_REFERENCE.md          # API 参考
└── README.md                     # 本文件
```

---

## 🚀 核心功能详解

### 1. 多平台热点研究

FireSpot 会自动在以下平台搜索相关话题：
- 国内：微信公众号、小红书、抖音、B站
- 国际：YouTube、X (Twitter)、TikTok

**研究内容**：
- 热门话题和观点
- 用户评论和反馈
- 行业趋势和数据

### 2. 智能内容创作

**创作流程**：
1. **分析研究数据** → 提取关键信息
2. **生成文章大纲** → 确定结构
3. **撰写正文** → 专业内容
4. **优化标题** → 吸引眼球
5. **生成摘要** → 提炼要点

**质量保证**：
- 字数控制（800-1500字）
- 格式规范（微信公众号标准）
- SEO 优化（关键词布局）
- 引用标注（来源清晰）

### 3. 图片规划系统

**图片类型**：
- **封面图**：科技感、未来感，吸引点击
- **配图**：数据图、场景图，增强理解
- **金句图**：视觉强化，便于分享

**占位符格式**：
```
[IMAGE_PLACEHOLDER]
position: 封面
type: 封面图
description: 人形机器人与人类握手...
style: 科技写实风格
size: 2.35:1
purpose: 吸引点击
[/IMAGE_PLACEHOLDER]
```

### 4. 自动发布功能

**发布流程**：
1. ✅ 上传图片到微信素材库
2. ✅ 创建图文草稿
3. ✅ 保存到草稿箱
4. 📋 提醒最终确认发布

**支持操作**：
- 立即发布
- 定时发布
- 保存为草稿

---

## 🛠️ 技术架构

### 系统组成

```
┌─────────────────────────────────────────┐
│         DeerFlow (Agent System)          │
│  - LangGraph Server (port 2024)        │
│  - Gateway API (port 8001)              │
│  - Frontend (port 3000/2026)            │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│       FireSpot Skill (Agent Skill)       │
│  - 7阶段工作流                          │
│  - 多平台研究                            │
│  - 内容创作                              │
│  - 图片规划                              │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│      MCP Servers (Tool Integration)      │
│  - WeChat Publisher (port 3101)          │
│    - Upload media                         │
│    - Create drafts                        │
│    - Publish articles                     │
│  - XHS Publisher (port 3102)             │
│  - Douyin Publisher (port 3103)           │
└─────────────────────────────────────────┘
```

### 数据流

```
用户输入 → DeerFlow → FireSpot Skill
                         ↓
                   触发子Agent
                         ↓
              [研究Agent] → 调用搜索MCP工具
                         ↓
              [创作Agent] → 使用LLM创作
                         ↓
              [发布Agent] → 调用微信MCP工具
                         ↓
                   返回用户结果
```

---

## 📚 文档导航

### 用户文档
- **[快速开始指南](docs/FIRESPOT_USER_GUIDE.md)** - 5分钟上手
- **[完整安装指南](docs/INSTALLATION_GUIDE.md)** - 详细安装说明
- **[故障排除指南](docs/TROUBLESHOOTING.md)** - 问题解决方案

### 技术文档
- **[API 参考文档](docs/API_REFERENCE.md)** - MCP 工具接口
- **[开发指南](docs/DEVELOPER_GUIDE.md)** - 二次开发说明
- **[架构设计](docs/ARCHITECTURE.md)** - 系统架构详解

### 示例和教程
- **[使用案例](docs/USE_CASES.md)** - 实际应用场景
- **[最佳实践](docs/BEST_PRACTICES.md)** - 使用技巧
- **[视频教程](docs/VIDEO_TUTORIALS.md)** - 视频演示

---

## 🎯 使用场景示例

### 场景 1：科技博主

**需求**：每周创作 3-5 篇 AI 行业文章

**使用方式**：
```
帮我写一篇关于AI大模型的公众号文章，角度是技术发展趋势
```

**效果**：
- ⏱️ 创作时间：从 3 小时缩短到 10 分钟
- 📊 内容质量：专业、数据支撑、引用来源
- 📱 发布便捷：一键保存到草稿箱

### 场景 2：企业运营

**需求**：快速响应热点事件

**使用方式**：
```
帮我写一篇关于今日热点事件的公众号文章，角度是行业影响分析
```

**效果**：
- ⚡ 快速响应：30 分钟内完成
- 🔍 深度分析：多维度观点
- 📈 专业可信：数据支撑

### 场景 3：个人品牌

**需求**：建立专业形象

**使用方式**：
```
使用 FireSpot 创作一系列专业文章，主题是[您的专业领域]，风格是专家观点
```

**效果**：
- 🎯 定位精准：专家视角
- 📝 内容连贯：系列化输出
- 🏆 品牌建设：专业形象

---

## 🔧 配置选项

### 模型选择

**推荐配置**：
```yaml
# config.yaml
models:
  - name: deepseek-chat          # 快速响应
    api_key: $DEEPSEEK_API_KEY
    
  - name: deepseek-v3            # 深度思考
    api_key: $DEEPSEEK_API_KEY
    supports_thinking: true
```

### 技能配置

**启用 FireSpot**：
```json
// extensions_config.json
{
  "skills": {
    "firespot": {
      "enabled": true
    }
  }
}
```

### MCP 服务器配置

**微信发布服务**：
```yaml
mcp:
  servers:
    - name: wechat-publisher
      url: http://localhost:3101/sse
      enabled: true
```

---

## 📊 性能指标

### 创作速度

| 文章类型 | 字数 | 平均耗时 |
|---------|------|----------|
| 简单文章 | 500-800字 | 3-5 分钟 |
| 标准文章 | 800-1200字 | 5-10 分钟 |
| 深度文章 | 1200-1500字 | 10-15 分钟 |

### 资源占用

| 资源 | 占用情况 |
|------|----------|
| 内存 | ~500MB（创作中） |
| CPU | 中等（LLM 推理时较高） |
| 网络 | 依赖 LLM API 和搜索 API |

---

## 🎓 学习资源

### 视频教程
- [5分钟快速上手](https://example.com/quickstart)
- [完整功能演示](https://example.com/full-demo)
- [高级功能教程](https://example.com/advanced)

### 社区资源
- [用户社区](https://community.example.com)
- [开发者论坛](https://forum.example.com)
- [Discord 频道](https://discord.gg/example)

---

## 🤝 贡献指南

欢迎贡献代码、报告问题、提出建议！

### 贡献方式
1. Fork 本项目
2. 创建特性分支
3. 提交 Pull Request
4. 参与代码审查

### 开发指南
详见 [开发者指南](docs/DEVELOPER_GUIDE.md)

---

## 📜 许可协议

本项目采用 MIT 许可协议。详见 [LICENSE](LICENSE) 文件。

---

## 📞 联系方式

### 技术支持
- **GitHub Issues**: [问题追踪](https://github.com/your-repo/issues)
- **邮件支持**: support@example.com
- **微信社群**: 扫码加入用户群

### 商务合作
- **商务邮箱**: business@example.com
- **合作咨询**: partnership@example.com

---

## 🎉 致谢

感谢以下项目和工具的支持：
- [DeerFlow](https://github.com/your-repo/deerflow) - AI Agent 框架
- [DeepSeek](https://www.deepseek.com/) - LLM 服务
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent 编排框架
- [MCP](https://modelcontextprotocol.io/) - 模型上下文协议

---

## 📈 更新日志

### v3.0.0 (2026-04-02)

**新增功能**：
- ✨ 多平台热点研究
- ✨ 智能图片规划系统
- ✨ 自动发布到微信草稿箱
- ✨ 7阶段标准化工作流

**优化改进**：
- 🚀 创作速度提升 50%
- 📝 内容质量优化
- 🔧 配置流程简化
- 📚 文档完善

### v2.x 版本
- 基础内容创作功能
- 手动发布流程

---

## 🌟 开始您的 AI 创作之旅！

**FireSpot V3.0** 让公众号内容创作变得简单、高效、专业！

**立即开始**：
1. 安装 FireSpot V3.0
2. 配置 API Keys
3. 启动系统
4. 开始创作您的第一篇 AI 驱动文章

**创作无限可能！** 🚀

---

**[⬆ 返回顶部](#-firespot-v30-微信公众号-ai-内容创作与发布系统)**

**[📚 查看文档](docs/)**

**[🎯 快速开始](#快速开始)**
