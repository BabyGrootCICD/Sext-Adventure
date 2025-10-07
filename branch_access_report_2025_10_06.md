# 🔐 Tsext Adventure 分支存取權限報告

## 📊 存取權限概覽

### 核心存取權限 - 主要分支和功能分支

**@dennislee928**
- 可存取分支: main, dev, feature/*, hotfix/*
- 權限: push, merge, create_branch

## 🔒 分支保護規則

### main 分支
- 必需狀態檢查: ci, tests, lint
- 必需審查數: 2
- 限制用戶: maintainer1, maintainer2

### dev 分支
- 必需狀態檢查: ci, tests
- 必需審查數: 1
- 限制用戶: maintainer1, core1, core2


## 📋 存取權限等級說明

| 等級 | 可存取分支 | 主要權限 | 描述 |
|------|------------|----------|------|
| 👑 維護者 | 所有分支 | 完整權限 | 可以推送到任何分支，包括 main |
| 🥇 核心貢獻者 | main, dev, feature/* | 推送 + 合併 | 可以推送到主要分支 |
| 🥈 活躍貢獻者 | dev, feature/* | 推送 | 可以推送到開發分支 |
| 🥉 新手貢獻者 | feature/* | 推送 | 只能推送到功能分支 |

## 🚀 如何請求存取權限

1. **自動存取**: 根據你的貢獻者等級自動獲得相應權限
2. **手動請求**: 創建 Issue 標記 `branch-access-request`
3. **PR 請求**: 通過 Pull Request 請求存取特定分支

---

*報告生成時間: 2025-10-06 23:33:24*  
*Tsext Adventure 分支存取控制系統*
