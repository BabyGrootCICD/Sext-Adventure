#!/bin/bash
# Tsext Adventure: Halloween Haunt 部署腳本

echo "🎃 Tsext Adventure: Halloween Haunt 部署腳本 🎃"
echo "=================================================="

# 檢查是否在正確的目錄
if [ ! -f "main.py" ]; then
    echo "❌ 錯誤: 請在專案根目錄運行此腳本"
    exit 1
fi

# 創建部署目錄
echo "📁 創建部署目錄..."
mkdir -p deploy/github-pages
mkdir -p deploy/itch-io

# 複製 GitHub Pages 檔案
echo "🌐 準備 GitHub Pages 部署..."
cp web/index.html deploy/github-pages/
cp web/DEPLOYMENT.md deploy/github-pages/

# 複製 itch.io 檔案
echo "🎮 準備 itch.io 部署..."
cp web/index.html deploy/itch-io/
cp itch-deploy/README.md deploy/itch-io/

# 創建 ZIP 檔案
echo "📦 創建部署包..."
cd deploy/itch-io
zip -r ../tsext-adventure-itch-io.zip .
cd ../..

# 顯示部署資訊
echo ""
echo "✅ 部署準備完成！"
echo ""
echo "📁 部署檔案位置:"
echo "  • GitHub Pages: deploy/github-pages/"
echo "  • itch.io: deploy/itch-io/"
echo "  • itch.io ZIP: deploy/tsext-adventure-itch-io.zip"
echo ""
echo "🚀 部署步驟:"
echo ""
echo "GitHub Pages:"
echo "  1. 將 deploy/github-pages/ 的內容推送到 gh-pages 分支"
echo "  2. 或在 GitHub 設定中啟用 Pages"
echo ""
echo "itch.io:"
echo "  1. 上傳 deploy/tsext-adventure-itch-io.zip"
echo "  2. 設置專案資訊"
echo "  3. 發布遊戲"
echo ""
echo "🎃 Happy Deploying! 🎃"
