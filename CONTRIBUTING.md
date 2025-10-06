# 🎃 詳細貢獻指南 (Comprehensive Contributing Guide)

歡迎來到 **Tsext Adventure: Halloween Haunt - 萬聖節極樂莊園** 的完整貢獻指南！我們熱烈歡迎社區成員為這個成人向萬聖節文字冒險遊戲做出貢獻。

> **🔞 注意**: 本專案包含成人內容，貢獻者需年滿18歲。

## 🚀 快速開始 (5分鐘貢獻)

### 方法一：簡單故事貢獻
```bash
# 1. Fork 並 clone 專案
git clone https://github.com/your-username/tsext-adventure.git
cd tsext-adventure

# 2. 創建新分支
git checkout -b add-vampire-scene

# 3. 編輯故事檔案 (選擇以下任一)
# 選項 A：直接編輯 web/index.html (即時生效)
# 選項 B：編輯 stories/halloween.json (結構化)

# 4. 測試你的更改
# 本地測試
python tests/test_stories.py  # 確保所有測試通過
# 開啟 web/index.html 在瀏覽器中測試

# 5. 提交更改
git add .
git commit -m "Add: 吸血鬼城堡新場景 - 血酒儀式"
git push origin add-vampire-scene

# 6. 建立 Pull Request
# GitHub Actions 會自動運行測試驗證你的更改
```

### 方法二：成就系統貢獻
```bash
# 1. 編輯成就檔案
# stories/achievements.json 或 web/index.html 中的 achievementsData

# 2. 遵循成就格式
# 3. 測試解鎖條件
# 4. 提交 PR
```

## 📝 詳細貢獻類型

### 🎭 故事內容貢獻 (Story Content)

#### 🏰 九大區域擴展 (已完整實現)
遊戲現在擁有**完整的9大區域**，包含**60+場景**和**35+結局**：

1. **🧙‍♀️ 女巫塔** - 魔法與掃帚騎乘 (8場景)
2. **👻 鬼屋探險** - 幽靈互動與靈魂共鳴 (12場景)  
3. **🎃 南瓜田迷宮** - 魔法南瓜與農夫女郎 (6場景)
4. **🧛‍♂️ 吸血鬼城堡** - 變身術與初擁儀式 (15場景)
5. **🎉 地下派對** - 魔法雞尾酒與狂歡 (8場景)
6. **⚰️ 古老墓地** - 維多利亞幽靈與復仇 (6場景)
7. **🌲 魔法森林** - 精靈試煉與獨角獸 (5場景)
8. **📚 詛咒圖書館** - 禁忌知識與愛情魔法 (4場景)
9. **🍷 巫師酒吧** - 變性藥劑與預知未來 (4場景)

> **📊 當前狀態**: 所有區域已完整實現，包含完整的場景連接和結局系統

#### 故事場景格式 (完整示例)
```javascript
// web/index.html 中的 storyData 格式
"your_scene_id": {
    "title": "場景標題 (要有萬聖節氛圍)",
    "description": "詳細場景描述，包含：\n- 視覺細節 (燭光、月光等)\n- 角色動作和表情\n- NSFW暗示 (適度但誘人)\n- 雙關語或幽默元素\n\n對話格式：「引號內是角色說話」",
    "choices": [ // 如果不是結局場景
        {
            "option": "A: 具體選擇描述 - 「直接對話」", 
            "next_scene": "下個場景ID"
        },
        {
            "option": "B: 另一個選擇 - 「不同風格對話」",
            "next_scene": "另一個場景ID" 
        }
        // 建議3-5個選擇，提供不同性格路線
    ],
    // 如果是結局場景，改為：
    "is_ending": true,
    "outcome": "🎉 結局標題！詳細結局描述...\n\n你獲得了『稱號名稱』，並學會了特殊技能。",
    "score": 85 // 分數範圍：20-150
}
```

#### stories/halloween.json 格式 (結構化版本)
```json
{
  "scene_id": {
    "title": "場景標題",
    "description": "場景描述...",
    "choices": [
      {
        "option": "A: 選擇文字",
        "next_scene": "下個場景"
      }
    ]
  }
}
```

#### 內容創作指南
1. **萬聖節氛圍必備**：鬼怪、南瓜、魔法、月光、古堡等元素
2. **成人暗示技巧**：使用雙關語而非直接描述，保持誘人但不過度
3. **角色個性化**：
   - 女巫：神秘、調皮、魔法感
   - 吸血鬼：優雅、誘惑、古典
   - 幽靈：哀怨、浪漫、超脫
   - 精靈：自然、純真、試煉感
   - 魅魔：直接、熱情、放蕩

#### 雙關語示例庫
```javascript
// 各區域專用雙關語
🧙‍♀️ 女巫區：
- "Want to ride my broomstick?" (想騎我的掃帚嗎？)
- "I'll cast a spell on you!" (我要對你施咒！)
- "My cauldron is bubbling for you!" (我的大鍋為你沸騰！)

🧛‍♂️ 吸血鬼區：
- "I want to suck... your attention!" (我想吸...你的注意力！)
- "You make my heart race... if I had one!" (你讓我心跳加速...如果我還有心的話！)
- "Want to see my... fangs?" (想看我的...尖牙嗎？)

🎃 南瓜田區：
- "You're gourd-geous!" (你太"南瓜"了！)
- "Let's get pumped!" (讓我們興奮起來！)
- "I'm falling for you... into the pumpkin patch!" (我為你傾倒...掉進南瓜田！)
```

### 🏆 成就系統貢獻 (Achievement System)

#### 成就類型分級
```javascript
// 成就稀有度與分數指南
"achievement_id": {
    "name": "成就名稱 (要朗朗上口且有趣)",
    "description": "達成條件的幽默描述",
    "icon": "🎭", // 選擇合適的 emoji
    "rarity": "稀有度等級",
    "condition": "觸發條件ID", 
    "points": "分數"
}

// 稀有度分級：
- Common (20-50分)：基礎結局、簡單探索
- Rare (60-90分)：特殊選擇、隱藏路線
- Epic (100-150分)：困難成就、組合條件  
- Legendary (200-500分)：終極挑戰、完美通關
```

#### 成就示例 (各區域)
```javascript
// 🧛‍♂️ 吸血鬼城堡成就
"night_sky_knight": {
    "name": "夜空騎士",
    "description": "掌握蝙蝠變身，在月夜中翱翔",
    "icon": "🦇",
    "rarity": "epic", 
    "condition": "ending_bat_transformation",
    "points": 95
},

// 🎉 地下派對成就
"desire_king": {
    "name": "慾火之王", 
    "description": "成為地下派對的絕對主角",
    "icon": "🔥",
    "rarity": "legendary",
    "condition": "ending_party_center_fire", 
    "points": 120
},

// 組合成就 (解鎖多個相關結局)
"vampire_lord": {
    "name": "吸血鬼領主",
    "description": "解鎖所有吸血鬼城堡結局", 
    "icon": "🧛‍♂️👑",
    "rarity": "legendary",
    "condition": "all_vampire_endings",
    "points": 200
}
```

### 🎨 UI/UX 改進 (User Interface & Experience)

#### 響應式設計貢獻
```css
/* web/index.html 中的 CSS 改進 */
/* 新增螢幕適配 */
@media (max-width: 480px) {
    .choice {
        padding: 15px;
        font-size: 0.9em;
        /* 確保觸控友善，最小44px高度 */
        min-height: 44px;
    }
}

/* 新增動畫效果 */
.achievement-popup {
    animation: slideInUp 0.3s ease-out;
    transform: translateY(20px);
    opacity: 0;
}

.achievement-popup.show {
    transform: translateY(0);
    opacity: 1;
}
```

#### 成就圖片下載功能
```javascript
// 貢獻新的圖片生成功能
function downloadAchievementImage(achievementId) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // 設定 canvas 尺寸 (社交媒體適用)
    canvas.width = 800;
    canvas.height = 600;
    
    // 添加你的創意設計...
}
```

#### 無障礙功能 (Accessibility)
- **鍵盤導航**：支援 Tab/Enter 鍵操作
- **高對比模式**：支援 `prefers-contrast: high`
- **減少動畫**：支援 `prefers-reduced-motion`
- **螢幕閱讀器**：適當的 ARIA 標籤

### 💻 技術改進 (Technical Improvements)

#### 前端技術棧
- **HTML5**：語義化標籤、Canvas API
- **CSS3**：Flexbox、Grid、媒體查詢、動畫
- **JavaScript ES6+**：模組化、箭頭函數、Promise
- **本地儲存**：localStorage 遊戲進度
- **社交分享**：8大平台整合

#### 效能優化建議
```javascript
// 使用 requestAnimationFrame 優化動畫
function smoothScrollTo(element) {
    const start = window.pageYOffset;
    const target = element.offsetTop;
    const duration = 300;
    
    function animation(currentTime) {
        // 平滑捲動邏輯...
    }
    
    requestAnimationFrame(animation);
}
```

### 🌍 多平台部署貢獻

#### GitHub Pages 自動部署
```yaml
# .github/workflows/deploy.yml 改進
name: Deploy to GitHub Pages
on:
  push:
    branches: [ main, dev ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Add cache busting
        run: |
          TIMESTAMP=$(date +%s)
          sed -i "s/{{VERSION}}/${TIMESTAMP}/g" web/index.html
```

#### Itch.io 版本同步
- 確保 `itch-deploy/index.html` 與 `web/index.html` 同步
- 添加 Itch.io 特定的元數據和樣式
- 測試不同瀏覽器相容性

### 🐛 Bug 修復與測試 (Bug Fixes & Testing)

#### 常見問題類型
1. **缺失場景**：`next_scene` 指向不存在的場景ID
2. **成就觸發**：`condition` 與實際結局ID不匹配  
3. **UI斷裂**：在小螢幕上排版問題
4. **快取問題**：瀏覽器快取導致的更新延遲

#### 測試檢查清單
```bash
# 手動測試流程
1. 開啟 web/index.html
2. 測試每個主要路線至少到達一個結局
3. 檢查成就是否正確解鎖
4. 測試響應式設計 (手機/桌面)
5. 檢查瀏覽器控制台無錯誤
6. 測試分享功能
7. 驗證圖片下載功能
```

#### 自動化測試貢獻
```javascript
// tests/test_stories.py 或新增 JavaScript 測試
describe('Story Flow Tests', () => {
    it('所有場景都應該可達', () => {
        const allScenes = Object.keys(storyData);
        const reachableScenes = findReachableScenes('start');
        
        expect(reachableScenes).to.include.members(allScenes);
    });
    
    it('所有成就條件都應該有效', () => {
        Object.entries(achievementsData).forEach(([id, achievement]) => {
            if (achievement.condition.startsWith('ending_')) {
                const sceneId = achievement.condition.replace('ending_', '');
                expect(storyData[sceneId]).to.exist;
                expect(storyData[sceneId].is_ending).to.be.true;
            }
        });
    });
});
```

### 📚 文件與本地化 (Documentation & Localization)

#### 多語言支援架構
```javascript
// 建議的國際化結構
const translations = {
    'zh-TW': {
        'ui.start': '開始遊戲',
        'ui.achievements': '成就',
        // 故事內容...
    },
    'en-US': {
        'ui.start': 'Start Game', 
        'ui.achievements': 'Achievements',
        // Story content...
    }
};
```

#### API 文件貢獻
- 為主要函數添加 JSDoc 註解
- 建立遊戲狀態管理文件
- 成就系統 API 說明
- 自定義事件系統文件

## 🎯 萬聖節特別挑戰 (Halloween Hacktoberfest)

### 🥉 新手友善議題 (Good First Issues)
標籤 `good-first-issue` 的議題，適合初次貢獻者：

#### 故事內容優化 (5-15分鐘)
- [ ] 為現有場景添加更多對話選項
- [ ] 改進場景描述的細節和氛圍
- [ ] 為結局添加更多後續劇情
- [ ] 創造新的雙關語和幽默內容
- [ ] 優化現有角色的個性化對話

#### 成就系統 (10-20分鐘)
- [ ] 設計新的區域組合成就
- [ ] 添加特殊時間觸發成就 (如深夜、萬聖節)
- [ ] 創建連續遊玩獎勵成就
- [ ] 設計社交分享相關成就

#### UI/UX 改進 (15-30分鐘)
- [ ] 改善手機端觸控體驗
- [ ] 添加新的動畫效果
- [ ] 優化成就通知樣式
- [ ] 改進分享按鈕設計

### 🥈 中級挑戰 (Intermediate Issues)
適合有經驗的貢獻者：

#### 功能開發 (30-60分鐘)
- [ ] 實作音效系統 (背景音樂、音效)
- [ ] 添加自動存檔功能
- [ ] 建立遊戲統計面板
- [ ] 實作夜間模式切換
- [ ] 添加遊戲內提示系統

#### 技術優化 (45-90分鐘)
- [ ] 優化載入速度和快取策略
- [ ] 添加 PWA 支援 (離線遊戲)
- [ ] 實作無障礙功能改進
- [ ] 建立自動化測試框架
- [ ] 優化 SEO 和社交媒體分享

### 🥇 進階專案 (Advanced Projects)
適合資深貢獻者的大型項目：

#### 系統架構 (2-5小時)
- [ ] 建立模組化故事引擎
- [ ] 實作多語言國際化系統
- [ ] 建立故事編輯器工具
- [ ] 添加使用者自定義故事功能
- [ ] 建立雲端存檔同步系統

#### 平台擴展 (3-8小時)  
- [ ] 移植到 React/Vue 框架
- [ ] 建立 Android/iOS 應用
- [ ] 添加多人遊戲模式
- [ ] 建立故事分享社群平台
- [ ] 整合 VR/AR 體驗

## 📋 現代化貢獻規範

### 技術棧要求
- **前端**: HTML5, CSS3, ES6+ JavaScript
- **工具**: Git, GitHub Actions, 瀏覽器開發工具
- **測試**: 手動測試 + 自動化測試(可選)
- **部署**: GitHub Pages, Itch.io

### 代碼風格指南
```javascript
// ✅ 推薦的 JavaScript 風格
const gameState = {
    currentScene: 'start',
    unlockedAchievements: new Set(),
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

### Git 提交訊息格式
```bash
# 格式：類型(範圍): 簡短描述
# 
# 詳細描述（可選）
#
# Breaking Changes（如有）
# Closes #123

# 範例：
feat(vampire): 新增血酒品鑑場景

為吸血鬼城堡添加了三種新的血酒：
- 深紅玫瑰血酒 (浪漫路線)  
- 千年陳釀血酒 (力量路線)
- 月夜特調血酒 (神秘路線)

每種血酒都有獨特的效果和後續劇情分支

Closes #42
```

**提交類型**:
- `feat`: 新功能或故事內容
- `fix`: Bug 修復  
- `ui`: UI/UX 改進
- `perf`: 效能優化
- `docs`: 文件更新
- `test`: 測試相關
- `refactor`: 代碼重構
- `deploy`: 部署相關

### Pull Request 檢查清單
提交 PR 前，請確認：
- [ ] 📖 **描述清楚**：PR 標題和描述說明改動內容
- [ ] 🧪 **測試通過**：運行 `python tests/test_stories.py` 確保所有測試通過
- [ ] 🎮 **瀏覽器測試**：在至少兩個瀏覽器中測試
- [ ] 📱 **響應式**：在手機和桌面都能正常顯示  
- [ ] 🎭 **內容品質**：故事有趣、語法正確、符合主題
- [ ] 🔗 **連結正確**：所有新場景都能正確連接
- [ ] 🏆 **成就對應**：新結局有對應的成就
- [ ] ⚡ **效能良好**：沒有明顯的效能問題
- [ ] 🎯 **無錯誤**：瀏覽器控制台沒有錯誤
- [ ] 🔄 **同步更新**：同時更新 `web/index.html` 和 `stories/halloween.json`

## 🏆 貢獻者認可系統

### 貢獻者等級
- 🥉 **新手貢獻者** (Novice)：首次貢獻 (1-2 PR)
- 🥈 **活躍貢獻者** (Active)：持續貢獻 (3-10 PR)
- 🥇 **核心貢獻者** (Core)：重大功能 (10+ PR)
- 👑 **專案維護者** (Maintainer)：長期維護專案

### 月度特殊貢獻獎
- 🎭 **最佳劇情獎**：最有創意的故事內容
- 🛠️ **技術創新獎**：最佳技術改進
- 🐛 **Bug獵人獎**：發現和修復最多問題
- 🎨 **設計大師獎**：最佳UI/UX改進
- 🌟 **社區之星**：最熱心幫助新手的貢獻者

### 獎勵機制
- **GitHub 認可**：Special mention in README.md
- **Discord 角色**：專屬貢獻者身分組
- **優先審核**：PR 和 Issue 優先處理權
- **提早體驗**：新功能搶先體驗權限

## 🤝 社區行為準則 (Community Code of Conduct)

### 🔞 成人內容處理準則
- **年齡確認**：所有貢獻者需確認年滿18歲
- **內容分級**：明確標記NSFW內容級別
- **品味界線**：保持幽默感，避免過度露骨
- **尊重原則**：尊重所有性向和身份認同

### 期望行為 ✅
- ✨ 使用友善和包容的語言
- 🤝 尊重不同的觀點和經驗  
- 💭 優雅地接受建設性批評
- 🎯 關注對社區最有利的事情
- ❤️ 對其他社區成員表現同理心
- 😄 保持幽默感，享受創作過程

### 不可接受行為 ❌
- 🚫 惡意的人身攻擊或侮辱性評論
- 🚫 公開或私下的騷擾行為
- 🚫 未經許可發布他人私人資訊
- 🚫 過度露骨或令人不適的內容
- 🚫 其他在專業環境中不適當的行為

## 📞 獲得幫助與支援

### 即時討論平台
- 🎮 **Discord**: [Tsext Community](https://discord.gg/tsext) (主要討論區)
- 💬 **GitHub Discussions**: 技術問題和功能討論  
- 🐛 **Issue Tracker**: Bug回報和功能請求

### 導師制度
新貢獻者可以申請導師協助：
1. 在 Issue 中標記 `@mentor-request`  
2. 說明你的背景和想貢獻的方向
3. 我們會安排合適的導師協助你

### 社交媒體
- 🐦 **Twitter**: [@tsext_adventure](https://x.com/lee66876613) 
- 📧 **Email**: contributors@tsext-adventure.com
- 📱 **Telegram**: [Tsext Adventure群組](https://t.me/tsext_adventure)

### 常見問題 FAQ
**Q: 我不會程式設計，能貢獻嗎？**  
A: 當然！你可以貢獻故事內容、測試遊戲、回報問題、翻譯內容等。

**Q: 如何確保我的NSFW內容適當？**  
A: 以現有內容為參考標準，使用暗示而非直接描述，保持幽默感。

**Q: 測試失敗怎麼辦？**  
A: 運行 `python tests/test_stories.py` 檢查錯誤，確保所有場景連接正確。

**Q: 需要同時更新兩個檔案嗎？**  
A: 是的！故事內容需要同時更新 `web/index.html` 和 `stories/halloween.json`。

**Q: 需要多久才能審核我的PR？**  
A: 通常1-3天內會有初步回應，複雜功能可能需要更長時間。

**Q: 如何成為核心貢獻者？**  
A: 持續提供高品質的貢獻，參與社區討論，幫助新手貢獻者。

## 📊 專案當前狀態 (2024年10月)

### ✅ 已完成功能
- **🎭 完整故事系統**: 9大區域，60+場景，35+結局
- **🏆 成就系統**: 60+成就，包含個人、組合、終極成就
- **📱 響應式設計**: 支援手機、平板、桌面
- **🎨 現代化UI**: 成就圖片下載、社交分享、無障礙功能
- **🧪 自動化測試**: GitHub Actions 測試套件，15個測試全部通過
- **🚀 雙平台部署**: GitHub Pages + Itch.io 自動部署

### 🔄 持續改進領域
- **📝 故事內容優化**: 對話細節、角色個性化
- **🎨 UI/UX 改進**: 動畫效果、使用者體驗
- **🌍 國際化支援**: 多語言版本
- **📊 遊戲統計**: 進度追蹤、成就分析

### 🎯 貢獻重點
由於核心功能已完成，現在歡迎以下類型的貢獻：
- **內容優化**: 改進現有場景的對話和描述
- **新成就設計**: 創意成就和觸發條件
- **UI改進**: 動畫、效果、使用者體驗
- **測試覆蓋**: 邊界情況測試、效能測試
- **文件完善**: API文件、使用指南

## 🎉 感謝所有貢獻者

感謝每一位為 **Tsext Adventure** 做出貢獻的開發者、設計師、作家和測試者！每個PR、每個建議、每個Bug報告都讓這個專案變得更好。

### 特別感謝
- 🌟 **故事創作者們**：為遊戲增添了無數精彩劇情
- 🛠️ **技術貢獻者們**：持續改進遊戲體驗和效能  
- 🎨 **設計師們**：讓遊戲界面更加美觀實用
- 🐛 **測試者們**：幫助發現和修復各種問題
- 💬 **社區管理者們**：維護友善包容的貢獻環境

---

**🎃 Remember**: 這是一個充滿創意和幽默的專案。讓我們一起創造最棒的萬聖節成人冒險遊戲，同時保持尊重、包容和專業的態度！

### 🚀 準備好開始貢獻了嗎？

1. 🍴 Fork 這個專案
2. 🌟 選擇一個適合你的議題  
3. 💻 開始你的創意貢獻
4. 🎉 提交你的第一個 Pull Request！

**Happy Contributing! 🎃✨**
