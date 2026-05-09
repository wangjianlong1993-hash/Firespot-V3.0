#!/bin/bash

# FireSpot v7.2 - GitHub Release Package Creation Script
# This script creates a distributable package for GitHub release

set -e

VERSION="7.2.0"
PACKAGE_NAME="firespot-v${VERSION}"
OUTPUT_DIR="./release"

echo "🔥 FireSpot v${VERSION} - Package Creation"
echo "=========================================="
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📦 Creating package: ${PACKAGE_NAME}"

# Create temporary directory for packaging
TEMP_DIR=$(mktemp -d)
echo "Using temporary directory: $TEMP_DIR"

# Copy all files to temp directory
echo "Copying files..."
rsync -av \
    --exclude='.git' \
    --exclude='.DS_Store' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.gitignore' \
    --exclude='release' \
    --exclude='*.log' \
    ./ "$TEMP_DIR/${PACKAGE_NAME}/"

# Create package archive
echo "Creating archive..."
cd "$TEMP_DIR"
tar -czf "${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz" "${PACKAGE_NAME}"
zip -rq "${OUTPUT_DIR}/${PACKAGE_NAME}.zip" "${PACKAGE_NAME}"
cd - > /dev/null

# Calculate checksums
echo "Calculating checksums..."
cd "$OUTPUT_DIR"
shasum -a 256 "${PACKAGE_NAME}.tar.gz" > "${PACKAGE_NAME}.sha256"
shasum -a 512 "${PACKAGE_NAME}.tar.gz" > "${PACKAGE_NAME}.sha512"
md5 "${PACKAGE_NAME}.tar.gz" > "${PACKAGE_NAME}.md5"
cd - > /dev/null

# Get file sizes
TAR_SIZE=$(du -h "${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz" | cut -f1)
ZIP_SIZE=$(du -h "${OUTPUT_DIR}/${PACKAGE_NAME}.zip" | cut -f1)

# Clean up temp directory
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Package creation complete!"
echo ""
echo "📦 Package Information:"
echo "  Name: ${PACKAGE_NAME}"
echo "  Version: ${VERSION}"
echo "  Output Directory: ${OUTPUT_DIR}"
echo ""
echo "📁 Created Files:"
echo "  - ${PACKAGE_NAME}.tar.gz (${TAR_SIZE})"
echo "  - ${PACKAGE_NAME}.zip (${ZIP_SIZE})"
echo "  - ${PACKAGE_NAME}.sha256"
echo "  - ${PACKAGE_NAME}.sha512"
echo "  - ${PACKAGE_NAME}.md5"
echo ""
echo "🔐 Checksums:"
cat "${OUTPUT_DIR}/${PACKAGE_NAME}.sha256"
echo ""
echo "📋 Next Steps:"
echo "1. Test the package: tar -xzf ${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz"
echo "2. Upload to GitHub Release"
echo "3. Update GitHub Release page with package information"
echo ""
echo -e "${GREEN}🎉 FireSpot v${VERSION} package ready for distribution!${NC}"