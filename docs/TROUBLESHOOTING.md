# 🔧 FireSpot V3.0 故障排除指南

**版本**: V3.0  
**更新时间**: 2026-04-02

---

## 📋 目录

1. [安装问题](#安装问题)
2. [配置问题](#配置问题)
3. [运行时问题](#运行时问题)
4. [API 连接问题](#api-连接问题)
5. [微信发布问题](#微信发布问题)
6. [性能问题](#性能问题)
7. [诊断工具](#诊断工具)

---

## 安装问题

### ❌ 问题：安装脚本执行失败

**症状**：
```bash
./install.sh
bash: ./install.sh: Permission denied
```

**解决方案**：
```bash
chmod +x install.sh
./install.sh
```

---

### ❌ 问题：找不到 DeerFlow 项目

**症状**：
```
❌ DeerFlow 项目路径不存在
```

**解决方案**：
```bash
# 检查当前目录
pwd

# 指定正确的 DeerFlow 路径
./install.sh /path/to/deer-flow

# 或者确保在 DeerFlow 项目根目录运行
cd /path/to/deer-flow
"Firespot V3.0/install.sh"
```

---

### ❌ 问题：Python 依赖安装失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement httpx
```

**解决方案**：
```bash
# 更新 pip
pip3 install --upgrade pip

# 使用国内镜像源
pip3 install httpx mcp -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用 conda（如果使用 conda 环境）
conda install -c conda-forge httpx mcp
```

---

### ❌ 问题：文件复制失败

**症状**：
```
cp: cannot create regular file '...': Permission denied
```

**解决方案**：
```bash
# 检查文件权限
ls -la /path/to/deer-flow/skills/public/
ls -la /path/to/deer-flow/mcp-servers/

# 修复权限
chmod +w /path/to/deer-flow/skills/public/
chmod +w /path/to/deer-flow/mcp-servers/

# 重新运行安装
./install.sh
```

---

## 配置问题

### ❌ 问题：.env 文件配置错误

**症状**：
```
KeyError: 'WECHAT_APPID'
```

**解决方案**：
```bash
# 检查 .env 文件
cat .env | grep WECHAT

# 确保没有多余的空格或引号
# 错误示例：WECHAT_APPID = "wx123"
# 正确示例：WECHAT_APPID=wx123
```

---

### ❌ 问题：config.yaml 语法错误

**症状**：
```
Error loading config.yaml
```

**解决方案**：
```bash
# 验证 YAML 语法
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# 检查缩进（YAML 对缩进敏感）
# 使用空格，不要使用 Tab

# 恢复备份
cp config.yaml.backup.YYYYMMDD_HHMMSS config.yaml

# 重新编辑
nano config.yaml
```

---

### ❌ 问题：extensions_config.json 格式错误

**症状**：
```
JSON decode error
```

**解决方案**：
```bash
# 验证 JSON 格式
python3 -m json.tool extensions_config.json

# 恢复备份
cp extensions_config.json.backup.* extensions_config.json

# 重新编辑
nano extensions_config.json
```

---

## 运行时问题

### ❌ 问题：DeerFlow 无法启动

**症状**：
```
Error: Port 2026 already in use
```

**解决方案**：
```bash
# 检查端口占用
lsof -i :2026

# 停止占用进程
kill -9 $(lsof -ti :2026)

# 重新启动
cd /path/to/deer-flow
make dev
```

---

### ❌ 问题：MCP 服务器启动失败

**症状**：
```
ERROR: [Errno 48] address already in use
```

**解决方案**：
```bash
# 检查端口 3101
lsof -i :3101

# 停止占用进程
kill -9 $(lsof -ti :3101)

# 检查环境变量
echo $WECHAT_APPID
echo $WECHAT_APPSECRET

# 重新启动
cd mcp-servers/wechat
./start_wechat_server.sh &
```

---

### ❌ 问题：FireSpot 技能未激活

**症状**：
```
使用 FireSpot 时无响应
```

**解决方案**：
```bash
# 1. 检查 skill 文件是否存在
ls skills/public/firespot/SKILL.md

# 2. 检查 extensions_config.json
grep firespot extensions_config.json

# 3. 重启 DeerFlow
make stop
make dev

# 4. 在 DeerFlow 中重新启用技能
# 访问 http://localhost:2026/settings/skills
```

---

## API 连接问题

### ❌ 问题：LLM API 调用失败

**症状**：
```
Error: DEEPSEEK_API_KEY is invalid
```

**解决方案**：
```bash
# 1. 验证 API Key
cat .env | grep DEEPSEEK_API_KEY

# 2. 检查 API Key 格式
# DeepSeek Key 应该以 "sk-" 开头

# 3. 测试 API 连接
curl -s https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"hi"}]}'

# 4. 更新 API Key
nano .env
```

---

### ❌ 问题：网络搜索功能不可用

**症状**：
```
Error: TAVILY_API_KEY not configured
```

**解决方案**：
```bash
# 1. 获取 Tavily API Key
# 访问：https://tavily.com/

# 2. 配置 API Key
nano .env
# 添加：TAVILY_API_KEY=tvly-your-key-here

# 3. 重启服务
./start-firespot.sh
```

---

### ❌ 问题：微信 API 连接超时

**症状**：
```
TimeoutError: Request timeout
```

**解决方案**：
```bash
# 1. 检查网络连接
ping api.weixin.qq.com

# 2. 检查防火墙设置
sudo ufw status

# 3. 尝试手动获取 Token
curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=YOUR_APPID&secret=YOUR_SECRET"

# 4. 检查 IP 白名单
# 登录微信公众平台 → 设置与开发 → 基本配置 → IP 白名单
```

---

## 微信发布问题

### ❌ 问题：IP 白名单错误

**症状**：
```json
{
  "errcode": 40164,
  "errmsg": "invalid ip xxx.xxx.xxx.xxx, not in whitelist"
}
```

**解决方案**：
```
1. 登录微信公众平台：https://mp.weixin.qq.com/

2. 进入「设置与开发」→「基本配置」

3. 找到「IP 白名单」设置

4. 添加您的服务器 IP 地址

5. 保存设置

6. 重启 MCP 服务器
   pkill -f "wechat.*server.py"
   cd mcp-servers/wechat
   ./start_wechat_server.sh &
```

---

### ❌ 问题：图片上传失败

**症状**：
```
Error: Invalid media file format
```

**解决方案**：
```bash
# 1. 检查图片格式
# 支持格式：JPG, PNG
# 图片大小：≤ 5MB

# 2. 测试图片上传
curl -X POST "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=TOKEN&type=image" \
  -F "media=@/path/to/image.jpg"

# 3. 检查图片 URL
# 确保 URL 可访问
curl -I https://example.com/image.jpg
```

---

### ❌ 问题：草稿创建失败

**症状**：
```
Error: Invalid thumb_media_id
```

**解决方案**：
```bash
# 1. 确认封面图已上传
# 检查上传返回的 media_id

# 2. 验证 media_id 格式
# 应该是：MEDIA_ID（不是 URL）

# 3. 检查内容格式
# 确保正文是 HTML 格式

# 4. 查看详细错误
# 返回的错误信息包含具体原因
```

---

## 性能问题

### ❌ 问题：文章生成速度慢

**症状**：
```
生成一篇文章需要超过 10 分钟
```

**解决方案**：
```bash
# 1. 使用更快的模型
# 编辑 config.yaml，切换到 deepseek-chat（而不是 deepseek-v3）

# 2. 减少搜索范围
# 在请求时指定：只搜索微信公众号平台

# 3. 降低字数要求
# 指定字数为 800 字而不是 1500 字

# 4. 禁用 thinking 模式
# 使用 flash 模式而不是 pro/ultra 模式
```

---

### ❌ 问题：内存占用过高

**症状**：
```
Memory Error: Out of memory
```

**解决方案**：
```bash
# 1. 减少并发子 Agent
# 编辑 config.yaml：
# agents:
#   lead_agent:
#     max_concurrent_subagents: 1  # 从 3 减少到 1

# 2. 使用上下文较短的模型
# 选择 max_tokens 较小的模型

# 3. 重启服务
make stop
make dev
```

---

## 诊断工具

### 1. 系统状态检查脚本

```bash
cd "Firespot V3.0"
./diagnose.sh
```

**输出**：
```
🔍 系统诊断报告
==================
✅ Python 版本: 3.9.7
✅ DeerFlow: 运行中 (端口 2026)
✅ MCP 服务器: 运行中 (端口 3101)
⚠️  API Keys: 部分未配置
```

### 2. 配置验证脚本

```bash
cd "Firespot V3.0"
./verify_config.sh
```

### 3. 日志查看工具

```bash
# DeerFlow 日志
tail -f /path/to/deer-flow/backend/.langgraph.log

# MCP 服务器日志
tail -f /tmp/wechat-mcp.log

# 系统日志
tail -f /var/log/system.log
```

### 4. 网络诊断工具

```bash
# 测试 API 连通性
curl -I https://api.deepseek.com
curl -I https://api.weixin.qq.com

# 测试 DNS 解析
nslookup api.deepseek.com
nslookup api.weixin.qq.com

# 测试端口连通性
telnet localhost 3101
telnet localhost 2026
```

---

## 🔧 高级故障排除

### 重置安装

如果问题无法解决，可以重置安装：

```bash
# 1. 停止所有服务
make stop
pkill -f "wechat.*server.py"

# 2. 备份配置
cp config.yaml config.yaml.backup
cp extensions_config.json extensions_config.json.backup
cp .env .env.backup

# 3. 删除 FireSpot 文件
rm -rf skills/public/firespot
rm -rf mcp-servers/wechat

# 4. 重新安装
cd "Firespot V3.0"
./install.sh

# 5. 恢复配置
# 手动合并之前的自定义配置
```

### 清理缓存

```bash
# 清理 Python 缓存
pip3 cache purge

# 清理 DeerFlow 缓存
rm -rf backend/.deer-flow/cache/

# 清理浏览器缓存
# 在浏览器中按 Ctrl+Shift+Delete
```

---

## 📞 获取更多帮助

### 在线资源

- **GitHub Issues**: [项目问题追踪](https://github.com/your-repo/deerflow/issues)
- **文档中心**: [完整文档](../README.md)
- **社区论坛**: [用户社区](https://community.example.com)

### 本地文档

- **[用户指南](FIRESPOT_USER_GUIDE.md)**
- **[安装指南](INSTALLATION_GUIDE.md)**
- **[API 参考](API_REFERENCE.md)**

### 联系支持

如需技术支持，请提供：
1. 系统环境信息（OS、Python 版本等）
2. 错误日志完整内容
3. 配置文件（隐藏敏感信息后）
4. 复现步骤

---

**最后更新**: 2026-04-02  
**维护者**: FireSpot V3.0 团队
