#!/bin/bash
# ============================================================================
# FireSpot V3.0 - 系统诊断脚本
# ============================================================================
# 用途：诊断 FireSpot V3.0 安装和配置问题
# ============================================================================

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

print_section() {
    echo ""
    echo -e "${YELLOW}▶ $1${NC}"
    echo "--------------------------------"
}

print_ok() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_fail() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 获取 DeerFlow 路径
if [ -d "/Users/garywong/deer-flow" ]; then
    DEERFLOW_PATH="/Users/garywong/deer-flow"
else
    # 尝试从脚本位置推断
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -d "$SCRIPT_DIR/../.." ]; then
        DEERFLOW_PATH="$SCRIPT_DIR/../.."
    else
        echo "错误：无法找到 DeerFlow 项目路径"
        exit 1
    fi
fi

print_header "FireSpot V3.0 系统诊断"

# ============================================================================
# 1. 系统环境检查
# ============================================================================
print_section "1. 系统环境检查"

# Python 版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
if [ -n "$PYTHON_VERSION" ]; then
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    if [ "$PYTHON_MAJOR" -ge 3 ]; then
        print_ok "Python 版本: $PYTHON_VERSION"
    else
        print_fail "Python 版本过低: $PYTHON_VERSION (需要 3.8+)"
    fi
else
    print_fail "未找到 Python3"
fi

# pip
if command -v pip3 &> /dev/null; then
    print_ok "pip 已安装"
else
    print_fail "pip 未安装"
fi

# Git
if command -v git &> /dev/null; then
    print_ok "Git 已安装"
else
    print_info "Git 未安装（非必需）"
fi

# ============================================================================
# 2. DeerFlow 项目检查
# ============================================================================
print_section "2. DeerFlow 项目检查"

if [ -d "$DEERFLOW_PATH" ]; then
    print_ok "DeerFlow 路径: $DEERFLOW_PATH"
else
    print_fail "DeerFlow 路径不存在: $DEERFLOW_PATH"
    exit 1
fi

# 检查关键文件和目录
if [ -f "$DEERFLOW_PATH/config.yaml" ]; then
    print_ok "config.yaml 存在"
else
    print_fail "config.yaml 不存在"
fi

if [ -d "$DEERFLOW_PATH/backend" ]; then
    print_ok "backend 目录存在"
else
    print_fail "backend 目录不存在"
fi

if [ -d "$DEERFLOW_PATH/frontend" ]; then
    print_ok "frontend 目录存在"
else
    print_info "frontend 目录不存在（可选）"
fi

# ============================================================================
# 3. FireSpot 安装检查
# ============================================================================
print_section "3. FireSpot 安装检查"

FIRESPOT_SKILL="$DEERFLOW_PATH/skills/public/firespot/SKILL.md"
MCP_SERVER="$DEERFLOW_PATH/mcp-servers/wechat/server.py"

if [ -f "$FIRESPOT_SKILL" ]; then
    print_ok "FireSpot Skill 已安装"
else
    print_fail "FireSpot Skill 未安装"
fi

if [ -f "$MCP_SERVER" ]; then
    print_ok "微信 MCP 服务器已安装"
else
    print_fail "微信 MCP 服务器未安装"
fi

# ============================================================================
# 4. 配置文件检查
# ============================================================================
print_section "4. 配置文件检查"

ENV_FILE="$DEERFLOW_PATH/.env"
if [ -f "$ENV_FILE" ]; then
    print_ok ".env 文件存在"

    # 检查关键配置
    if grep -q "DEEPSEEK_API_KEY=" "$ENV_FILE"; then
        print_info "DeepSeek API Key: 已配置"
    elif grep -q "DEEPSEEK_API_KEY=Your_" "$ENV_FILE"; then
        print_fail "DeepSeek API Key: 未配置（仍为占位符）"
    else
        print_info "DeepSeek API Key: 未配置"
    fi

    if grep -q "WECHAT_APPID=" "$ENV_FILE"; then
        if ! grep -q "WECHAT_APPID=Your_" "$ENV_FILE"; then
            print_ok "微信凭证: 已配置"
        else
            print_info "微信凭证: 未配置（仍为占位符）"
        fi
    else
        print_info "微信凭证: 未配置"
    fi
else
    print_fail ".env 文件不存在"
fi

# 检查 config.yaml
if grep -q "wechat-publisher" "$DEERFLOW_PATH/config.yaml" 2>/dev/null; then
    print_ok "MCP 服务器已配置（config.yaml）"
else
    print_fail "MCP 服务器未配置（config.yaml）"
fi

# 检查 extensions_config.json
if [ -f "$DEERFLOW_PATH/extensions_config.json" ]; then
    if python3 -c "import json; config=json.load(open('$DEERFLOW_PATH/extensions_config.json')); print('firespot' in config.get('skills', {}))" 2>/dev/null; then
        print_ok "FireSpot 技能已启用（extensions_config.json）"
    else
        print_fail "FireSpot 技能未启用（extensions_config.json）"
    fi
else
    print_fail "extensions_config.json 不存在"
fi

# ============================================================================
# 5. 服务状态检查
# ============================================================================
print_section "5. 服务状态检查"

# 检查端口占用
check_port() {
    local port=$1
    local service_name=$2

    if lsof -i :$port > /dev/null 2>&1; then
        print_ok "$service_name: 运行中 (端口 $port)"
        return 0
    else
        print_fail "$service_name: 未运行 (端口 $port)"
        return 1
    fi
}

check_port 2026 "DeerFlow"
check_port 3101 "微信 MCP 服务器"
check_port 8001 "Gateway API"

# ============================================================================
# 6. Python 依赖检查
# ============================================================================
print_section "6. Python 依赖检查"

check_module() {
    local module=$1
    local package_name=$2

    if python3 -c "import $module" 2>/dev/null; then
        print_ok "$package_name 已安装"
        return 0
    else
        print_fail "$package_name 未安装"
        return 1
    fi
}

check_module "httpx" "httpx"
check_module "mcp" "mcp"
check_module "uvicorn" "uvicorn"

# ============================================================================
# 7. 网络连接检查
# ============================================================================
print_section "7. 网络连接检查"

# 测试 LLM API
if [ -n "$DEEPSEEK_API_KEY" ] && [ "$DEEPSEEK_API_KEY" != "Your_DEEPSEEK_API_KEY_HERE" ]; then
    print_info "测试 DeepSeek API..."
    if curl -s -o /dev/null -w "%{http_code}" "https://api.deepseek.com" | grep -q "200\|302\|301"; then
        print_ok "DeepSeek API 可访问"
    else
        print_fail "DeepSeek API 不可访问"
    fi
else
    print_info "DeepSeek API Key 未配置，跳过测试"
fi

# 测试微信 API
if [ -n "$WECHAT_APPID" ] && [ "$WECHAT_APPID" != "Your_WECHAT_APPID_HERE" ]; then
    print_info "测试微信 API..."
    response=$(curl -s "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=$WECHAT_APPID&secret=$WECHAT_APPSECRET")
    if echo "$response" | grep -q "access_token"; then
        print_ok "微信 API 可访问"
    else
        print_fail "微信 API 认证失败（检查凭证或IP白名单）"
    fi
else
    print_info "微信凭证未配置，跳过测试"
fi

# ============================================================================
# 8. 生成诊断报告
# ============================================================================
print_header "诊断报告总结"

echo ""
echo "📊 系统状态总览"
echo "================"

# 统计问题数量
total_checks=20
passed_checks=0
failed_checks=0

# 简单统计（实际应该更精确）
if lsof -i :2026 > /dev/null 2>&1; then ((passed_checks++)); else ((failed_checks++)); fi
if lsof -i :3101 > /dev/null 2>&1; then ((passed_checks++)); else ((failed_checks++)); fi
if [ -f "$FIRESPOT_SKILL" ]; then ((passed_checks++)); else ((failed_checks++)); fi
if [ -f "$MCP_SERVER" ]; then ((passed_checks++)); else ((failed_checks++)); fi
if [ -f "$ENV_FILE" ]; then ((passed_checks++)); else ((failed_checks++)); fi

echo "通过检查: $passed_checks"
echo "失败检查: $failed_checks"
echo "完成度: $((passed_checks * 100 / (passed_checks + failed_checks)))%"

echo ""
if [ $passed_checks -ge $((total_checks * 2 / 3)) ]; then
    print_ok "🎉 系统基本就绪，可以开始使用！"
    echo ""
    echo "🚀 快速开始："
    echo "   1. 访问 http://localhost:2026"
    echo "   2. 输入：帮我写一篇关于[选题]的公众号文章"
    echo "   3. 等待 AI 完成创作和发布"
else
    print_fail "⚠️  系统未完全就绪，请根据上述提示进行修复"
    echo ""
    echo "🔧 建议操作："
    echo "   1. 运行安装脚本: cd 'Firespot V3.0' && ./install.sh"
    echo "   2. 配置 API Keys: nano .env"
    echo "   3. 启动服务: ./start-firespot.sh"
    echo "   4. 查看文档: docs/FIRESPOT_USER_GUIDE.md"
fi

echo ""
echo "📚 更多帮助："
echo "   - 用户指南: docs/FIRESPOT_USER_GUIDE.md"
echo "   - 安装指南: docs/INSTALLATION_GUIDE.md"
echo "   - 故障排除: docs/TROUBLESHOOTING.md"
echo ""

# 保存诊断报告
REPORT_FILE="$DEERFLOW_PATH/firespot_diagnostic_$(date +%Y%m%d_%H%M%S).txt"
{
    echo "FireSpot V3.0 诊断报告"
    echo "生成时间: $(date)"
    echo ""
    echo "系统环境:"
    echo "Python 版本: $(python3 --version 2>&1 || echo '未安装')"
    echo "操作系统: $(uname -s) $(uname -r)"
    echo ""
    echo "服务状态:"
    lsof -i :2026 -i :3101 -i :8001 || echo "无服务运行"
    echo ""
    echo "配置状态: 见上述输出"
} > "$REPORT_FILE"

echo "📄 诊断报告已保存: $REPORT_FILE"
echo ""
