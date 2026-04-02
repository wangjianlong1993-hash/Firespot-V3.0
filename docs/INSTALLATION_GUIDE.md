# 🔧 FireSpot V3.0 详细安装指南

**版本**: V3.0  
**难度**: 中等  
**预计时间**: 15-30 分钟

---

## 📋 安装前检查

### 1. 验证 DeerFlow 环境

**检查 DeerFlow 是否已安装**：
```bash
cd /path/to/deer-flow
ls config.yaml
ls backend/
ls frontend/
```

**预期输出**：
```
config.yaml
backend/
frontend/
```

**检查 DeerFlow 版本**：
```bash
cd /path/to/deer-flow/backend
cat pyproject.toml | grep version
```

**最低要求**：DeerFlow 1.0+

### 2. 验证 Python 环境

```bash
python3 --version
# 应该输出: Python 3.8.x 或更高

pip3 --version
# 应该显示 pip 版本信息
```

### 3. 验证网络连接

```bash
# 测试 PyPI 连接
ping -c 3 pypi.org

# 测试 GitHub 连接
ping -c 3 github.com
```

---

## 📦 方法一：自动安装（推荐）

### 步骤 1：准备安装文件

**假设您已将 `Firespot V3.0` 文件夹放在 DeerFlow 项目根目录**

```bash
cd /path/to/deer-flow
ls "Firespot V3.0"
```

**应该看到**：
```
install.sh
firespot-skill/
mcp-servers/
config/
docs/
.env.template
```

### 步骤 2：运行安装脚本

```bash
cd "Firespot V3.0"
chmod +x install.sh
./install.sh
```

**安装过程**：
1. ✅ 检查 DeerFlow 项目
2. ✅ 复制 FireSpot Skill
3. ✅ 复制 MCP 服务器文件
4. ✅ 配置环境变量
5. ✅ 更新 DeerFlow 配置
6. ✅ 安装 Python 依赖
7. ✅ 创建启动脚本
8. ✅ 验证安装

### 步骤 3：确认安装结果

安装完成后，脚本会显示验证结果：

```
✅ FireSpot Skill 已安装
✅ 微信 MCP 服务器已安装
✅ 环境变量文件已配置
✅ 快速启动脚本已创建
```

---

## 🔧 方法二：手动安装

### 步骤 1：手动复制文件

#### 1.1 复制 FireSpot Skill

```bash
cd /path/to/deer-flow

# 创建目标目录
mkdir -p skills/public/firespot

# 复制 Skill 文件
cp "Firespot V3.0/firespot-skill/SKILL.md" skills/public/firespot/
```

#### 1.2 复制微信 MCP 服务器

```bash
# 创建目标目录
mkdir -p mcp-servers/wechat

# 复制服务器文件
cp "Firespot V3.0/mcp-servers/wechat/server.py" mcp-servers/wechat/

# 复制启动脚本
cp "Firespot V3.0/mcp-servers/wechat/start_wechat_server.sh" mcp-servers/wechat/
chmod +x mcp-servers/wechat/start_wechat_server.sh
```

### 步骤 2：配置环境变量

#### 2.1 创建或更新 .env 文件

```bash
cd /path/to/deer-flow

# 如果 .env 不存在，从模板创建
if [ ! -f .env ]; then
    cp "Firespot V3.0/.env.template" .env
fi

# 如果 .env 已存在，追加 FireSpot 配置
echo "" >> .env
echo "# ============================================================================ #" >> .env
echo "# FireSpot V3.0 - 微信公众号发布配置" >> .env
echo "# ============================================================================ #" >> .env
grep -E "^(WECHAT_APPID|WECHAT_APPSECRET|DEEPSEEK_API_KEY|ZHIPU_API_KEY|TAVILY_API_KEY)" "Firespot V3.0/.env.template" >> .env
```

#### 2.2 配置 API Keys

```bash
nano .env
```

**将以下占位符替换为真实值**：
```bash
DEEPSEEK_API_KEY=Your_DEEPSEEK_API_KEY_HERE
ZHIPU_API_KEY=Your_ZHIPU_API_KEY_HERE
TAVILY_API_KEY=Your_TAVILY_API_KEY_HERE
WECHAT_APPID=Your_WECHAT_APPID_HERE
WECHAT_APPSECRET=Your_WECHAT_APPSECRET_HERE
```

保存并退出（`Ctrl+O`, `Ctrl+X`）

### 步骤 3：更新 DeerFlow 配置

#### 3.1 更新 config.yaml

```bash
nano config.yaml
```

**在文件末尾添加**：

```yaml
# ============================================================================
# MCP 服务器配置 - FireSpot V3.0
# ============================================================================
mcp:
  servers:
    - name: wechat-publisher
      type: sse
      url: http://localhost:3101/sse
      enabled: true
      description: "FireSpot 微信公众号发布服务器"
      tools:
        - mcp_wechat_upload_media
        - mcp_wechat_create_draft
        - mcp_wechat_publish
        - mcp_wechat_get_status
```

#### 3.2 更新 extensions_config.json

```bash
# 备份原配置
cp extensions_config.json extensions_config.json.backup

# 编辑配置
nano extensions_config.json
```

**在 `mcpServers` 部分添加**：

```json
{
  "mcpServers": {
    "wechat-publisher": {
      "enabled": true,
      "type": "sse",
      "url": "http://localhost:3101/sse",
      "description": "FireSpot 微信公众号发布服务器"
    }
  },
  "skills": {
    "firespot": {
      "enabled": true
    }
  }
}
```

### 步骤 4：安装 Python 依赖

```bash
# 进入项目目录
cd /path/to/deer-flow

# 安装 MCP 服务器依赖
pip3 install httpx mcp

# 验证安装
python3 -c "import httpx, mcp; print('依赖安装成功')"
```

### 步骤 5：创建快速启动脚本

```bash
cd /path/to/deer-flow

# 复制启动脚本
cp "Firespot V3.0/start-firespot.sh" .
chmod +x start-firespot.sh
```

---

## ✅ 验证安装

### 1. 检查文件结构

```bash
cd /path/to/deer-flow

# 检查 FireSpot Skill
ls -la skills/public/firespot/SKILL.md

# 检查 MCP 服务器
ls -la mcp-servers/wechat/server.py

# 检查配置文件
grep "firespot" extensions_config.json
grep "wechat-publisher" config.yaml
```

### 2. 运行测试脚本

```bash
cd "Firespot V3.0"
chmod +x test_installation.sh
./test_installation.sh
```

**预期输出**：
```
🧪 FireSpot V3.0 安装验证
================================
✅ FireSpot Skill: 已安装
✅ MCP 服务器: 已安装
✅ 配置文件: 已配置
✅ 环境变量: 已配置
✅ 启动脚本: 已创建
🎉 安装验证通过！
```

---

## 🚀 首次启动

### 1. 配置 API Keys（如果还未配置）

```bash
cd /path/to/deer-flow
nano .env
```

**必需配置**：
```bash
DEEPSEEK_API_KEY=sk-your-real-key-here
```

**可选配置**（用于发布功能）：
```bash
WECHAT_APPID=wx-your-appid
WECHAT_APPSECRET=your-appsecret
```

### 2. 启动系统

```bash
cd /path/to/deer-flow
./start-firespot.sh
```

### 3. 访问 DeerFlow

打开浏览器：http://localhost:2026

### 4. 测试 FireSpot

在聊天界面输入：
```
帮我写一篇简短的测试文章，主题是 FireSpot 安装测试
```

---

## 📝 安装检查清单

使用此清单确保安装完整：

- [ ] DeerFlow 已正确安装并运行
- [ ] Python 3.8+ 已安装
- [ ] FireSpot Skill 文件已复制到 `skills/public/firespot/`
- [ ] MCP 服务器文件已复制到 `mcp-servers/wechat/`
- [ ] `.env` 文件已配置
- [ ] `config.yaml` 已更新（包含 MCP 配置）
- [ ] `extensions_config.json` 已更新（启用 FireSpot）
- [ ] Python 依赖已安装（httpx, mcp）
- [ ] 微信 MCP 服务器可启动
- [ ] DeerFlow 可正常访问
- [ ] FireSpot 技能可正常调用

---

## 🎯 下一章

安装完成后，请阅读：
- **[用户指南](docs/FIRESPOT_USER_GUIDE.md)** - 学习如何使用
- **[故障排除](docs/TROUBLESHOOTING.md)** - 解决常见问题
- **[API 参考](docs/API_REFERENCE.md)** - 了解 MCP 工具

---

## 📞 获取帮助

如果安装过程中遇到问题：

1. **查看日志文件**：
   ```bash
   tail -f /tmp/wechat-mcp.log
   ```

2. **检查服务状态**：
   ```bash
   lsof -i :2026  # DeerFlow
   lsof -i :3101  # MCP 服务器
   lsof -i :8001  # Gateway
   ```

3. **运行诊断脚本**：
   ```bash
   cd "Firespot V3.0"
   ./diagnose.sh
   ```

4. **查看详细文档**：
   - [故障排除指南](docs/TROUBLESHOOTING.md)
   - [FAQ](docs/FAQ.md)

---

**祝您安装顺利！** 🎉

如有问题，请参考故障排除文档或联系技术支持。
