# FireSpot v7.2 安装和使用指南

## 📥 安装方法

### 方法一：从GitHub安装（推荐）

1. **克隆仓库**
```bash
git clone https://github.com/your-org/firespot.git
cd firespot
git checkout v7.2.0
```

2. **验证安装**
```bash
bash release-check.sh
```

### 方法二：下载发布包

1. **下载并解压**
```bash
# 下载 .tar.gz 或 .zip 文件
wget https://github.com/your-org/firespot/releases/download/v7.2.0/firespot-v7.2.0.tar.gz

# 解压
tar -xzf firespot-v7.2.0.tar.gz
cd firespot-v7.2.0
```

2. **验证完整性**
```bash
# 验证SHA256校验和
shasum -a 256 -c firespot-v7.2.0.sha256
```

## ⚙️ 配置要求

### 必需组件

1. **Anthropic Claude Agent**
   - 安装Claude Agent CLI
   - 配置API密钥

2. **ZhipuArts MCP工具**（强烈推荐）
   - 安装ZhipuArts MCP服务器
   - 配置智谱AI API密钥

```json
{
  "mcpServers": {
    "zhipuarts": {
      "command": "npx",
      "args": ["-y", "@zhipuarts/mcp-server"],
      "env": {
        "ZHIPUARTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### 可选组件

1. **wechat-publisher MCP工具**
   - 用于自动发布到微信公众号
   - 需要微信开发者账号

```json
{
  "mcpServers": {
    "wechat-publisher": {
      "command": "npx",
      "args": ["-y", "@wechat-publisher/mcp-server"],
      "env": {
        "WECHAT_APP_ID": "your_app_id",
        "WECHAT_APP_SECRET": "your_app_secret"
      }
    }
  }
}
```

## 🚀 使用方法

### 在Claude Agent中使用

1. **配置技能路径**
```yaml
# claude-agent-config.yaml
skills:
  - path: /path/to/firespot
    enabled: true
```

2. **启动Agent**
```bash
claude-agent --skill firespot
```

3. **开始创作**
```
用户：帮我写一篇关于量子计算的商业化前景的公众号文章
Agent：启动FireSpot 9阶段工作流...
```

### 技能触发关键词

FireSpot会在以下情况自动激活：

**包含这些关键词会激活**：
- "公众号"、"推文"、"文章创作"
- "写文章"、"撰写"、"内容创作"
- "firespot"、"FireSpot"
- "从XX角度分析XX"（要求写成文章）

**不会激活的情况**：
- 纯粹的简短问答
- 技术问题排查
- 数据分析任务

## 📋 工作流程说明

FireSpot使用9阶段标准化工作流：

```
阶段0：参数收集 (用户输入)
    ↓
阶段1：多平台热点研究 (自动化)
    ↓
阶段2：内容分析 (自动化)
    ↓
阶段3：内容规划+图片规划 (自动化)
    ↓
阶段4：内容创作 (自动化)
    ↓
阶段5：合规校验 (自动化)
    ↓
阶段6：人工审核 (用户确认)
    ↓
阶段7：AI自动生图 (自动化)
    ↓
阶段8：图文合并预览 (自动化)
    ↓
阶段9：自动发布 (可选)
```

## 🔧 高级配置

### 自定义参数

```python
# 在对话中指定参数
用户：写一篇1500字的AI伦理文章，从技术监管角度，使用严肃专业的语气
```

### 修改工作流

如需自定义工作流，可以编辑：
- `SKILL.md` - 主要技能定义
- `references/workflow_v7.2.md` - 工作流详细规范

### 自定义Prompt模板

编辑以下文件来自定义Prompt：
- `assets/prompts/stage1_research.txt` - 研究阶段Prompt
- `assets/prompts/stage4_writing.txt` - 写作阶段Prompt
- `assets/prompts/image_generation.txt` - 图片生成Prompt

## 📊 输出文件说明

FireSpot会生成以下输出文件：

| 文件 | 位置 | 说明 |
|------|------|------|
| `stage4_draft.md` | `/mnt/user-data/outputs/` | Markdown格式文章草稿 |
| `stage4_article.json` | `/mnt/user-data/workspace/` | 文章元数据 |
| `stage6_review.html` | `/mnt/user-data/outputs/` | 审核页面HTML |
| `stage7_images.json` | `/mnt/user-data/workspace/` | 图片元数据 |
| `stage8_final.html` | `/mnt/user-data/outputs/` | 最终发布HTML |

## 🐛 故障排除

### 常见问题

**1. 技能无法激活**
- 检查触发关键词是否正确
- 确认技能路径配置正确
- 查看Claude Agent日志

**2. MCP工具连接失败**
- 验证API密钥配置
- 检查网络连接
- 确认MCP服务器运行状态

**3. 图片生成失败**
- 确认ZhipuArts MCP已配置
- 检查API配额是否充足
- 尝试简化Prompt重新生成

### 调试模式

启用详细日志：
```bash
claude-agent --skill firespot --debug --log-level debug
```

## 📈 性能优化

### 提高响应速度

1. **使用本地MCP服务器**
2. **缓存常用数据**
3. **调整工作流参数**

### 减少API调用

1. **跳过可选阶段**
2. **复用已有内容**
3. **批量处理**

## 🔗 相关资源

- **项目主页**: https://github.com/your-org/firespot
- **文档**: https://github.com/your-org/firespot/wiki
- **问题反馈**: https://github.com/your-org/firespot/issues
- **更新日志**: [CHANGELOG.md](CHANGELOG.md)

## 📞 获取帮助

如遇到问题：
1. 查看 [README.md](README.md)
2. 检查 [CHANGELOG.md](CHANGELOG.md) 中的已知问题
3. 在GitHub Issues中搜索类似问题
4. 创建新的Issue并提供详细信息

---

**FireSpot v7.2** - 让公众号内容创作更简单！
*最后更新: 2026-05-09*
