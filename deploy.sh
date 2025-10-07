#!/bin/bash
# Tsext Adventure: Halloween Haunt 部署腳本 (含快取管理)

echo "🎃 Tsext Adventure: Halloween Haunt 部署腳本 🎃"
echo "=================================================="

# 檢查是否在正確的目錄
if [ ! -f "main.py" ]; then
    echo "❌ 錯誤: 請在專案根目錄運行此腳本"
    exit 1
fi

# 快取管理功能
CACHE_MANAGEMENT=true
VERSION_FILE="version.json"
DEPLOY_TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "🚀 開始部署流程 (含快取管理)"
echo "部署時間戳: $DEPLOY_TIMESTAMP"

# 版本管理和快取清除
if [ "$CACHE_MANAGEMENT" = true ]; then
    echo "🔧 執行版本管理和快取清除..."
    
    # 執行版本管理腳本
    if [ -f "scripts/version-manager.py" ]; then
        echo "📝 更新版本號..."
        python3 scripts/version-manager.py
    else
        echo "⚠️  警告: 版本管理腳本不存在，跳過版本更新"
    fi
    
    # 建立快取清除檔案
    echo "🧹 建立快取清除檔案..."
    cat > deploy/cache-info.md << EOF
# GitHub Pages 快取清除指南

## 🚀 部署資訊
- **部署時間**: $DEPLOY_TIMESTAMP
- **版本檔案**: $VERSION_FILE
- **快取管理**: 已啟用

## 🧹 即時解決方法

### 1. 強制重新整理
- **Windows/Linux**: Ctrl + F5 或 Ctrl + Shift + R
- **Mac**: Cmd + Shift + R
- **手機**: 長按重新整理按鈕選擇「重新載入」

### 2. 無痕模式
開啟瀏覽器的無痕/隱私模式瀏覽網站

### 3. 清除瀏覽器快取
手動清除瀏覽器的快取資料

## ⏰ 等待 CDN 更新
GitHub Pages CDN 通常需要 5-10 分鐘更新

## 🔍 版本檢查
訪問 \`/version-check.html\` 檢查當前版本

---
*自動生成於 $DEPLOY_TIMESTAMP*
EOF
fi

# 創建部署目錄
echo "📁 創建部署目錄..."
mkdir -p deploy/github-pages
mkdir -p deploy/itch-io

# 複製 GitHub Pages 檔案 (含快取管理)
echo "🌐 準備 GitHub Pages 部署..."
cp web/index.html deploy/github-pages/
cp web/DEPLOYMENT.md deploy/github-pages/

# 加入快取管理檔案
if [ "$CACHE_MANAGEMENT" = true ]; then
    cp deploy/cache-info.md deploy/github-pages/
    cp $VERSION_FILE deploy/github-pages/ 2>/dev/null || echo "⚠️  版本檔案不存在"
    
    # 建立版本檢查頁面
    cat > deploy/github-pages/version-check.html << EOF
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
    <title>版本檢查 - Tsext Adventure</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #1a1a2e; color: #fff; }
        .container { max-width: 600px; margin: 0 auto; }
        .version-info { background: #333; padding: 20px; border-radius: 10px; margin: 20px 0; }
        .timestamp { color: #ff6b35; font-weight: bold; }
        .instructions { background: #2a2a4e; padding: 15px; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎃 Tsext Adventure - 版本檢查</h1>
        
        <div class="version-info">
            <h2>📊 當前版本資訊</h2>
            <p><strong>頁面載入時間:</strong> <span class="timestamp" id="loadTime"></span></p>
            <p><strong>部署時間戳:</strong> <span class="timestamp">$DEPLOY_TIMESTAMP</span></p>
            <p><strong>瀏覽器快取:</strong> <span id="cacheStatus">檢查中...</span></p>
        </div>
        
        <div class="instructions">
            <h3>🧹 如果看到舊版本，請嘗試：</h3>
            <ul>
                <li>按 <strong>Ctrl+F5</strong> (Windows/Linux) 或 <strong>Cmd+Shift+R</strong> (Mac) 強制重新整理</li>
                <li>開啟無痕模式瀏覽</li>
                <li>清除瀏覽器快取</li>
                <li>等待 5-10 分鐘讓 CDN 更新</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="index.html" style="color: #ff6b35; text-decoration: none; font-size: 1.2em;">
                🎮 回到遊戲
            </a>
        </div>
    </div>
    
    <script>
        document.getElementById('loadTime').textContent = new Date().toISOString();
        
        // 檢查快取狀態
        if ('caches' in window) {
            caches.keys().then(function(cacheNames) {
                const cacheCount = cacheNames.length;
                document.getElementById('cacheStatus').textContent = 
                    cacheCount > 0 ? \`找到 \${cacheCount} 個快取\` : '無快取';
            });
        } else {
            document.getElementById('cacheStatus').textContent = '瀏覽器不支援快取 API';
        }
        
        // 記錄頁面載入
        console.log('版本檢查頁面載入:', new Date().toISOString());
        console.log('部署時間戳:', '$DEPLOY_TIMESTAMP');
    </script>
</body>
</html>
EOF
fi

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

# 快取管理資訊
if [ "$CACHE_MANAGEMENT" = true ]; then
    echo "🧹 快取管理功能:"
    echo "  • 版本檢查頁面: deploy/github-pages/version-check.html"
    echo "  • 快取清除指南: deploy/github-pages/cache-info.md"
    echo "  • 版本檔案: deploy/github-pages/version.json"
    echo ""
    echo "🔍 版本資訊:"
    if [ -f "$VERSION_FILE" ]; then
        VERSION=$(python3 -c "import json; print(json.load(open('$VERSION_FILE'))['version'])" 2>/dev/null || echo "未知")
        echo "  • 當前版本: $VERSION"
    fi
    echo "  • 部署時間戳: $DEPLOY_TIMESTAMP"
    echo ""
fi

echo "🚀 部署步驟:"
echo ""
echo "GitHub Pages:"
echo "  1. 將 deploy/github-pages/ 的內容推送到 gh-pages 分支"
echo "  2. 或在 GitHub 設定中啟用 Pages"
echo "  3. 等待 5-10 分鐘讓 CDN 更新"
echo "  4. 訪問 /version-check.html 檢查版本"
echo ""
echo "itch.io:"
echo "  1. 上傳 deploy/tsext-adventure-itch-io.zip"
echo "  2. 設置專案資訊"
echo "  3. 發布遊戲"
echo ""

# 快取問題解決提示
if [ "$CACHE_MANAGEMENT" = true ]; then
    echo "⚠️  快取問題解決提示:"
    echo "  • 如果使用者看到舊版本，請他們按 Ctrl+F5 強制重新整理"
    echo "  • 或提供 /version-check.html 連結讓他們檢查版本"
    echo "  • 等待 5-10 分鐘讓 GitHub Pages CDN 更新"
    echo ""
fi

echo "🎃 Happy Deploying! 🎃"
