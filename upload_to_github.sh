#!/bin/bash

# FireSpot 4.0 GitHub 上传脚本
# 使用方法: ./upload_to_github.sh YOUR_GITHUB_USERNAME

set -e

if [ -z "$1" ]; then
    echo "❌ 错误: 请提供您的 GitHub 用户名"
    echo ""
    echo "使用方法: $0 YOUR_GITHUB_USERNAME"
    echo ""
    echo "示例: $0 myusername"
    exit 1
fi

USERNAME="$1"
REPO_NAME="FireSpot-4.0"
REPO_URL="https://github.com/${USERNAME}/${REPO_NAME}.git"

echo "═══════════════════════════════════════════════════════════════"
echo "    FireSpot 4.0 上传到 GitHub"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📤 仓库信息:"
echo "   用户名: ${USERNAME}"
echo "   仓库名: ${REPO_NAME}"
echo "   仓库 URL: ${REPO_URL}"
echo ""

# 检查是否在正确的目录
if [ ! -f "README.md" ]; then
    echo "❌ 错误: 请在 FireSpot_4.0_Packaging 目录中运行此脚本"
    echo "   当前目录: $(pwd)"
    exit 1
fi

echo "✅ 目录检查通过"
echo ""

# 检查远程仓库是否已存在
if git remote | grep -q "origin"; then
    echo "⚠️  检测到已存在的 origin 远程仓库"
    echo "   正在移除..."
    git remote remove origin
fi

# 添加远程仓库
echo "📌 添加远程仓库..."
git remote add origin "${REPO_URL}"

# 确保分支名为 main
echo "🌿 设置分支为 main..."
git branch -M main

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "    准备上传！"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📋 接下来的步骤:"
echo ""
echo "1️️️   在浏览器中访问: https://github.com/new"
echo "2️️   创建新仓库:"
echo "    • 仓库名称: ${REPO_NAME}"
echo "    • 描述: FireSpot 4.0 - AI Content Creation Agent"
echo "    • 选择 Public 或 Private"
echo "    • ⚠️  不要勾选 'Add a README file'"
echo "    • 点击 'Create repository'"
echo ""
echo "3️️   创建完成后，按回车键继续..."
echo ""

read -p "按回车键继续..."

echo ""
echo "🚀 正在上传代码到 GitHub..."
echo ""

# 推送到 GitHub
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "    ✅ 上传成功！"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "🎉 您的仓库已经成功创建！"
    echo ""
    echo "📖 访问您的仓库:"
    echo "   ${REPO_URL}"
    echo ""
    echo "📌 建议添加的 Topics:"
    echo "   - ai-agent"
    echo "   - content-creation"
    echo "   - langgraph"
    echo "   - wechat"
    echo "   - automation"
    echo "   - python"
    echo ""
else
    echo ""
    echo "═══════════════════════════════════════════════════════════════"
    echo "    ❌ 上传失败"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "可能的原因:"
    echo "1. 仓库还未在 GitHub 上创建"
    echo "2. GitHub 用户名或密码错误"
    echo "3. 网络连接问题"
    echo ""
    echo "请检查以上问题后重试。"
    echo ""
    exit 1
fi
