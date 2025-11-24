# 📊 Community Pulse Reporter

[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-Community%20Pulse%20Reporter-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=github)](https://github.com/marketplace/actions/community-pulse-reporter)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**自動生成社群貢獻報告與排行榜 | Automatically generate community contribution reports and leaderboards**

一個專為開源專案維護者設計的 GitHub Action，可自動分析貢獻者數據、生成精美的 Markdown 報告與排行榜，激勵社群參與！

A GitHub Action designed for open-source maintainers to automatically analyze contributor data, generate beautiful Markdown reports and leaderboards, and motivate community engagement!

---

## ✨ 功能特色 | Features

- 🎯 **全面分析** - 追蹤 PRs、Issues、Commits 等所有貢獻活動
- 🏆 **排行榜系統** - 自動生成貢獻者排行榜，展示頭部貢獻者
- 📊 **詳細統計** - 提供多維度的貢獻數據分析
- 📝 **Markdown 報告** - 生成美觀的 Markdown 格式報告
- ⚙️ **靈活配置** - 支援自定義時間範圍、輸出路徑等
- 🚀 **即插即用** - 簡單配置，5 分鐘完成設置

---

## 🚀 快速開始 | Quick Start

### 基礎使用 | Basic Usage

在你的專案中創建 `.github/workflows/community-report.yml`：

```yaml
name: Generate Community Report

on:
  schedule:
    # 每月 1 號生成報告
    - cron: '0 0 1 * *'
  workflow_dispatch: # 允許手動觸發

jobs:
  generate-report:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Generate Community Pulse Report
        uses: dennislee928/Sext-Adventure@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          interval: '30'
          output_file: 'COMMUNITY_REPORT.md'
      
      - name: Commit report
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add COMMUNITY_REPORT.md
          git commit -m "📊 Update community report" || exit 0
          git push
```

### 進階配置 | Advanced Configuration

```yaml
- name: Generate Community Pulse Report
  uses: dennislee928/Sext-Adventure@main
  with:
    # GitHub Token（必需）
    github_token: ${{ secrets.GITHUB_TOKEN }}
    
    # 倉庫擁有者（預設為當前倉庫）
    repo_owner: ${{ github.repository_owner }}
    
    # 倉庫名稱（預設為當前倉庫）
    repo_name: ${{ github.event.repository.name }}
    
    # 分析時間範圍：數字（天數）或關鍵字
    # 支援: '7', '30', '365', 'week', 'month', 'year'
    interval: '30'
    
    # 輸出文件路徑
    output_file: 'COMMUNITY_REPORT.md'
    
    # 是否包含詳細統計
    include_stats: 'true'
```

---

## 📋 輸入參數 | Inputs

| 參數 | 必需 | 預設值 | 說明 |
|------|------|--------|------|
| `github_token` | ✅ | - | GitHub Token，使用 `secrets.GITHUB_TOKEN` |
| `repo_owner` | ❌ | 當前倉庫擁有者 | 要分析的倉庫擁有者 |
| `repo_name` | ❌ | 當前倉庫名稱 | 要分析的倉庫名稱 |
| `interval` | ❌ | `30` | 分析時間範圍（天數或關鍵字） |
| `output_file` | ❌ | `COMMUNITY_REPORT.md` | 報告輸出路徑 |
| `include_stats` | ❌ | `true` | 是否包含詳細統計 |

### 時間間隔選項 | Interval Options

- **數字**: `7`, `30`, `90`, `365` 等（代表天數）
- **關鍵字**: 
  - `week` / `last_week` - 最近 7 天
  - `month` / `last_month` - 最近 30 天
  - `year` / `last_year` - 最近 365 天

---

## 📤 輸出參數 | Outputs

| 輸出 | 說明 |
|------|------|
| `report_file` | 生成的報告文件路徑 |
| `total_contributors` | 活躍貢獻者總數 |
| `total_prs` | Pull Request 總數 |
| `total_issues` | Issue 總數 |

### 使用輸出 | Using Outputs

```yaml
- name: Generate Community Pulse Report
  id: report
  uses: dennislee928/Sext-Adventure@main
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}

- name: Display Stats
  run: |
    echo "Total Contributors: ${{ steps.report.outputs.total_contributors }}"
    echo "Total PRs: ${{ steps.report.outputs.total_prs }}"
    echo "Total Issues: ${{ steps.report.outputs.total_issues }}"
```

---

## 📊 報告範例 | Report Example

生成的報告包含以下內容：

### 1️⃣ 總覽 | Overview

顯示關鍵指標：
- 活躍貢獻者數量
- PR 和 Issue 統計
- Commit 數量
- PR 合併率

### 2️⃣ 排行榜 | Leaderboard

展示前 10 名貢獻者：
- 🥇 第一名
- 🥈 第二名  
- 🥉 第三名
- 包含 PRs、Issues、Commits 詳細數據

### 3️⃣ 類別分析 | Category Breakdown

按貢獻類型分類：
- ✨ 新功能 (Features)
- 🐛 Bug 修復 (Bug Fixes)
- 📖 文檔 (Documentation)
- ⚡ 改進 (Enhancements)
- 📦 其他 (Others)

### 4️⃣ 詳細統計 | Detailed Statistics

完整的貢獻者列表與數據

[查看完整報告範例 →](./COMMUNITY_REPORT.md)

---

## 🎯 使用場景 | Use Cases

### 1. 月度社群報告

```yaml
on:
  schedule:
    - cron: '0 0 1 * *' # 每月 1 號
```

### 2. 季度績效總結

```yaml
with:
  interval: '90' # 90 天
  output_file: 'Q1_REPORT.md'
```

### 3. 即時監控

```yaml
on:
  push:
    branches: [main]
```

### 4. 週報生成

```yaml
on:
  schedule:
    - cron: '0 9 * * 1' # 每週一早上 9 點
with:
  interval: 'week'
  output_file: 'WEEKLY_REPORT.md'
```

---

## 🔧 進階技巧 | Advanced Tips

### 1. 自動發布 Release

```yaml
- name: Generate Report
  id: report
  uses: dennislee928/Sext-Adventure@main
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}

- name: Create Release
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: report-${{ github.run_number }}
    release_name: Community Report ${{ github.run_number }}
    body_path: COMMUNITY_REPORT.md
```

### 2. 通知到 Slack

```yaml
- name: Send to Slack
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "📊 新的社群報告已生成！\n活躍貢獻者: ${{ steps.report.outputs.total_contributors }}\nPRs: ${{ steps.report.outputs.total_prs }}"
      }
```

### 3. 多倉庫分析

```yaml
strategy:
  matrix:
    repo: ['repo1', 'repo2', 'repo3']
steps:
  - name: Generate Report
    uses: dennislee928/Sext-Adventure@main
    with:
      github_token: ${{ secrets.GITHUB_TOKEN }}
      repo_name: ${{ matrix.repo }}
      output_file: 'reports/${{ matrix.repo }}_REPORT.md'
```

---

## 💡 評分規則 | Scoring Rules

貢獻分數計算方式：

- **已合併 PR (Merged PR)**: 5 分
- **PR (Pull Request)**: 3 分
- **Commit**: 2 分
- **Issue**: 1 分

> 此評分系統旨在激勵高質量的代碼貢獻，同時也認可問題回報和討論參與。

---

## 🤝 貢獻 | Contributing

歡迎提交 Issues 和 Pull Requests！

### 本地開發

```bash
# Clone repository
git clone https://github.com/dennislee928/Sext-Adventure.git
cd Sext-Adventure

# Install dependencies
pip install -r requirements.txt

# Test locally
python action_entrypoint.py
```

---

## 📝 License

本專案採用 [MIT License](LICENSE)。

---

## 🌟 關於 | About

此 Action 源自 [Tsext Adventure](https://github.com/dennislee928/Sext-Adventure) 專案的貢獻者追蹤系統，經過重構和優化，現在可以為任何開源專案提供社群分析服務。

Developed with ❤️ by [Tsext Adventure Team](https://github.com/dennislee928)

---

## 📞 支援 | Support

- 🐛 [回報 Bug](https://github.com/dennislee928/Sext-Adventure/issues)
- 💡 [功能建議](https://github.com/dennislee928/Sext-Adventure/issues)
- 📖 [查看文檔](https://github.com/dennislee928/Sext-Adventure)
- ⭐ [給我們一個星星](https://github.com/dennislee928/Sext-Adventure)

---

**讓我們一起建設更好的開源社群！| Let's build better open-source communities together!** 🚀

