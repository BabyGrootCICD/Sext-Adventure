# 遊戲機制說明

本文檔詳細說明了 Tsext Adventure: Halloween Haunt 的遊戲機制和內部運作原理。

## 🎮 核心機制

### 場景系統
遊戲基於場景系統運作，每個場景包含：

- **標題**: 場景的名稱
- **描述**: 場景的詳細描述
- **選擇**: 玩家可以選擇的選項
- **連接**: 選擇後前往的下一個場景

### 狀態管理
遊戲維護以下狀態：

- **當前場景**: 玩家目前所在的場景
- **玩家名稱**: 玩家輸入的名字
- **分數**: 累積的分數
- **已訪問場景**: 記錄玩家訪問過的場景

## 🔄 遊戲流程

### 1. 初始化
```python
game = HalloweenAdventure()
game.current_scene = "start"
game.score = 0
game.visited_scenes = set()
```

### 2. 載入故事
```python
game.load_stories()  # 從 JSON 檔案載入故事資料
```

### 3. 遊戲循環
```python
while True:
    game.display_scene(game.current_scene)
    if is_ending_scene:
        break
    next_scene = get_user_choice()
    game.current_scene = next_scene
```

### 4. 結局處理
```python
if scene.is_ending:
    game.handle_ending(scene)
    ask_restart()
```

## 📊 分數系統

### 分數計算
每個結局場景都有對應的分數：

```json
{
  "scene_id": {
    "is_ending": true,
    "score": 85,
    "outcome": "結局描述..."
  }
}
```

### 分數等級
- **0-30**: 搞笑結局 (Funny Endings)
- **31-60**: 友誼結局 (Friendship Endings)
- **61-80**: 浪漫結局 (Romantic Endings)
- **81-95**: 激情結局 (Passionate Endings)
- **96-100**: 完美結局 (Perfect Endings)

### 分數影響因素
- **選擇類型**: 浪漫選擇通常獲得更高分數
- **角色關係**: 與角色建立良好關係
- **探索程度**: 訪問更多場景
- **結局類型**: 不同結局有不同分數

## 🎭 角色系統

### 角色類型
- **女巫**: 擁有魔法能力，喜歡勇敢的人
- **鬼魂**: 200 歲的寂寞靈魂，渴望陪伴
- **農夫女郎**: 南瓜田守護者，喜歡直接的人
- **黑貓**: 神秘生物，會變身成人形

### 角色互動
每個角色都有不同的互動模式：

- **女巫**: 喜歡魔法和冒險
- **鬼魂**: 需要理解和陪伴
- **農夫女郎**: 欣賞誠實和直接
- **黑貓**: 重視友誼和信任

## 🗺️ 場景連接

### 場景圖結構
遊戲使用有向圖結構連接場景：

```
start -> witch_encounter -> broom_ride_success -> rooftop_romance
     -> haunted_house -> ghost_romance -> ghost_lessons
     -> pumpkin_patch -> farmer_romance -> heart_to_heart
```

### 場景驗證
系統會驗證：

- 所有場景都存在
- 場景連接有效
- 結局場景可達
- 沒有孤立場景

## 🎯 成就系統

### 成就類型
- **結局成就**: 完成特定結局
- **探索成就**: 訪問所有場景
- **分數成就**: 達到特定分數
- **角色成就**: 與所有角色互動

### 成就解鎖
成就會在以下情況解鎖：

- 完成特定結局
- 達到特定分數
- 訪問所有場景
- 與所有角色互動

## 🔧 技術實現

### 資料結構
```python
class HalloweenAdventure:
    def __init__(self):
        self.story_data = {}      # 故事資料
        self.current_scene = ""   # 當前場景
        self.player_name = ""    # 玩家名稱
        self.score = 0           # 分數
        self.visited_scenes = set()  # 已訪問場景
```

### 場景資料格式
```json
{
  "scene_id": {
    "title": "場景標題",
    "description": "場景描述",
    "choices": [
      {
        "option": "選擇描述",
        "next_scene": "下一個場景ID"
      }
    ],
    "is_ending": false,
    "score": 0,
    "outcome": "結局描述"
  }
}
```

### 錯誤處理
- **檔案不存在**: 顯示錯誤訊息並退出
- **JSON 格式錯誤**: 顯示解析錯誤
- **場景不存在**: 顯示警告訊息
- **無效選擇**: 要求重新輸入

## 🧪 測試機制

### 測試類型
- **單元測試**: 測試個別函數
- **整合測試**: 測試遊戲流程
- **資料驗證**: 測試故事資料完整性

### 測試覆蓋
- 所有場景連接
- 所有結局可達
- 分數計算正確
- 錯誤處理有效

## 🎨 自訂機制

### 添加新場景
1. 在 `stories/halloween.json` 中添加場景
2. 確保場景連接有效
3. 添加對應的測試案例

### 添加新角色
1. 定義角色屬性
2. 創建角色互動場景
3. 添加角色相關結局

### 添加新機制
1. 修改 `HalloweenAdventure` 類別
2. 更新場景資料格式
3. 添加對應測試

## 📈 效能考量

### 記憶體使用
- 故事資料載入到記憶體
- 已訪問場景使用集合儲存
- 分數使用整數儲存

### 執行效率
- 場景查找使用字典 (O(1))
- 選擇驗證使用列表遍歷
- 結局檢查使用布林值

## 🔮 未來擴展

### 計劃功能
- 存檔系統
- 多語言支援
- 音效和視覺效果
- 多玩家模式
- Web 版本

### 技術改進
- 更好的錯誤處理
- 效能優化
- 程式碼重構
- 測試覆蓋率提升

---

**注意**: 這些機制可能會在未來版本中更新，請關注更新日誌。

🎃 Happy Coding! 🎃
