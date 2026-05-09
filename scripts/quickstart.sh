#!/bin/bash

# FireSpot v7.2 - Quick Start Script
# This script helps you get started with FireSpot quickly

set -e

echo "🔥 FireSpot v7.2 - Quick Start"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Welcome to FireSpot v7.2!${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "SKILL.md" ]; then
    echo -e "${YELLOW}⚠️  Please run this script from the FireSpot root directory${NC}"
    exit 1
fi

echo -e "${GREEN}✅ FireSpot v7.2 detected${NC}"
echo ""

# Display basic information
echo "📋 Quick Information:"
echo "  Version: 7.2.0"
echo "  Workflow: 9 stages"
echo "  Main Features: ZhipuArts MCP, Auto Publishing"
echo ""

# Check documentation
echo "📚 Documentation Available:"
echo "  - README.md          : Project overview"
echo "  - INSTALL.md         : Installation guide"
echo "  - CHANGELOG.md       : Version history"
echo "  - GITHUB_RELEASE_GUIDE.md : GitHub release instructions"
echo ""

# Ask what user wants to do
echo "What would you like to do?"
echo ""
echo "1. 📖 Read documentation"
echo "2. 🔍 Verify installation"
echo "3. 🚀 Prepare for GitHub release"
echo "4. ❓ Get help"
echo "5. 🚪 Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "📖 Opening README.md..."
        if command -v less &> /dev/null; then
            less README.md
        else
            cat README.md
        fi
        ;;
    2)
        echo ""
        echo "🔍 Running installation verification..."
        bash release-check.sh
        ;;
    3)
        echo ""
        echo "🚀 GitHub Release Preparation"
        echo "Please follow the instructions in GITHUB_RELEASE_GUIDE.md"
        echo ""
        cat GITHUB_RELEASE_GUIDE.md
        ;;
    4)
        echo ""
        echo "❓ Getting Help"
        echo ""
        echo "Documentation:"
        echo "  - README.md          : Start here for project overview"
        echo "  - INSTALL.md         : Installation and configuration guide"
        echo "  - CHANGELOG.md       : What's new in this version"
        echo "  - PACKAGE_SUMMARY.md : Complete package summary"
        echo ""
        echo "Support:"
        echo "  - GitHub Issues: https://github.com/your-org/firespot/issues"
        echo "  - GitHub Discussions: https://github.com/your-org/firespot/discussions"
        echo ""
        echo "Quick Links:"
        echo "  - Main Skill File: SKILL.md"
        echo "  - Workflow Docs: references/workflow_v7.2.md"
        echo "  - Data Structures: references/data_structures.md"
        ;;
    5)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✨ Done!${NC}"
echo ""
echo "For more information, see:"
echo "  - README.md (overview)"
echo "  - INSTALL.md (installation)"
echo "  - GITHUB_RELEASE_GUIDE.md (release instructions)"