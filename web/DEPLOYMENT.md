# GitHub Pages 部署指南

## 🚀 部署到 GitHub Pages

### 方法 1: 使用 GitHub Actions (推薦)

1. **創建 GitHub Actions 工作流程**
   - 在專案根目錄創建 `.github/workflows/deploy.yml`
   - 每次推送到 `main` 分支時自動部署

2. **設置步驟**
   ```bash
   # 1. 確保你的專案在 GitHub 上
   git add .
   git commit -m "Add web version for GitHub Pages"
   git push origin main
   
   # 2. 在 GitHub 設定中啟用 Pages
   # Settings > Pages > Source: GitHub Actions
   ```

### 方法 2: 手動部署

1. **切換到 gh-pages 分支**
   ```bash
   git checkout -b gh-pages
   ```

2. **複製 web 檔案到根目錄**
   ```bash
   cp web/index.html .
   cp -r web/assets .  # 如果有額外資源
   ```

3. **提交並推送**
   ```bash
   git add .
   git commit -m "Deploy web version"
   git push origin gh-pages
   ```

## 🎮 部署到 itch.io

### 步驟 1: 準備檔案
```bash
# 創建部署資料夾
mkdir itch-deploy
cp web/index.html itch-deploy/
# 如果有額外資源，也複製過去
```

### 步驟 2: 上傳到 itch.io
1. 登入 [itch.io](https://itch.io)
2. 創建新專案
3. 上傳 `index.html` 檔案
4. 設置專案資訊：
   - 標題: "Tsext Adventure: Halloween Haunt"
   - 描述: "搞笑瑟瑟文字冒險遊戲的萬聖節特別版本"
   - 標籤: "text-adventure", "halloween", "nsfw", "comedy"
   - 價格: 免費或付費

### 步驟 3: 發布設定
- **Kind**: HTML
- **Embed**: 選擇 "This file will be played in the browser"
- **Visibility**: Public

## 📱 優化建議

### 移動裝置優化
- 響應式設計已包含
- 觸控友好的按鈕
- 適合手機螢幕的佈局

### 效能優化
- 壓縮 HTML/CSS/JS
- 使用 CDN 載入字體
- 優化圖片大小

### SEO 優化
- 添加 meta 標籤
- 結構化資料
- 社交媒體分享標籤

## 🔧 自訂部署

### 添加更多功能
```javascript
// 在 index.html 中添加
- 音效支援
- 動畫效果
- 存檔功能
- 多語言支援
```

### 整合分析
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>

<!-- 或使用其他分析工具 -->
```

## 📊 部署後檢查清單

- [ ] 遊戲正常載入
- [ ] 所有場景都能正常顯示
- [ ] 選擇按鈕正常工作
- [ ] 結局正確顯示
- [ ] 重新開始功能正常
- [ ] 移動裝置相容性
- [ ] 載入速度合理
- [ ] 沒有 JavaScript 錯誤

## 🌐 部署 URL

### GitHub Pages
```
https://yourusername.github.io/tsext-adventure/
```

### itch.io
```
https://yourusername.itch.io/tsext-adventure-halloween-haunt
```

## 🎯 推廣建議

### 社交媒體
- Twitter: 分享遊戲連結和截圖
- Reddit: 在相關社群分享
- Discord: 在遊戲社群推廣

### 內容創作
- 創建遊戲預告影片
- 寫遊戲評測文章
- 製作遊戲攻略

---

**🎃 Happy Deploying! 🎃**
