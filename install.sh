#!/bin/bash
# ============================================================================
# FireSpot V3.0 - 自动安装脚本
# ============================================================================
# 用途：自动将 FireSpot V3.0 安装到 DeerFlow 项目中
# 使用：sudo ./install.sh [deerflow_project_path]
# ============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 默认 DeerFlow 项目路径（假设此脚本在 DeerFlow 项目中运行）
DEERFLOW_PATH="${1:-$(cd "$SCRIPT_DIR/.." && pwd)}"

# 检查 DeerFlow 项目是否存在
check_deerflow_project() {
    print_header "检查 DeerFlow 项目"

    if [ ! -d "$DEERFLOW_PATH" ]; then
        print_error "DeerFlow 项目路径不存在: $DEERFLOW_PATH"
        echo "请确保 DeerFlow 已正确安装，或提供正确的项目路径"
        echo "用法: $0 [deerflow_project_path]"
        exit 1
    fi

    print_success "找到 DeerFlow 项目: $DEERFLOW_PATH"

    # 检查关键文件
    if [ -f "$DEERFLOW_PATH/config.yaml" ]; then
        print_success "找到 config.yaml"
    else
        print_warning "未找到 config.yaml，将在安装后创建"
    fi

    if [ -d "$DEERFLOW_PATH/backend" ]; then
        print_success "找到 backend 目录"
    else
        print_error "未找到 backend 目录，这不是有效的 DeerFlow 项目"
        exit 1
    fi

    echo ""
}

# 安装 FireSpot Skill
install_firespot_skill() {
    print_header "安装 FireSpot Skill"

    local skill_source="$SCRIPT_DIR/firespot-skill/SKILL.md"
    local skill_dest="$DEERFLOW_PATH/skills/public/firespot"

    # 创建目标目录
    mkdir -p "$skill_dest"

    # 复制 skill 文件
    if [ -f "$skill_source" ]; then
        cp "$skill_source" "$skill_dest/SKILL.md"
        print_success "FireSpot Skill 已复制到: $skill_dest"
    else
        print_error "未找到 FireSpot Skill 源文件: $skill_source"
        exit 1
    fi

    echo ""
}

# 安装微信 MCP 服务器
install_wechat_mcp_server() {
    print_header "安装微信 MCP 服务器"

    local mcp_source="$SCRIPT_DIR/mcp-servers/wechat"
    local mcp_dest="$DEERFLOW_PATH/mcp-servers/wechat"

    # 创建目标目录
    mkdir -p "$mcp_dest"

    # 复制 MCP 服务器文件
    if [ -f "$mcp_source/server.py" ]; then
        cp "$mcp_source/server.py" "$mcp_dest/server.py"
        print_success "MCP 服务器文件已复制"
    fi

    if [ -f "$mcp_source/start_wechat_server.sh" ]; then
        cp "$mcp_source/start_wechat_server.sh" "$mcp_dest/start_wechat_server.sh"
        chmod +x "$mcp_dest/start_wechat_server.sh"
        print_success "MCP 启动脚本已复制并设置为可执行"
    fi

    echo ""
}

# 配置环境变量
configure_environment() {
    print_header "配置环境变量"

    local env_template="$SCRIPT_DIR/.env.template"
    local env_file="$DEERFLOW_PATH/.env"

    if [ ! -f "$env_file" ]; then
        print_info ".env 文件不存在，创建新文件"
        cp "$env_template" "$env_file"
        print_success ".env 文件已创建"
    else
        print_info ".env 文件已存在，追加 FireSpot 配置"
        echo "" >> "$env_file"
        echo "# ============================================================================ #" >> "$env_file"
        echo "# FireSpot V3.0 - 微信公众号发布配置" >> "$env_file"
        echo "# ============================================================================ #" >> "$env_file"
        grep -E "^(WECHAT_APPID|WECHAT_APPSECRET|DEEPSEEK_API_KEY|ZHIPU_API_KEY|TAVILY_API_KEY)" "$env_template" >> "$env_file"
        print_success "FireSpot 配置已追加到 .env 文件"
    fi

    print_warning "请编辑 .env 文件，配置您的 API Keys"
    print_info "必需配置项："
    echo "   - DEEPSEEK_API_KEY (必需，LLM 模型)"
    echo "   - WECHAT_APPID (可选，发布功能)"
    echo "   - WECHAT_APPSECRET (可选，发布功能)"
    echo ""
    echo "   nano $env_file"
    echo ""
}

# 更新 DeerFlow 配置
update_deerflow_config() {
    print_header "更新 DeerFlow 配置"

    local config_dest="$DEERFLOW_PATH/config.yaml"
    local extensions_dest="$DEERFLOW_PATH/extensions_config.json"

    # 提示用户手动配置
    print_warning "需要手动更新配置文件"
    print_info "请按照以下步骤操作："
    echo ""
    echo "1. 编辑 config.yaml，添加 MCP 服务器配置："
    echo "   nano $config_dest"
    echo ""
    echo "2. 在文件末尾添加以下内容（参考 config/config.yaml.template）："
    echo "   mcp:"
    echo "     servers:"
    echo "       - name: wechat-publisher"
    echo "         type: sse"
    echo "         url: http://localhost:3101/sse"
    echo "         enabled: true"
    echo ""
    echo "3. 编辑 extensions_config.json，启用 FireSpot skill："
    echo "   nano $extensions_dest"
    echo ""
    echo "4. 在 skills 部分添加："
    echo "   \"skills\": {"
    echo "     \"firespot\": {"
    echo "       \"enabled\": true"
    echo "     }"
    echo "   }"
    echo ""

    # 询问是否自动配置
    read -p "是否尝试自动配置？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        auto_update_config
    else
        print_info "跳过自动配置，请手动完成上述步骤"
    fi

    echo ""
}

# 自动更新配置
auto_update_config() {
    print_info "尝试自动更新配置..."

    local config_dest="$DEERFLOW_PATH/config.yaml"
    local extensions_dest="$DEERFLOW_PATH/extensions_config.json"

    # 备份原配置
    if [ -f "$config_dest" ]; then
        cp "$config_dest" "$config_dest.backup.$(date +%Y%m%d_%H%M%S)"
        print_success "已备份 config.yaml"
    fi

    if [ -f "$extensions_dest" ]; then
        cp "$extensions_dest" "$extensions_dest.backup.$(date +%Y%m%d_%H%M%S)"
        print_success "已备份 extensions_config.json"
    fi

    # 更新 extensions_config.json
    if [ -f "$extensions_dest" ]; then
        # 使用 Python 处理 JSON
        python3 << EOF
import json

# 读取现有配置
try:
    with open('$extensions_dest', 'r') as f:
        config = json.load(f)
except:
    config = {"mcpServers": {}, "skills": {}}

# 添加微信 MCP 服务器
config['mcpServers']['wechat-publisher'] = {
    "enabled": True,
    "type": "sse",
    "command": None,
    "args": [],
    "env": {},
    "url": "http://localhost:3101/sse",
    "headers": {},
    "oauth": None,
    "description": "FireSpot 微信公众号发布服务器"
}

# 启用 FireSpot skill
config['skills']['firespot'] = {"enabled": True}

# 写回文件
with open('$extensions_dest', 'w') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("✅ extensions_config.json 已更新")
EOF
        print_success "extensions_config.json 已自动更新"
    fi

    print_info "config.yaml 需要手动添加 MCP 配置（见上述说明）"
    echo ""
}

# 安装 Python 依赖
install_dependencies() {
    print_header "安装 Python 依赖"

    print_info "检查并安装 required packages..."

    # 检查 Python 环境
    if ! command -v python3 &> /dev/null; then
        print_error "未找到 Python3"
        exit 1
    fi

    print_success "Python3 已找到"

    # 安装依赖
    print_info "安装 MCP 服务器依赖..."
    cd "$DEERFLOW_PATH"

    if pip3 install httpx mcp > /dev/null 2>&1; then
        print_success "Python 依赖安装成功"
    else
        print_warning "自动安装失败，请手动运行："
        echo "   pip3 install httpx mcp"
    fi

    echo ""
}

# 创建快速启动脚本
create_quickstart_script() {
    print_header "创建快速启动脚本"

    local script_path="$DEERFLOW_PATH/start-firespot.sh"

    cat > "$script_path" << 'EOF'
#!/bin/bash
# ============================================================================
# FireSpot V3.0 - 快速启动脚本
# ============================================================================

echo "🚀 启动 FireSpot V3.0 系统"
echo "========================="
echo ""

# 获取项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 设置环境变量（从 .env 文件读取）
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep ^WECHAT_ "$PROJECT_ROOT/.env" | xargs)
    export $(grep ^DEEPSEEK_ "$PROJECT_ROOT/.env" | xargs)
    export $(grep ^ZHIPU_ "$PROJECT_ROOT/.env" | xargs)
    export $(grep ^TAVILY_ "$PROJECT_ROOT/.env" | xargs)
fi

# 启动微信 MCP 服务器
echo "📱 启动微信 MCP 服务器..."
cd "$PROJECT_ROOT/mcp-servers/wechat"
if [ -f "start_wechat_server.sh" ]; then
    ./start_wechat_server.sh &
    sleep 2
    if lsof -i :3101 > /dev/null 2>&1; then
        echo "✅ 微信 MCP 服务器已启动 (端口 3101)"
    else
        echo "⚠️  微信 MCP 服务器启动失败"
    fi
else
    echo "❌ 未找到启动脚本"
fi

echo ""
echo "🎯 FireSpot V3.0 系统状态"
echo "====================="
echo ""

# 检查服务状态
if lsof -i :3101 > /dev/null 2>&1; then
    echo "✅ 微信 MCP 服务器: 运行中"
else
    echo "❌ 微信 MCP 服务器: 未运行"
fi

if lsof -i :2026 > /dev/null 2>&1; then
    echo "✅ DeerFlow: 运行中"
else
    echo "❌ DeerFlow: 未运行 (请运行 make dev)"
fi

echo ""
echo "📝 快速开始指南"
echo "=================="
echo "1. 确保 DeerFlow 正在运行 (make dev)"
echo "2. 访问 http://localhost:2026"
echo "3. 输入：帮我写一篇关于[选题]的公众号文章"
echo ""
echo "📚 更多信息："
echo "   - 使用指南: docs/FIRESPOT_USER_GUIDE.md"
echo "   - 配置说明: .env.template"
echo ""
EOF

    chmod +x "$script_path"
    print_success "快速启动脚本已创建: $script_path"

    echo ""
}

# 验证安装
verify_installation() {
    print_header "验证安装"

    local errors=0

    # 检查文件
    if [ -f "$DEERFLOW_PATH/skills/public/firespot/SKILL.md" ]; then
        print_success "✅ FireSpot Skill 已安装"
    else
        print_error "❌ FireSpot Skill 未安装"
        ((errors++))
    fi

    if [ -f "$DEERFLOW_PATH/mcp-servers/wechat/server.py" ]; then
        print_success "✅ 微信 MCP 服务器已安装"
    else
        print_error "❌ 微信 MCP 服务器未安装"
        ((errors++))
    fi

    if [ -f "$DEERFLOW_PATH/.env" ]; then
        print_success "✅ 环境变量文件已配置"
    else
        print_error "❌ 环境变量文件未配置"
        ((errors++))
    fi

    if [ -f "$DEERFLOW_PATH/start-firespot.sh" ]; then
        print_success "✅ 快速启动脚本已创建"
    else
        print_error "❌ 快速启动脚本未创建"
        ((errors++))
    fi

    echo ""

    if [ $errors -eq 0 ]; then
        print_success "🎉 安装验证通过！"
        return 0
    else
        print_error "❌ 安装验证失败，发现 $errors 个问题"
        return 1
    fi
}

# 显示下一步操作
show_next_steps() {
    print_header "下一步操作"

    echo "安装已完成！请按以下步骤开始使用："
    echo ""
    echo "1️⃣  配置 API Keys："
    echo "   nano $DEERFLOW_PATH/.env"
    echo "   将 'Your_XXX_API_KEY_HERE' 替换为真实值"
    echo ""
    echo "2️⃣  启动系统："
    echo "   cd $DEERFLOW_PATH"
    echo "   ./start-firespot.sh"
    echo ""
    echo "3️⃣ 访问 DeerFlow："
    echo "   http://localhost:2026"
    echo ""
    echo "4️⃣ 开始创作："
    echo "   输入：帮我写一篇关于[选题]的公众号文章"
    echo ""
    echo "📚 详细文档："
    echo "   - 用户指南: docs/FIRESPOT_USER_GUIDE.md"
    echo "   - 安装说明: docs/INSTALLATION_GUIDE.md"
    echo "   - 故障排除: docs/TROUBLESHOOTING.md"
    echo ""
}

# 主安装流程
main() {
    print_header "FireSpot V3.0 安装向导"

    print_info "DeerFlow 项目路径: $DEERFLOW_PATH"
    echo ""

    # 执行安装步骤
    check_deerflow_project
    install_firespot_skill
    install_wechat_mcp_server
    configure_environment
    update_deerflow_config
    install_dependencies
    create_quickstart_script

    # 验证安装
    if verify_installation; then
        show_next_steps
        print_success "🎊 FireSpot V3.0 安装完成！"
        exit 0
    else
        print_error "安装过程出现问题，请检查上述错误信息"
        exit 1
    fi
}

# 运行主程序
main "$@"
