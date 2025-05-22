#!/bin/bash

# Pavel Hrdina 2025

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="game_package_$TIMESTAMP"
DIST_DIR="dist"

echo "Cleaning __pycache__ folders..."
find . -name "__pycache__" -type d -exec rm -r {} +

echo "Removing optional dev files from venv..."
rm -rf venv/lib/python*/site-packages/pip
rm -rf venv/lib/python*/site-packages/setuptools
rm -rf venv/share
rm -rf venv/include

echo "Creating dist directory..."
mkdir -p "$DIST_DIR"

echo "Creating tar.gz archive..."
tar --warning=no-file-changed \
    --exclude='./dist' \
    --exclude='./*.tar.gz' \
    --exclude='./*.zip' \
    --exclude='./.git' \
    --exclude='./__pycache__' \
    -czf "$DIST_DIR/$PACKAGE_NAME.tar.gz" .

echo "Creating zip archive..."
zip -r "$DIST_DIR/$PACKAGE_NAME.zip" . \
    -x "dist/*" "*.tar.gz" "*.zip" ".git/*" "__pycache__/*"

echo "Packaging complete:"
ls -lh "$DIST_DIR"
