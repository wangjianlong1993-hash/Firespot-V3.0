#!/bin/bash

# FireSpot v7.2 - GitHub Release Preparation Script
# This script helps prepare the FireSpot skill for GitHub release

set -e

echo "🔥 FireSpot v7.2 - GitHub Release Preparation"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "SKILL.md" ]; then
    echo -e "${RED}❌ Error: SKILL.md not found. Please run this script from the FireSpot root directory.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found FireSpot skill directory${NC}"
echo ""

# Check required files
echo "📋 Checking required files..."
required_files=(
    "SKILL.md"
    "README.md"
    "package.json"
    "CHANGELOG.md"
    "LICENSE"
    ".gitignore"
)

all_files_present=true
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file (missing)${NC}"
        all_files_present=false
    fi
done

if [ "$all_files_present" = false ]; then
    echo -e "${RED}❌ Some required files are missing. Please check the list above.${NC}"
    exit 1
fi

echo ""
echo "📂 Checking directory structure..."
directories=(
    "assets/prompts"
    "assets/templates"
    "assets/schemas"
    "assets/html"
    "scripts"
    "references"
)

all_dirs_present=true
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        file_count=$(find "$dir" -type f | wc -l)
        echo -e "${GREEN}✅ $dir (${file_count} files)${NC}"
    else
        echo -e "${RED}❌ $dir (missing)${NC}"
        all_dirs_present=false
    fi
done

echo ""
echo "🔍 Checking for common issues..."
issues_found=0

# Check for .DS_Store files
ds_store_files=$(find . -name ".DS_Store" -type f)
if [ -n "$ds_store_files" ]; then
    echo -e "${YELLOW}⚠️  Found .DS_Store files (should be in .gitignore)${NC}"
    issues_found=$((issues_found + 1))
fi

# Check for Python cache
python_cache=$(find . -type d -name "__pycache__" 2>/dev/null)
if [ -n "$python_cache" ]; then
    echo -e "${YELLOW}⚠️  Found Python cache directories${NC}"
    issues_found=$((issues_found + 1))
fi

# Check for large files
large_files=$(find . -type f -size +1M -not -path "./.git/*")
if [ -n "$large_files" ]; then
    echo -e "${YELLOW}⚠️  Found large files (>1MB):${NC}"
    echo "$large_files"
    issues_found=$((issues_found + 1))
fi

if [ $issues_found -eq 0 ]; then
    echo -e "${GREEN}✅ No common issues found${NC}"
fi

echo ""
echo "📊 Package Statistics..."
total_files=$(find . -type f -not -path "./.git/*" | wc -l)
total_dirs=$(find . -type d -not -path "./.git/*" | wc -l)
total_size=$(du -sh . | cut -f1)

echo "Total files: $total_files"
echo "Total directories: $total_dirs"
echo "Total size: $total_size"

echo ""
echo "📦 Content Summary..."
python_files=$(find . -name "*.py" -type f | wc -l)
markdown_files=$(find . -name "*.md" -type f | wc -l)
json_files=$(find . -name "*.json" -type f | wc -l)
html_files=$(find . -name "*.html" -type f | wc -l)
txt_files=$(find . -name "*.txt" -type f | wc -l)

echo "Python files: $python_files"
echo "Markdown files: $markdown_files"
echo "JSON files: $json_files"
echo "HTML files: $html_files"
echo "Text files: $txt_files"

echo ""
echo "🎯 Version Information..."
if [ -f "package.json" ]; then
    version=$(grep -o '"version": "[^"]*"' package.json | cut -d'"' -f4)
    echo -e "${GREEN}Version: $version${NC}"
fi

echo ""
echo "✨ Preparation Complete!"
echo ""
echo "Next steps:"
echo "1. Review the checklist above"
echo "2. Test the skill locally if needed"
echo "3. Commit changes: git add . && git commit -m 'Release v7.2.0'"
echo "4. Create tag: git tag v7.2.0"
echo "5. Push to GitHub: git push && git push --tags"
echo "6. Create GitHub Release with release notes"
echo ""
echo -e "${GREEN}🎉 FireSpot v7.2 is ready for GitHub release!${NC}"