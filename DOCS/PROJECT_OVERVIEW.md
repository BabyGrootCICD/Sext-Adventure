# Tsext Adventure: Halloween Haunt

一個搞笑瑟瑟文字冒險遊戲的萬聖節特別版本！

## 🎃 專案特色

- **搞笑元素**: 充滿萬聖節雙關語和成人幽默
- **互動性**: 透過簡單選擇推進情節
- **多結局**: 10+ 個不同的故事結局
- **角色多樣**: 女巫、鬼魂、農夫女郎等有趣角色
- **開源**: 歡迎社區貢獻新故事和內容

## 🚀 快速開始

### 需求
- Python 3.8+

### 安裝
```bash
git clone https://github.com/dennislee928/tsext-adventure.git
cd tsext-adventure
python main.py
```

### 開始遊戲
1. 輸入你的名字
2. 輸入 "start" 開始遊戲
3. 享受萬聖節冒險！

## 📁 專案結構

```
tsext-adventure/
├── README.md              # 專案說明
├── LICENSE                # MIT 授權
├── main.py                # 主要遊戲腳本
├── stories/               # 故事資料
│   ├── halloween.json     # 萬聖節故事
│   └── common.json        # 通用資料
├── tests/                 # 測試腳本
│   └── test_stories.py
├── docs/                  # 文件
│   ├── guides/            # 使用指南
│   ├── api/               # API 文件
│   └── examples/          # 範例
├── images/                # 圖像資源
│   ├── cover.png          # 封面圖片
│   └── badges/            # 徽章
└── CONTRIBUTING.md        # 貢獻指南
```

## 🎮 遊戲機制

### 場景系統
- 基於場景的互動式故事
- 每個場景包含描述和選擇選項
- 選擇會影響故事發展和結局

### 分數系統
- 根據選擇和結局獲得不同分數
- 分數範圍: 0-100
- 不同分數對應不同成就

### 角色系統
- **女巫**: 擁有魔法的性感女巫
- **鬼魂**: 200 歲的寂寞靈魂
- **農夫女郎**: 南瓜田守護者
- **黑貓**: 神秘會說話的黑貓

## 🎯 結局類型

- **浪漫結局**: 與角色的浪漫故事
- **搞笑結局**: 充滿幽默的結局
- **冒險結局**: 探索神秘地點
- **神秘結局**: 超自然元素結局

## 🧪 測試

```bash
python tests/test_stories.py
```

測試包括:
- 故事資料完整性
- 場景連接驗證
- 遊戲邏輯測試
- 結局可達性檢查

## 🤝 貢獻

我們歡迎各種貢獻！

### 貢獻類型
- 新故事分支
- 萬聖節雙關語
- Bug 修復
- 文件改進
- 測試案例

### 如何貢獻
1. Fork 專案
2. 建立分支
3. 提交變更
4. 建立 Pull Request

詳見 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📚 文件

- [快速開始指南](docs/guides/quick-start.md)
- [遊戲機制說明](docs/guides/game-mechanics.md)
- [API 文件](docs/api/)
- [自訂故事範例](docs/examples/custom-story.md)

## 🎨 自訂

### 添加新場景
1. 編輯 `stories/halloween.json`
2. 添加新場景資料
3. 確保場景連接正確
4. 運行測試驗證

### 添加新角色
1. 定義角色屬性
2. 創建角色互動場景
3. 添加角色相關結局

## 🏆 成就系統

### 可獲得稱號
- 魔法騎士
- 月光戀人
- 鬼魂戀人
- 南瓜大師
- 田野戀人

### 分數等級
- 0-30: 搞笑結局
- 31-60: 友誼結局
- 61-80: 浪漫結局
- 81-95: 激情結局
- 96-100: 完美結局

## 🔮 未來計劃

- [ ] 存檔系統
- [ ] 多語言支援
- [ ] Web 版本
- [ ] 音效和視覺效果
- [ ] 多玩家模式

## 📞 聯絡

- **Discord**: [Tsext Community](https://discord.gg/yourinvite)
- **Twitter**: [@tsext_adventure](https://x.com/lee66876613)
- **GitHub Issues**: 回報問題和建議

## ⚠️ 免責聲明

本遊戲包含成人暗示和幽默內容，僅適合 18 歲以上玩家。無圖像內容，純文字遊戲。

## 📄 授權

本專案採用 [MIT License](LICENSE) 授權。

---

**給個星星 ⭐ 如果你覺得有趣！**

🎃 Happy Halloween! 🎃
