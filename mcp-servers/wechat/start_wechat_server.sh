#!/bin/bash
# 微信公众号 MCP 服务器启动脚本

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 设置环境变量（从项目根目录的 .env 文件读取）
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep ^WECHAT_ "$PROJECT_ROOT/.env" | xargs)
else
    echo "错误：未找到 .env 文件，请确保已配置微信公众账号凭证"
    exit 1
fi

# 检查必需的环境变量
if [ -z "$WECHAT_APPID" ] || [ -z "$WECHAT_APPSECRET" ]; then
    echo "错误：请在 .env 文件中配置 WECHAT_APPID 和 WECHAT_APPSECRET"
    exit 1
fi

echo "微信公众号 MCP 服务器启动中..."
echo "AppID: $WECHAT_APPID"
echo "监听端口: 3101"
echo "SSE 端点: http://localhost:3101/sse"
echo ""

# 启动服务器
cd "$SCRIPT_DIR"
python3 server.py
