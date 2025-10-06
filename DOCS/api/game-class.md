# API 文件

## HalloweenAdventure 類別

`HalloweenAdventure` 是遊戲的主要類別，負責管理遊戲狀態和流程。

### 初始化
```python
game = HalloweenAdventure()
```

### 屬性
- `story_data`: 故事資料字典
- `current_scene`: 當前場景 ID
- `player_name`: 玩家名稱
- `score`: 累積分數
- `visited_scenes`: 已訪問場景集合

### 方法

#### `load_stories()`
載入故事資料從 JSON 檔案。

**參數**: 無

**回傳值**: 無

**異常**: 
- `FileNotFoundError`: 找不到故事檔案
- `json.JSONDecodeError`: JSON 格式錯誤

#### `display_scene(scene_id: str)`
顯示指定場景的內容。

**參數**:
- `scene_id` (str): 場景 ID

**回傳值**: 無

**異常**: 無

#### `handle_ending(scene: Dict[str, Any])`
處理結局場景。

**參數**:
- `scene` (Dict[str, Any]): 結局場景資料

**回傳值**: 無

**異常**: 無

#### `get_user_choice(choices: List[Dict[str, Any]]) -> str`
獲取用戶選擇。

**參數**:
- `choices` (List[Dict[str, Any]]): 選擇選項列表

**回傳值**: 
- `str`: 下一個場景 ID

**異常**:
- `ValueError`: 無效的數字輸入
- `KeyboardInterrupt`: 用戶中斷

#### `play()`
主要遊戲循環。

**參數**: 無

**回傳值**: 無

**異常**: 無

#### `restart_game()`
重新開始遊戲。

**參數**: 無

**回傳值**: 無

**異常**: 無

#### `start()`
開始遊戲。

**參數**: 無

**回傳值**: 無

**異常**: 無

## 故事資料格式

### 場景格式
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

### 欄位說明
- `title`: 場景標題 (可選)
- `description`: 場景描述 (可選)
- `choices`: 選擇選項列表 (可選)
- `is_ending`: 是否為結局場景 (布林值)
- `score`: 結局分數 (整數，僅結局場景)
- `outcome`: 結局描述 (字串，僅結局場景)

### 選擇格式
```json
{
  "option": "選擇描述",
  "next_scene": "下一個場景ID"
}
```

## 測試 API

### TestStoryData 類別
測試故事資料的完整性和格式。

#### 測試方法
- `test_halloween_data_structure()`: 測試萬聖節故事資料結構
- `test_scene_structure()`: 測試場景結構
- `test_scene_connections()`: 測試場景連接
- `test_ending_scenes()`: 測試結局場景
- `test_common_data_structure()`: 測試通用資料結構
- `test_puns_content()`: 測試雙關語內容

### TestGameLogic 類別
測試遊戲邏輯。

#### 測試方法
- `test_game_initialization()`: 測試遊戲初始化
- `test_story_loading()`: 測試故事載入
- `test_scene_display()`: 測試場景顯示
- `test_score_calculation()`: 測試分數計算
- `test_restart_functionality()`: 測試重新開始功能

### TestGameFlow 類別
測試遊戲流程。

#### 測試方法
- `test_start_to_ending_path()`: 測試從開始到結局的完整路徑
- `test_all_endings_reachable()`: 測試所有結局都可以到達

## 錯誤處理

### 常見錯誤
- **檔案不存在**: 顯示錯誤訊息並退出
- **JSON 格式錯誤**: 顯示解析錯誤
- **場景不存在**: 顯示警告訊息
- **無效選擇**: 要求重新輸入

### 錯誤處理最佳實踐
1. 使用 try-except 捕獲異常
2. 提供有意義的錯誤訊息
3. 記錄錯誤日誌
4. 優雅地處理錯誤情況

## 擴展 API

### 添加新場景
```python
def add_scene(scene_id: str, scene_data: Dict[str, Any]):
    """添加新場景到故事資料"""
    self.story_data[scene_id] = scene_data
```

### 添加新角色
```python
def add_character(character_id: str, character_data: Dict[str, Any]):
    """添加新角色到角色資料"""
    # 實作角色添加邏輯
    pass
```

### 添加新機制
```python
def add_mechanic(mechanic_name: str, mechanic_func: Callable):
    """添加新遊戲機制"""
    setattr(self, mechanic_name, mechanic_func)
```

## 效能考量

### 時間複雜度
- 場景查找: O(1)
- 選擇驗證: O(n)
- 結局檢查: O(1)

### 空間複雜度
- 故事資料: O(n)
- 已訪問場景: O(n)
- 分數: O(1)

### 優化建議
1. 使用字典進行快速查找
2. 使用集合進行快速成員檢查
3. 避免不必要的資料複製
4. 使用生成器處理大型資料集

## 版本相容性

### Python 版本
- 最低要求: Python 3.8
- 推薦版本: Python 3.9+
- 測試版本: Python 3.8, 3.9, 3.10, 3.11

### 依賴套件
- 標準庫: json, os, sys, random, typing
- 測試: unittest, unittest.mock

### 向後相容性
- 主要版本: 可能破壞相容性
- 次要版本: 保持相容性
- 修補版本: 完全相容

---

**注意**: API 可能會在未來版本中更新，請關注更新日誌。

🎃 Happy Coding! 🎃
