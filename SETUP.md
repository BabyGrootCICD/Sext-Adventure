# Tsext Adventure: Halloween Haunt - 開發環境設置

## 🚀 快速設置

### 1. 克隆專案
```bash
git clone https://github.com/dennislee928/tsext-adventure.git
cd tsext-adventure
```

### 2. 設置 Python 環境
```bash
# 創建虛擬環境 (推薦)
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 安裝依賴
```bash
# 本專案使用標準庫，無需額外安裝
# 但如果你想要開發工具：
pip install pytest black flake8 mypy
```

### 4. 運行遊戲
```bash
python main.py
```

### 5. 運行測試
```bash
python tests/test_stories.py
```

### 6. 查看演示
```bash
python demo.py
```

## 🛠️ 開發工具設置

### VS Code 設置
創建 `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"],
    "files.associations": {
        "*.json": "jsonc"
    }
}
```

### Git Hooks (可選)
創建 `.git/hooks/pre-commit`:
```bash
#!/bin/sh
python tests/test_stories.py
```

## 📁 專案結構說明

```
tsext-adventure/
├── .gitignore              # Git 忽略檔案
├── README.md               # 專案說明
├── LICENSE                  # MIT 授權
├── CONTRIBUTING.md          # 貢獻指南
├── main.py                  # 主要遊戲腳本
├── demo.py                  # 演示腳本
├── stories/                 # 故事資料
│   ├── halloween.json       # 萬聖節故事
│   └── common.json          # 通用資料
├── tests/                   # 測試腳本
│   └── test_stories.py      # 測試案例
├── docs/                    # 文件
│   ├── guides/              # 使用指南
│   ├── api/                 # API 文件
│   └── examples/            # 範例
└── images/                  # 圖像資源
    ├── cover-design.md      # 封面設計
    └── badges/              # 徽章
```

## 🧪 測試和品質控制

### 運行所有測試
```bash
python tests/test_stories.py
```

### 程式碼格式化 (如果安裝了 black)
```bash
black *.py tests/*.py
```

### 程式碼檢查 (如果安裝了 flake8)
```bash
flake8 *.py tests/*.py
```

### 類型檢查 (如果安裝了 mypy)
```bash
mypy *.py
```

## 🎮 遊戲開發

### 添加新場景
1. 編輯 `stories/halloween.json`
2. 添加新場景資料
3. 確保場景連接正確
4. 運行測試驗證

### 添加新角色
1. 在 `stories/common.json` 中定義角色
2. 創建角色互動場景
3. 添加角色相關結局

### 添加新測試
1. 在 `tests/test_stories.py` 中添加測試方法
2. 確保測試覆蓋新功能
3. 運行測試驗證

## 🔧 故障排除

### 常見問題

**Q: 找不到故事檔案**
A: 確保在正確的目錄中運行遊戲

**Q: JSON 格式錯誤**
A: 使用 JSON 驗證工具檢查格式

**Q: 測試失敗**
A: 檢查故事資料的完整性和連接

**Q: 中文顯示問題**
A: 確保終端支援 UTF-8 編碼

### 除錯技巧
1. 使用 `print()` 語句除錯
2. 檢查 JSON 檔案格式
3. 驗證場景連接
4. 運行單個測試方法

## 📚 更多資源

- [Python 官方文件](https://docs.python.org/)
- [JSON 格式驗證](https://jsonlint.com/)
- [Git 使用指南](https://git-scm.com/docs)
- [VS Code Python 擴展](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

## 🤝 貢獻

詳見 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳細的貢獻流程。

---

**🎃 Happy Coding! 🎃**
