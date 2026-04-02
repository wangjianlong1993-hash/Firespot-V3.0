# 🎯 FireSpot V3.0 新用户快速开始指南

**版本**: V3.0  
**更新时间**: 2026-04-02  
**适用人群**: 已安装 DeerFlow 的用户

---

## 📋 目录

1. [系统要求](#系统要求)
2. [快速安装](#快速安装)
3. [配置 API Keys](#配置-api-keys)
4. [启动系统](#启动系统)
5. [使用指南](#使用指南)
6. [故障排除](#故障排除)
7. [常见问题](#常见问题)

---

## 系统要求

### 必需环境
- ✅ **DeerFlow 已安装** (版本 1.0+)
- ✅ **Python 3.8+**
- ✅ **pip 包管理器**
- ✅ **网络连接** (用于 API 调用)

### 可选环境
- 微信公众平台账号（用于发布功能）
- 其他 LLM API Keys（DeepSeek、OpenAI 等）

---

## 快速安装

### 方法一：自动安装（推荐）

**步骤 1**：下载并解压 FireSpot V3.0
```bash
# 假设您已将 FireSpot V3.0 下载到 DeerFlow 项目目录
cd /path/to/deer-flow/Firespot\ V3.0
```

**步骤 2**：运行安装脚本
```bash
chmod +x install.sh
./install.sh
```

安装脚本将自动完成：
- ✅ 复制 FireSpot Skill 到 DeerFlow
- ✅ 复制微信 MCP 服务器文件
- ✅ 配置环境变量模板
- ✅ 更新 DeerFlow 配置
- ✅ 安装 Python 依赖
- ✅ 创建快速启动脚本

**步骤 3**：配置 API Keys（见下一节）

### 方法二：手动安装

详见 [手动安装指南](docs/INSTALLATION_GUIDE.md)

---

## 配置 API Keys

### 1. 编辑环境变量文件

```bash
cd /path/to/deer-flow
nano .env
```

### 2. 配置必需的 API Keys

#### **必需配置**

**DeepSeek API**（推荐用于中文内容创作）：
```bash
DEEPSEEK_API_KEY=sk-your-real-deepseek-api-key
```

**获取方式**：
1. 访问：https://platform.deepseek.com/
2. 注册/登录账号
3. 在 API Keys 页面创建新密钥
4. 复制密钥到 `.env` 文件

#### **可选配置**

**智谱 AI**（备选 LLM）：
```bash
ZHIPU_API_KEY=your-zhipu-api-key
```

**Tavily API**（网络搜索功能）：
```bash
TAVILY_API_KEY=your-tavily-api-key
```

**微信公众号**（发布功能）：
```bash
WECHAT_APPID=wx-your-appid
WECHAT_APPSECRET=your-appsecret
```

### 3. 保存并退出

按 `Ctrl+O` 保存，`Ctrl+X` 退出

---

## 启动系统

### 一键启动

```bash
cd /path/to/deer-flow
./start-firespot.sh
```

### 分步启动

**步骤 1**：启动 DeerFlow
```bash
cd /path/to/deer-flow
make dev
```

**步骤 2**：启动微信 MCP 服务器
```bash
cd mcp-servers/wechat
./start_wechat_server.sh &
```

**步骤 3**：验证服务状态
```bash
# 检查 DeerFlow (端口 2026)
lsof -i :2026

# 检查 MCP 服务器 (端口 3101)
lsof -i :3101
```

---

## 使用指南

### 访问 DeerFlow

打开浏览器访问：**http://localhost:2026**

### 基础使用

**简单创作**：
```
帮我写一篇关于[选题]的公众号文章
```

**示例**：
```
帮我写一篇关于人工智能发展的公众号文章
```

### 高级使用

**指定角度和字数**：
```
帮我写一篇1200字的公众号文章，主题是量子计算，从科普教育角度
```

**完整功能测试**：
```
使用 FireSpot 创作一篇关于AI医疗应用的深度分析文章，要求：
- 字数：1200字左右
- 包含：封面图、数据图、金句图
- 引用：至少3个权威来源
- 自动发布到草稿箱
```

### 可用命令

FireSpot 支持以下触发词：
- `帮我写...`
- `创作...`
- `撰写...`
- `公众号...`
- `微信公众号...`
- `推文...`
- `firespot...`

---

## 功能特性

### 🌍 多平台热点研究
- 微信公众号
- 小红书
- 抖音
- B站
- YouTube
- X (Twitter)
- TikTok

### 📝 专业内容创作
- 字数：800-1500字（可自定义）
- 风格：微信公众号标准格式
- SEO优化：关键词优化
- 引用来源：自动标注

### 🖼️ 图片规划系统
- 封面图占位符（科技感、未来感）
- 内容配图（数据图、场景图）
- 金句视觉强化图

### ✅ 智能合规校验
- 字数检查
- 禁用句式检测
- 图片占位符验证
- 引用来源校验

### 📱 自动发布功能
- 上传图片到微信素材库
- 创建图文草稿
- 保存到草稿箱
- 提醒最终确认发布

---

## 故障排除

### 问题 1：安装失败

**症状**：安装脚本执行失败

**解决方案**：
```bash
# 检查 Python 版本
python3 --version  # 应该是 3.8+

# 检查 DeerFlow 路径
ls /path/to/deer-flow/config.yaml

# 手动安装依赖
pip3 install httpx mcp
```

### 问题 2：MCP 服务器启动失败

**症状**：端口 3101 无法启动

**解决方案**：
```bash
# 检查端口占用
lsof -i :3101

# 停止占用进程
kill -9 $(lsof -ti :3101)

# 重新启动
cd mcp-servers/wechat
./start_wechat_server.sh &
```

### 问题 3：API Key 错误

**症状**：提示 API Key 无效

**解决方案**：
1. 检查 `.env` 文件中的 API Key 是否正确
2. 确认 API Key 有效且未过期
3. 检查账户余额是否充足

### 问题 4：微信发布失败

**症状**：无法发布到微信公众号

**解决方案**：
1. 检查 IP 白名单配置
2. 验证 AppID 和 AppSecret 是否正确
3. 确认账号权限（需要服务号）

---

## 常见问题

### Q1: FireSpot V3.0 是免费的吗？

**A**: FireSpot 本身完全免费开源。但您需要：
- LLM API（如 DeepSeek，有免费额度）
- 微信公众号账号（免费注册）

### Q2: 支持哪些 LLM 模型？

**A**: 支持所有 DeerFlow 兼容的模型：
- DeepSeek（推荐，中文效果好）
- 智谱 AI
- OpenAI (GPT-4)
- Claude (Anthropic)

### Q3: 可以同时发布到多个平台吗？

**A**: 当前版本主要支持微信公众号。小红书和抖音需要第三方 API 支持（计划中）。

### Q4: 文章质量如何保证？

**A**: FireSpot 采用 7 阶段标准化工作流：
1. 多平台热点研究
2. 深度内容分析
3. 详细内容规划
4. 专业内容创作
5. 多维度合规校验
6. 人工审核（可选）
7. 自动发布到草稿箱

### Q5: 可以自定义文章风格吗？

**A**: 可以！在使用时明确说明：
```
帮我写一篇关于AI的公众号文章，风格要轻松幽默，面向大学生
```

### Q6: 如何查看发布结果？

**A**: 
1. 文章会自动保存到微信公众平台的草稿箱
2. 登录微信公众平台：https://mp.weixin.qq.com/
3. 进入「草稿箱」查看和编辑
4. 最终确认发布

---

## 高级配置

### 自定义模型配置

编辑 `config.yaml` 添加更多模型：

```yaml
models:
  - name: claude-3-5-sonnet
    display_name: Claude 3.5 Sonnet
    use: langchain_anthropic:ChatAnthropic
    model: claude-3-5-sonnet-20241022
    api_key: $ANTHROPIC_API_KEY
    supports_vision: true
    supports_thinking: true
```

### 启用 Subagent（高级功能）

```yaml
agents:
  lead_agent:
    max_concurrent_subagents: 3
```

### 自定义中断模式

```yaml
channels:
  feishu:
    context:
      thinking_enabled: true
      subagent_enabled: true
```

---

## 技术支持

### 文档资源
- **安装指南**: [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)
- **故障排除**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
- **API 文档**: [docs/API_REFERENCE.md](docs/API_REFERENCE.md)

### 社区支持
- **GitHub Issues**: https://github.com/your-repo/deerflow/issues
- **文档中心**: 查看项目根目录 `README.md`

### 更新日志
查看 [CHANGELOG.md](CHANGELOG.md) 了解版本更新信息

---

## 🎊 开始使用

**恭喜！您已经完成了 FireSpot V3.0 的安装和配置。**

**立即开始创作**：
1. 访问 http://localhost:2026
2. 输入：`帮我写一篇关于[您感兴趣的话题]的公众号文章`
3. 等待 AI 完成创作和发布

**示例**：
```
帮我写一篇关于元宇宙发展趋势的公众号文章，角度是技术普及
```

**祝您创作愉快！** 🚀

---

**FireSpot V3.0** - 让 AI 帮您创作专业微信公众号内容
