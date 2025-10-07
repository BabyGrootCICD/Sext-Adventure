#!/bin/bash
# GitHub Pages 快取清除腳本
# 版本: 1.0.5
# 建置時間: 2025-01-06T00:00:00.000000

echo "🧹 GitHub Pages 快取清除工具"
echo "版本: 1.0.5"
echo "=================================="

# 方法 1: 強制重新整理提示
echo "📱 使用者端解決方案:"
echo "1. 按 Ctrl+F5 (Windows/Linux) 或 Cmd+Shift+R (Mac) 強制重新整理"
echo "2. 開啟無痕模式瀏覽網站"
echo "3. 清除瀏覽器快取"

# 方法 2: 等待 CDN 更新
echo ""
echo "⏰ 伺服器端解決方案:"
echo "1. 等待 5-10 分鐘讓 CDN 更新"
echo "2. 使用不同網路環境測試"
echo "3. 檢查版本號是否更新"

# 檢查版本
echo ""
echo "🔍 版本檢查:"
echo "當前版本: 1.0.5"
echo "建置時間: 2025-01-06T00:00:00.000000"

# 建立版本檢查頁面
cat > deploy/github-pages/version-check.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>版本檢查 - Tsext Adventure</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
</head>
<body>
    <h1>版本檢查</h1>
    <p>當前版本: 1.0.5</p>
    <p>建置時間: 2025-01-06T00:00:00.000000</p>
    <p>如果看到舊版本，請按 Ctrl+F5 強制重新整理</p>
    <script>
        console.log('版本檢查頁面載入時間:', new Date().toISOString());
    </script>
</body>
</html>
EOF

echo "✅ 快取清除腳本建立完成"
echo "📁 檔案位置: deploy/github-pages/cache-buster.sh"
echo "🌐 版本檢查: deploy/github-pages/version-check.html"
