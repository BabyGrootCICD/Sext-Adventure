# 貢獻者追蹤系統使用說明

## 📋 概述

貢獻者追蹤系統是一個自動化的 GitHub 整合工具，用於：
- 追蹤和分類專案貢獻者
- 自動更新 README.md 中的貢獻者區塊
- 生成月度貢獻報告
- 提供貢獻者認可機制

## 🚀 快速開始

### 1. 環境設定

```bash
# 安裝依賴
pip install -r requirements.txt

# 設定 GitHub Token（可選，用於提高 API 限制）
export GITHUB_TOKEN="your_github_token_here"
```

### 2. 基本使用

```bash
# 更新貢獻者數據
python scripts/track_contributors.py

# 只獲取 GitHub API 數據
python scripts/github_api.py
```

### 3. 自動化設定

系統已配置 GitHub Actions 工作流程，會：
- 每週一自動更新貢獻者數據
- 生成月度報告
- 自動提交更改到 README.md

## 📊 功能說明

### GitHub API 整合

`scripts/github_api.py` 提供以下功能：

```python
from scripts.github_api import GitHubAPI, ContributorTracker

# 初始化 API 客戶端
api = GitHubAPI(token="your_token")
tracker = ContributorTracker(api, "owner", "repo")

# 獲取貢獻者數據
contributors = api.get_contributors("owner", "repo")

# 分類貢獻者
categories = tracker.categorize_contributors()

# 生成 Markdown
markdown = tracker.generate_contributors_markdown(categories)
```

### 貢獻者分類

系統根據以下標準分類貢獻者：

| 等級 | 最低分數 | 最低 PR 數 | 描述 |
|------|----------|------------|------|
| 👑 維護者 | 50+ | 15+ | 長期維護專案的核心成員 |
| 🥇 核心貢獻者 | 20+ | 8+ | 重大功能開發者 |
| 🥈 活躍貢獻者 | 5+ | 2+ | 持續貢獻的社區成員 |
| 🥉 新手貢獻者 | 0+ | 0+ | 首次貢獻者 |

### 月度統計

系統會分析以下類型的貢獻：

- **🎭 故事內容**: 故事場景、劇情內容
- **🛠️ 技術改進**: 功能增強、技術優化
- **🐛 Bug 修復**: 錯誤修復、問題解決
- **🎨 UI 設計**: 界面改進、用戶體驗
- **🌟 社區幫助**: 回答問題、提供支援

## ⚙️ 配置

### 修改倉庫資訊

編輯 `scripts/github_api.py` 中的設定：

```python
OWNER = "your_github_username"  # 替換為實際的 GitHub 用戶名
REPO = "your_repository_name"    # 替換為實際的倉庫名
```

### 自定義分類標準

編輯 `config/contributor_config.json`：

```json
{
  "contribution_levels": {
    "maintainer": {
      "min_score": 50,
      "min_prs": 15,
      "description": "長期維護專案的核心成員"
    }
  }
}
```

### GitHub Actions 排程

編輯 `.github/workflows/update-contributors.yml`：

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'  # 每週一早上 9:00 UTC
```

## 🧪 測試

運行測試套件：

```bash
# 運行所有測試
python -m pytest tests/

# 運行特定測試
python tests/test_contributor_tracking.py

# 運行 GitHub API 測試
python tests/test_stories.py
```

## 📈 月度報告

系統會自動生成月度報告，包含：

1. **本月之星**: 各類別的最佳貢獻者
2. **詳細統計**: 所有貢獻者的詳細數據
3. **趨勢分析**: 貢獻模式和增長趨勢

報告會保存為 `monthly_report_YYYY_MM.md` 格式。

## 🔧 故障排除

### 常見問題

**Q: GitHub API 限制錯誤**
```
A: 設定 GITHUB_TOKEN 環境變數以提高 API 限制
```

**Q: 找不到貢獻者數據**
```
A: 檢查倉庫名稱和擁有者是否正確
```

**Q: README.md 更新失敗**
```
A: 確保有寫入權限，檢查檔案路徑
```

### 除錯模式

啟用詳細日誌：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 手動測試

```bash
# 測試 GitHub API 連接
python -c "
from scripts.github_api import GitHubAPI
api = GitHubAPI()
print(api.get_repo_info('BabyGrootCICD', 'Sext-Adventure'))
"
```

## 📚 API 參考

### GitHubAPI 類別

```python
class GitHubAPI:
    def get_repo_info(owner: str, repo: str) -> Dict
    def get_contributors(owner: str, repo: str) -> List[Dict]
    def get_pull_requests(owner: str, repo: str, state: str = 'all') -> List[Dict]
    def get_issues(owner: str, repo: str, state: str = 'all') -> List[Dict]
    def get_user_pr_count(owner: str, repo: str, username: str) -> int
    def get_user_issue_count(owner: str, repo: str, username: str) -> int
```

### ContributorTracker 類別

```python
class ContributorTracker:
    def categorize_contributors() -> Dict[str, List[Dict]]
    def generate_contributors_markdown(categories: Dict) -> str
    def get_monthly_stats(days: int = 30) -> Dict[str, Dict]
```

### READMEUpdater 類別

```python
class READMEUpdater:
    def read_readme() -> str
    def write_readme(content: str)
    def find_contributors_section(content: str) -> tuple
    def update_contributors_section(content: str, new_markdown: str) -> str
    def add_contribution_stats(content: str, stats: Dict) -> str
```

## 🤝 貢獻

歡迎為貢獻者追蹤系統貢獻代碼！

1. Fork 專案
2. 創建功能分支
3. 提交更改
4. 發送 Pull Request

詳見 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📄 授權

本專案採用 MIT License。詳見 [LICENSE](../LICENSE) 檔案。
