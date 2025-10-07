# 🧹 GitHub Pages 快取問題 - 快速修復指南

## ⚡ 緊急修復（5分鐘解決）

### 使用者端解決方案
1. **強制重新整理**
   - Windows/Linux: `Ctrl + F5`
   - Mac: `Cmd + Shift + R`
   - 手機: 長按重新整理 → 選擇「重新載入」

2. **無痕模式**
   - 開啟瀏覽器無痕/隱私模式

3. **版本檢查**
   - 訪問：`/version-check.html`
   - 確認版本號是否為最新

### 開發者端解決方案
```bash
# 一鍵快取清除
./scripts/cache-buster.sh purge

# 檢查版本狀態
./scripts/cache-buster.sh status

# 強制重新部署
./scripts/cache-buster.sh force
```

## 🚀 部署流程

### 自動部署（推薦）
```bash
# 執行部署腳本（含快取管理）
./deploy.sh

# Windows 版本
deploy.bat
```

### 手動部署
```bash
# 1. 更新版本
python3 scripts/version-manager.py

# 2. 推送到 GitHub
git add .
git commit -m "🚀 部署更新 - $(date)"
git push origin main

# 3. 等待 5-10 分鐘讓 CDN 更新
```

## 🔍 問題診斷

### 檢查清單
- [ ] 版本號是否更新？
- [ ] 部署時間戳是否正確？
- [ ] GitHub Actions 是否成功？
- [ ] 版本檢查頁面是否可訪問？

### 常見錯誤
| 問題 | 原因 | 解決方案 |
|------|------|----------|
| 看到舊版本 | 瀏覽器快取 | Ctrl+F5 強制重新整理 |
| 版本檢查失敗 | 頁面未部署 | 等待 5-10 分鐘 |
| 部署失敗 | GitHub Actions 錯誤 | 檢查 Actions 日誌 |

## 📞 緊急聯絡

- **版本檢查**: `/version-check.html`
- **快取指南**: `/cache-info.md`
- **GitHub Issues**: 技術問題回報

---
*最後更新: 2025-01-06*
