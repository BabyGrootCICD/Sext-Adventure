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

## 🤝 詳細貢獻指南

我們熱烈歡迎社區貢獻！無論你是程式新手還是資深開發者，都有適合的貢獻方式。

### 📋 貢獻類型

#### 🎭 故事內容貢獻
- **新故事分支**：創建全新的萬聖節冒險路線
- **結局擴展**：為現有路線添加更多結局選項  
- **雙關語梗**：萬聖節主題的NSFW搞笑內容
- **角色對話**：豐富NPC的個性和互動
- **成就系統**：設計新的成就和獎勵機制

#### 💻 技術改進
- **UI/UX 優化**：改善使用者介面和體驗
- **效能優化**：提升遊戲載入速度和響應性
- **新功能**：音效、動畫、存檔等進階功能
- **跨平台**：支援更多裝置和瀏覽器
- **無障礙**：提升可訪問性和包容性

#### 🐛 Bug修復與測試
- **錯誤回報**：發現並回報遊戲中的問題
- **修復實作**：解決已知的技術問題
- **測試覆蓋**：增加自動化測試
- **相容性**：確保跨瀏覽器相容性

### 🎯 快速開始 (5分鐘貢獻)

#### 方式一：簡單故事貢獻
```bash
# 1. Fork 並 clone 專案
git clone https://github.com/your-username/tsext-adventure.git
cd tsext-adventure

# 2. 創建新分支
git checkout -b add-my-story-idea

# 3. 編輯故事檔案 (選擇以下任一)
# 選項 A：直接編輯 web/index.html (簡單)
# 選項 B：編輯 stories/halloween.json (傳統)

# 4. 測試你的更改
# 開啟 web/index.html 在瀏覽器中測試

# 5. 提交更改
git add .
git commit -m "Add new Halloween pun: [簡述你的內容]"
git push origin add-my-story-idea

# 6. 建立 Pull Request
# 在 GitHub 介面建立 PR 並描述你的貢獻
```

### 📝 故事內容指南

#### 故事格式標準
```javascript
// 新場景格式範例
"your_scene_id": {
    "title": "場景標題 (必須有趣)",
    "description": "詳細描述場景，包含：\n- 視覺描述\n- 角色動作\n- 搞笑元素\n- NSFW暗示(適度)",
    "choices": [ // 如果不是結局
        {
            "option": "A: 選項文字 (要有個性)", 
            "next_scene": "下一個場景ID"
        }
        // 建議 3-5 個選項
    ],
    // 如果是結局，加上以下：
    "is_ending": true,
    "outcome": "🎉 結局描述！獲得稱號和經驗。",
    "score": 85 // 20-150 分
}
```

#### 內容創作準則
1. **萬聖節主題**：必須包含萬聖節元素（鬼怪、南瓜、魔法等）
2. **NSFW 適度**：成人暗示但不過度露骨，保持幽默感
3. **搞笑優先**：雙關語、意外轉折、荒謬情況
4. **角色個性**：每個NPC都要有獨特的說話方式
5. **選擇平衡**：避免明顯的「正確答案」，讓每個選擇都有趣

#### 雙關語示例
```
✅ 好的雙關語：
- "I'm dying to meet you!" (鬼魂說)
- "Want to bone?" (骷髏說)  
- "I'm batty about you!" (吸血鬼說)
- "You're gourd-geous!" (南瓜田)

❌ 避免的內容：
- 過度露骨的性描述
- 缺乏創意的陳詞濫調
- 與萬聖節無關的內容
```

### 🎨 成就系統貢獻

#### 成就設計標準
```javascript
"achievement_id": {
    "name": "成就名稱 (要朗朗上口)",
    "description": "達成條件的幽默描述",
    "icon": "🎭", // 選擇合適的 emoji
    "rarity": "common/rare/epic/legendary",
    "condition": "觸發條件",
    "points": "分數 (20-500)"
}
```

#### 稀有度指南
- **Common (20-50分)**：基礎結局、簡單探索
- **Rare (60-90分)**：特殊選擇、隱藏路線  
- **Epic (100-150分)**：困難成就、組合條件
- **Legendary (200-500分)**：終極挑戰、完美通關

### 🔧 技術貢獻指南

#### 開發環境設置
```bash
# 開發依賴 (可選)
npm install -g live-server  # 本地伺服器
npm install -g prettier     # 程式碼格式化

# 啟動開發伺服器
cd web
live-server --port=3000

# 程式碼格式化
prettier --write "**/*.{html,css,js}"
```

#### 程式碼風格
```javascript
// ✅ 推薦風格
const gameState = {
    currentScene: 'start',
    playerName: '',
    // 使用有意義的變數名稱
};

function displayScene(sceneId) {
    // 函數要簡潔且單一職責
    const scene = storyData[sceneId];
    if (!scene) {
        console.error('Scene not found:', sceneId);
        return;
    }
    // 其他邏輯...
}

// ❌ 避免的風格  
var x = document.getElementById('gameArea'); // 使用 const/let
function doStuff() { /* 功能不明確 */ }
```

#### UI/CSS 改進
```css
/* 響應式設計優先 */
@media (max-width: 768px) {
    .choice {
        padding: 15px;
        font-size: 0.9em;
        /* 確保觸控友善 */
        min-height: 44px;
    }
}

/* 使用 CSS 變數 */
:root {
    --primary-color: #ff6b35;
    --secondary-color: #8b5cf6;
}
```

### 🚀 進階貢獻

#### 新功能建議
1. **音效系統**：背景音樂和音效
2. **動畫效果**：場景轉換動畫
3. **多語言支援**：英文、日文版本
4. **社交分享**：成就分享到社交媒體
5. **統計系統**：詳細的遊戲統計
6. **主題切換**：不同的視覺主題

#### 大型功能開發流程
1. **提案階段**：在 Issues 中提出想法
2. **設計階段**：撰寫技術設計文件
3. **實作階段**：分階段開發，持續 PR
4. **測試階段**：跨瀏覽器測試
5. **部署階段**：協助部署和監控

### 📋 Pull Request 檢查清單

提交 PR 前，請確認：
- [ ] 📖 **描述清楚**：PR 標題和描述說明改動內容
- [ ] 🎮 **測試通過**：在至少兩個瀏覽器中測試
- [ ] 📱 **響應式**：在手機和桌面都能正常顯示
- [ ] 🎭 **內容品質**：故事有趣、語法正確、符合主題
- [ ] 🔗 **連結正確**：所有新場景都能正確連接
- [ ] 🏆 **成就對應**：新結局有對應的成就
- [ ] ⚡ **效能良好**：沒有明顯的效能問題
- [ ] 🎯 **無錯誤**：瀏覽器控制台沒有錯誤

## 🌟 貢獻者 (Contributors)

### 🥇 核心貢獻者
*重大功能開發者*

- [@dennislee928](https://github.com/dennislee928) - 9 PRs, 9 Issues - 38 總貢獻


## 📊 貢獻統計

### 總體數據
- **總貢獻者**: 1 人
- **本月活躍**: 1 人
- **總 PR 數**: 9 個
- **總 Issue 數**: 1 個

### 貢獻者等級分布
- 👑 **維護者**: 0 人
- 🥇 **核心貢獻者**: 1 人
- 🥈 **活躍貢獻者**: 0 人
- 🥉 **新手貢獻者**: 0 人

*最後更新: 2025-10-06 22:54:54*

## 授權

本專案採用 [MIT License](LICENSE)。歡迎 fork 和分享，但請保留 NSFW 警告。

## 聯絡與社群

- Discord：加入 [Tsext Community](https://discord.gg/yourinvite) 討論新想法。
- Twitter：[@tsext_adventure](https://x.com/lee66876613) – 分享你的搞笑結局！
- 問題回報：開 GitHub Issue。

給個星星 ⭐ 如果你覺得有趣！這能幫助我們上 GitHub Trending。
