#!/bin/bash
# ============================================================================
# FireSpot V3.0 - 安装验证脚本
# ============================================================================
# 用途：验证 FireSpot V3.0 是否正确安装
# ============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🧪 FireSpot V3.0 安装验证"
echo "=========================="
echo ""

# 获取 DeerFlow 路径
if [ -d "/Users/garywong/deer-flow" ]; then
    DEERFLOW_PATH="/Users/garywong/deer-flow"
else
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -d "$SCRIPT_DIR/.." ]; then
        DEERFLOW_PATH="$SCRIPT_DIR/.."
    else
        echo -e "${RED}错误：无法找到 DeerFlow 项目${NC}"
        exit 1
    fi
fi

errors=0

# 验证 FireSpot Skill
echo "1️⃣ 验证 FireSpot Skill"
echo "----------------------"
FIRESPOT_SKILL="$DEERFLOW_PATH/skills/public/firespot/SKILL.md"

if [ -f "$FIRESPOT_SKILL" ]; then
    echo -e "${GREEN}✅${NC} FireSpot Skill 已安装"
    echo "   位置: $FIRESPOT_SKILL"
else
    echo -e "${RED}❌${NC} FireSpot Skill 未安装"
    ((errors++))
fi
echo ""

# 验证 MCP 服务器
echo "2️⃣ 验证微信 MCP 服务器"
echo "------------------------"
MCP_SERVER="$DEERFLOW_PATH/mcp-servers/wechat/server.py"

if [ -f "$MCP_SERVER" ]; then
    echo -e "${GREEN}✅${NC} 微信 MCP 服务器已安装"
    echo "   位置: $MCP_SERVER"
else
    echo -e "${RED}❌${NC} 微信 MCP 服务器未安装"
    ((errors++))
fi
echo ""

# 验证配置文件
echo "3️⃣ 验证配置文件"
echo "----------------"

ENV_FILE="$DEERFLOW_PATH/.env"
if [ -f "$ENV_FILE" ]; then
    echo -e "${GREEN}✅${NC} .env 文件存在"

    # 检查配置完整性
    missing_configs=0

    if ! grep -q "DEEPSEEK_API_KEY=" "$ENV_FILE" || grep -q "DEEPSEEK_API_KEY=Your_" "$ENV_FILE"; then
        echo -e "${YELLOW}⚠️  ${NC}DEEPSEEK_API_KEY 未配置或使用占位符"
        ((missing_configs++))
    else
        echo -e "${GREEN}✅${NC} DEEPSEEK_API_KEY 已配置"
    fi

    if ! grep -q "WECHAT_APPID=" "$ENV_FILE" || grep -q "WECHAT_APPID=Your_" "$ENV_FILE"; then
        echo -e "${YELLOW}⚠️  ${NC}WECHAT_APPID 未配置或使用占位符"
        ((missing_configs++))
    else
        echo -e "${GREEN}✅${NC} WECHAT_APPID 已配置"
    fi

    if [ $missing_configs -eq 0 ]; then
        echo -e "${GREEN}✅${NC} 所有必需配置已完成"
    else
        echo -e "${YELLOW}⚠️  ${NC}发现 $missing_configs 个未完成配置"
    fi
else
    echo -e "${RED}❌${NC} .env 文件不存在"
    ((errors++))
fi
echo ""

# 验证 DeerFlow 配置
echo "4️⃣ 验证 DeerFlow 配置"
echo "-------------------"

config_updated=false
extensions_updated=false

if grep -q "wechat-publisher" "$DEERFLOW_PATH/config.yaml" 2>/dev/null; then
    echo -e "${GREEN}✅${NC} MCP 服务器已配置（config.yaml）"
    config_updated=true
else
    echo -e "${YELLOW}⚠️  ${NC}MCP 服务器未配置（config.yaml）"
fi

if [ -f "$DEERFLOW_PATH/extensions_config.json" ]; then
    if python3 -c "import json; config=json.load(open('$DEERFLOW_PATH/extensions_config.json')); print('firespot' in config.get('skills', {}))" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} FireSpot 技能已启用（extensions_config.json）"
        extensions_updated=true
    else
        echo -e "${YELLOW}⚠️  ${NC}FireSpot 技能未启用（extensions_config.json）"
    fi
else
    echo -e "${YELLOW}⚠️  ${NC}extensions_config.json 不存在"
fi
echo ""

# 验证启动脚本
echo "5️⃣ 验证启动脚本"
echo "--------------"

START_SCRIPT="$DEERFLOW_PATH/start-firespot.sh"
if [ -f "$START_SCRIPT" ]; then
    echo -e "${GREEN}✅${NC} 快速启动脚本已创建"
    chmod +x "$START_SCRIPT"
else
    echo -e "${YELLOW}⚠️  ${NC}快速启动脚本未创建"
fi
echo ""

# Python 依赖验证
echo "6️⃣ 验证 Python 依赖"
echo "------------------"

check_module() {
    local module=$1
    local display_name=$2

    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✅${NC} $display_name 已安装"
        return 0
    else
        echo -e "${RED}❌${NC} $display_name 未安装"
        return 1
    fi
}

check_module "httpx" "httpx" || ((errors++))
check_module "mcp" "mcp" || ((errors++))
echo ""

# 服务状态验证
echo "7️⃣ 验证服务状态"
echo "--------------"

check_port() {
    local port=$1
    local service_name=$2

    if lsof -i :$port > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $service_name: 运行中 (端口 $port)"
    else
        echo -e "${YELLOW}⚠️  ${NC} $service_name: 未运行 (端口 $port)"
    fi
}

check_port 2026 "DeerFlow"
check_port 3101 "微信 MCP 服务器"
check_port 8001 "Gateway API"
echo ""

# 总结
echo "========================================"
echo "验证结果总结"
echo "========================================"
echo ""
echo -e "发现问题: ${RED}$errors${NC} 个"
echo ""

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}🎉 所有验证通过！FireSpot V3.0 已成功安装！${NC}"
    echo ""
    echo "🚀 下一步："
    echo "   1. 配置 API Keys（如果还未配置）"
    echo "   2. 启动服务："
    echo "      cd $DEERFLOW_PATH"
    echo "      ./start-firespot.sh"
    echo "   3. 访问 http://localhost:2026"
    echo "   4. 开始使用："
    echo "      帮我写一篇关于[选题]的公众号文章"
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠️  发现 $errors 个问题，请根据上述提示进行修复${NC}"
    echo ""
    echo "📚 帮助文档："
    echo "   - 安装指南: docs/INSTALLATION_GUIDE.md"
    echo "   - 故障排除: docs/TROUBLESHOOTING.md"
    echo "   - 用户指南: docs/FIRESPOT_USER_GUIDE.md"
    echo ""
    exit 1
fi
