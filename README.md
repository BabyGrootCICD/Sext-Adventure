# Tsext Adventure: Halloween Haunt

![封面圖片](https://i.imgur.com/ti77o.jpg)  


[![GitHub release](https://img.shields.io/github/v/release/dennislee928/tsext-adventure.svg)](https://github.com/dennislee928/tsext-adventure/releases)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![GitHub stars](https://img.shields.io/github/stars/dennislee928/tsext-adventure.svg?style=social)](https://github.com/dennislee928/tsext-adventure/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/github/downloads/dennislee928/tsext-adventure/total.svg)](https://github.com/dennislee928/tsext-adventure/releases)

## 專案描述

**Tsext Adventure: Halloween Haunt** 是一個搞笑瑟瑟文字冒險遊戲的萬聖節特別版本！
- 玩家將在萬聖節夜晚參加一個「靈異約會趴」（haunted hookup party），透過文字選擇引導故事發展。
- 遊戲充滿成人幽默、雙關語（pun）和意外轉折。
- 例如試圖勾引女巫卻被掃帚掃飛，或是遇到饑渴鬼魂卻變成尷尬場面。

- **主題重點**：萬聖節元素（如鬼屋、南瓜田、巫師酒吧）結合 NSFW 搞笑，例如 "boo-ty call"（鬼魂版 booty call）或 "pumpkin spice and everything naughty"。
- **遊戲長度**：20-30 分鐘遊玩，包含 10-15 個分支結局，大多以荒謔失敗或高潮結束。
- **NSFW 警告**：本遊戲包含成人暗示和幽默，適合 18 歲以上玩家。無圖像內容，純文字。

[🌐 線上試玩 Demo](https://dennislee928.github.io/tsext-adventure/)  
[🎮 itch.io 版本](https://dennislee928.itch.io/tsext-adventure-halloween-haunt)  
*(直接在瀏覽器中試玩，無需下載！)*

## 為什麼玩這個遊戲？
- **搞笑元素**：每條故事路徑都融入萬聖節 pun，例如 "Why don't witches wear panties? So they can grip the broom better!" 或 "I'm light as a feather, and I can see you're stiff as a board."
- **互動性**：透過簡單選擇推進情節，適合手機或電腦遊玩。
- **社區貢獻**：我們鼓勵大家添加新故事分支、pun 或萬聖節梗！詳見貢獻指南。

## 安裝與運行

### 需求
- Python 3.8+（或 JavaScript，如果用 Twine 實作）
- 無需額外套件（基礎版使用標準庫）

### 步驟
1. **線上遊玩**（推薦）：
   - [GitHub Pages 版本](https://dennislee928.github.io/tsext-adventure/)
   - [itch.io 版本](https://dennislee928.itch.io/tsext-adventure-halloween-haunt)

2. **本地遊玩**：
   ```bash
   git clone https://github.com/dennislee928/tsext-adventure.git
   cd tsext-adventure
   python main.py
   ```

3. **Web 版本**：
   - 開啟 `web/index.html` 在瀏覽器運行
   - 或使用部署腳本：`./deploy.sh` (Linux/Mac) 或 `deploy.bat` (Windows)

## 專案架構

專案設計簡單易擴充，適合開源貢獻。以下是文件結構：

```
tsext-adventure/
├── README.md              # 本文件
├── LICENSE                # MIT 開源授權
├── main.py                # 主要遊戲腳本（Python 版）
├── demo.py                # 演示腳本
├── web/                   # Web 版本
│   ├── index.html         # 瀏覽器版本
│   └── DEPLOYMENT.md      # 部署指南
├── stories/               # 故事 JSON 檔案
│   ├── halloween.json     # 萬聖節故事分支
│   └── common.json        # 通用 pun 和結局資料庫
├── tests/                 # 測試腳本
│   └── test_stories.py    # 測試案例
├── docs/                  # 文件
│   ├── guides/            # 使用指南
│   ├── api/               # API 文件
│   └── examples/          # 範例
├── images/                # 圖像資源
│   ├── cover-design.md    # 封面設計說明
│   └── badges/            # 徽章資料夾
├── .github/workflows/     # GitHub Actions
│   └── deploy.yml         # 自動部署
├── itch-deploy/           # itch.io 部署包
└── CONTRIBUTING.md        # 貢獻指南
```

- **stories/**：故事以 JSON 格式儲存，便於貢獻新分支。例如：
  ```json
  {
    "scene": "鬼屋入口",
    "choices": [
      {"option": "A: 親吻鬼魂", "outcome": "尷尬結局：鬼魂變成鼻涕鬼！"},
      {"option": "B: 逃跑", "outcome": "搞笑逃脫：絆倒南瓜燈..."}
    ]
  }
  ```
- **tests/**：使用 pytest 測試故事連貫性。
- **docs/**：未來添加詳細文件，使用如 Docusaurus。

## 貢獻指南

我們歡迎貢獻！特別是萬聖節限定挑戰（Halloween Hacktoberfest）：
- **好入門議題**：標籤 `good-first-issue`，如添加新 pun 或結局。
- **如何貢獻**：
  1. Fork repo。
  2. 建立分支：`git checkout -b add-new-pun`。
  3. 修改 `stories/halloween.json` 添加內容。
  4. 提交 PR，並描述你的搞笑想法。
- **徵求**：新故事分支、萬聖節梗、bug 修復。
- 社區投票最搞笑貢獻！

詳見 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 授權

本專案採用 [MIT License](LICENSE)。歡迎 fork 和分享，但請保留 NSFW 警告。

## 聯絡與社群

- Discord：加入 [Tsext Community](https://discord.gg/yourinvite) 討論新想法。
- Twitter：[@tsext_adventure](https://x.com/lee66876613) – 分享你的搞笑結局！
- 問題回報：開 GitHub Issue。

給個星星 ⭐ 如果你覺得有趣！這能幫助我們上 GitHub Trending。
