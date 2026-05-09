#!/bin/bash

# FireSpot v7.2.0 - GitHub Release Creation Script
# This script creates a GitHub release using the GitHub API

# Note: You need a GitHub Personal Access Token with repo permissions
# Create one at: https://github.com/settings/tokens

echo "🚀 Creating GitHub Release for FireSpot v7.2.0"
echo "=============================================="
echo ""

# Check if we have a GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  GITHUB_TOKEN environment variable not set"
    echo ""
    echo "Please set your GitHub Personal Access Token:"
    echo "export GITHUB_TOKEN='your_token_here'"
    echo ""
    echo "Create a token at: https://github.com/settings/tokens"
    echo "Required scopes: repo (full repo access)"
    echo ""
    exit 1
fi

REPO="wangjianlong1993-hash/Firespot-V4.0"
TAG="v7.2.0"
TITLE="FireSpot v7.2.0 - 重大工作流优化升级"

# Read release notes from file
RELEASE_NOTES_FILE="GITHUB_RELEASE_NOTES.md"
if [ ! -f "$RELEASE_NOTES_FILE" ]; then
    echo "❌ Release notes file not found: $RELEASE_NOTES_FILE"
    exit 1
fi

RELEASE_NOTES=$(cat "$RELEASE_NOTES_FILE")

echo "📋 Release Information:"
echo "  Repository: $REPO"
echo "  Tag: $TAG"
echo "  Title: $TITLE"
echo ""

# Create the release using GitHub API
echo "🔄 Creating release via GitHub API..."
RESPONSE=$(curl -X POST \
  "https://api.github.com/repos/$REPO/releases" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -d "{
    \"tag_name\": \"$TAG\",
    \"target_commitish\": \"update-to-v7.2\",
    \"name\": \"$TITLE\",
    \"body\": $(echo "$RELEASE_NOTES" | jq -Rs .),
    \"draft\": false,
    \"prerelease\": false
  }" \
  2>&1)

# Check if release was created successfully
if echo "$RESPONSE" | grep -q "html_url"; then
    echo "✅ Release created successfully!"
    echo ""
    echo "🔗 Release URL:"
    echo "$RESPONSE" | jq -r '.html_url'
    echo ""
    echo "📊 Release Information:"
    echo "$RESPONSE" | jq -r '{name: .name, tag: .tag_name, url: .html_url, created_at: .created_at}'
else
    echo "❌ Failed to create release"
    echo ""
    echo "Error response:"
    echo "$RESPONSE"
    echo ""
    echo "💡 Manual creation:"
    echo "1. Visit: https://github.com/$REPO/releases/new"
    echo "2. Select tag: $TAG"
    echo "3. Copy title and notes from: $RELEASE_NOTES_FILE"
    echo "4. Publish release"
fi
