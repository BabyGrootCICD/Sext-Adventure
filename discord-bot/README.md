# Discord Bot 使用說明

## 📋 概述

Tsext Adventure Discord Bot 是一個自動化的貢獻者管理系統，用於：
- 自動分配貢獻者角色
- 追蹤 GitHub 貢獻
- 發送通知和更新
- 管理社區互動

## 🚀 快速開始

### 1. 環境設定

```bash
# 複製環境變數範例
cp env.example .env

# 編輯環境變數
nano .env
```

### 2. 安裝依賴

```bash
# 安裝 Python 依賴
pip install -r requirements.txt

# 或使用 Docker
docker-compose up -d
```

### 3. 設定 Discord Bot

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 創建新的應用程式
3. 在 Bot 頁面創建 Bot
4. 複製 Bot Token 到 `.env` 檔案
5. 在 OAuth2 > URL Generator 生成邀請連結
6. 邀請 Bot 到你的伺服器

### 4. 設定 GitHub Webhook

1. 前往專案的 Settings > Webhooks
2. 添加新的 Webhook
3. 設定 Payload URL: `https://your-domain.com/webhook`
4. 選擇事件: `Pull requests`, `Issues`
5. 複製 Webhook Secret 到 `.env` 檔案

### 5. 啟動 Bot

```bash
# 直接運行
python bot.py

# 或使用 Docker
docker-compose up -d discord-bot
```

## 🤖 Bot 命令

### 基本命令

- `!help` - 顯示幫助資訊
- `!link <github_username>` - 連結 GitHub 帳號
- `!update` - 更新貢獻者角色
- `!stats` - 查看貢獻統計

### 管理員命令

- `!sync-roles` - 同步所有角色
- `!list-contributors` - 列出所有貢獻者
- `!generate-report` - 生成貢獻者報告

## 🔧 配置

### 角色配置

編輯 `config.json` 來自定義角色：

```json
{
  "roles": {
    "maintainer": {
      "name": "👑 專案維護者",
      "color": "gold",
      "permissions": ["manage_messages", "manage_channels"],
      "description": "長期維護專案的核心成員"
    }
  }
}
```

### 頻道配置

設定通知頻道：

```json
{
  "channels": {
    "welcome": "welcome",
    "announcements": "announcements",
    "contributor-updates": "contributor-updates"
  }
}
```

## 📊 功能說明

### 自動角色分配

Bot 會根據以下標準自動分配角色：

| 等級 | 最低分數 | 最低 PR 數 | 描述 |
|------|----------|------------|------|
| 👑 維護者 | 50+ | 15+ | 長期維護專案的核心成員 |
| 🥇 核心貢獻者 | 20+ | 8+ | 重大功能開發者 |
| 🥈 活躍貢獻者 | 5+ | 2+ | 持續貢獻的社區成員 |
| 🥉 新手貢獻者 | 0+ | 0+ | 首次貢獻者 |

### Webhook 整合

Bot 會自動處理以下 GitHub 事件：

- **Pull Request 開啟/關閉/合併**
- **Issue 開啟/關閉**
- **貢獻者等級更新**

### 定期任務

- **每 24 小時**: 更新所有貢獻者角色
- **每 6 小時**: 檢查新的貢獻
- **每週**: 生成月度報告

## 🛠️ 開發

### 專案結構

```
discord-bot/
├── bot.py              # 主 Bot 程式
├── role_manager.py     # 角色管理
├── webhook_handler.py  # Webhook 處理
├── config.json         # 配置檔案
├── requirements.txt    # Python 依賴
├── Dockerfile         # Docker 配置
├── docker-compose.yml # Docker Compose
└── env.example        # 環境變數範例
```

### 添加新功能

1. 在 `bot.py` 中添加新命令
2. 在 `role_manager.py` 中添加角色邏輯
3. 在 `webhook_handler.py` 中添加事件處理
4. 更新 `config.json` 配置

### 測試

```bash
# 運行測試
python -m pytest tests/

# 測試 Webhook
curl -X POST http://localhost:5000/test
```

## 🚨 故障排除

### 常見問題

**Q: Bot 無法上線**
```
A: 檢查 DISCORD_BOT_TOKEN 是否正確設定
```

**Q: 角色無法分配**
```
A: 確保 Bot 有管理角色的權限
```

**Q: Webhook 無法接收事件**
```
A: 檢查 GITHUB_WEBHOOK_SECRET 和 URL 設定
```

### 日誌

```bash
# 查看 Bot 日誌
docker-compose logs discord-bot

# 查看 Webhook 日誌
docker-compose logs webhook-handler
```

### 除錯模式

啟用除錯模式：

```bash
# 設定環境變數
export DEBUG=True
export LOG_LEVEL=DEBUG

# 重新啟動
docker-compose restart
```

## 📚 API 參考

### Discord Bot API

```python
# 獲取用戶角色等級
role_level = await role_manager.get_user_role_level(member)

# 分配角色
success = await role_manager.assign_role_to_user(guild, member, 'core')

# 生成報告
report = await role_manager.generate_contributor_report(guild)
```

### Webhook API

```python
# 處理 PR 事件
await webhook_handler.handle_pull_request_event(payload)

# 處理 Issue 事件
await webhook_handler.handle_issue_event(payload)

# 發送通知
await webhook_handler.send_discord_notification(action, item, level)
```

## 🔒 安全性

### 權限設定

- Bot 只需要必要的權限
- 使用 Webhook Secret 驗證
- 限制 API 存取範圍

### 資料保護

- 不儲存敏感資訊
- 使用環境變數管理密鑰
- 定期更新依賴套件

## 📄 授權

本專案採用 MIT License。詳見 [LICENSE](../LICENSE) 檔案。
