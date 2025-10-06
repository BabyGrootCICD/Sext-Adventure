#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tsext Adventure: Halloween Haunt 測試腳本
測試故事邏輯、JSON 格式和遊戲功能

作者: Tsext Adventure Team
授權: MIT License
"""

import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock


class TestStoryData(unittest.TestCase):
    """測試故事資料的完整性和格式"""
    
    def setUp(self):
        """設定測試環境"""
        self.halloween_data = {}
        self.common_data = {}
        
        # 載入故事資料
        try:
            with open('stories/halloween.json', 'r', encoding='utf-8') as f:
                self.halloween_data = json.load(f)
        except FileNotFoundError:
            self.fail("找不到 stories/halloween.json 檔案")
        except json.JSONDecodeError as e:
            self.fail(f"halloween.json 格式錯誤: {e}")
        
        try:
            with open('stories/common.json', 'r', encoding='utf-8') as f:
                self.common_data = json.load(f)
        except FileNotFoundError:
            self.fail("找不到 stories/common.json 檔案")
        except json.JSONDecodeError as e:
            self.fail(f"common.json 格式錯誤: {e}")
    
    def test_halloween_data_structure(self):
        """測試萬聖節故事資料結構"""
        self.assertIsInstance(self.halloween_data, dict, "halloween.json 應該是字典格式")
        self.assertGreater(len(self.halloween_data), 0, "halloween.json 不應該為空")
        
        # 檢查必要場景
        required_scenes = ['start']
        for scene in required_scenes:
            self.assertIn(scene, self.halloween_data, f"缺少必要場景: {scene}")
    
    def test_scene_structure(self):
        """測試場景結構"""
        for scene_id, scene_data in self.halloween_data.items():
            with self.subTest(scene=scene_id):
                self.assertIsInstance(scene_data, dict, f"場景 {scene_id} 應該是字典格式")
                
                # 檢查必要欄位
                if 'choices' in scene_data:
                    self.assertIsInstance(scene_data['choices'], list, f"場景 {scene_id} 的 choices 應該是列表")
                    for i, choice in enumerate(scene_data['choices']):
                        self.assertIsInstance(choice, dict, f"場景 {scene_id} 的選擇 {i} 應該是字典")
                        self.assertIn('option', choice, f"場景 {scene_id} 的選擇 {i} 缺少 option 欄位")
                        self.assertIn('next_scene', choice, f"場景 {scene_id} 的選擇 {i} 缺少 next_scene 欄位")
                
                # 檢查結局場景
                if scene_data.get('is_ending', False):
                    self.assertIn('outcome', scene_data, f"結局場景 {scene_id} 缺少 outcome 欄位")
                    if 'score' in scene_data:
                        self.assertIsInstance(scene_data['score'], int, f"場景 {scene_id} 的 score 應該是整數")
    
    def test_scene_connections(self):
        """測試場景連接"""
        scene_ids = set(self.halloween_data.keys())
        
        for scene_id, scene_data in self.halloween_data.items():
            if 'choices' in scene_data:
                for choice in scene_data['choices']:
                    next_scene = choice['next_scene']
                    self.assertIn(next_scene, scene_ids, f"場景 {scene_id} 連接到不存在的場景: {next_scene}")
    
    def test_ending_scenes(self):
        """測試結局場景"""
        ending_scenes = [scene_id for scene_id, scene_data in self.halloween_data.items() 
                        if scene_data.get('is_ending', False)]
        
        self.assertGreater(len(ending_scenes), 0, "至少應該有一個結局場景")
        
        for scene_id in ending_scenes:
            scene_data = self.halloween_data[scene_id]
            self.assertIn('outcome', scene_data, f"結局場景 {scene_id} 缺少 outcome 欄位")
            self.assertIsInstance(scene_data['outcome'], str, f"結局場景 {scene_id} 的 outcome 應該是字串")
    
    def test_common_data_structure(self):
        """測試通用資料結構"""
        self.assertIsInstance(self.common_data, dict, "common.json 應該是字典格式")
        
        # 檢查必要欄位
        required_fields = ['common_puns', 'halloween_pickup_lines', 'nsfw_puns']
        for field in required_fields:
            self.assertIn(field, self.common_data, f"缺少必要欄位: {field}")
            self.assertIsInstance(self.common_data[field], list, f"{field} 應該是列表格式")
            self.assertGreater(len(self.common_data[field]), 0, f"{field} 不應該為空")
    
    def test_puns_content(self):
        """測試雙關語內容"""
        pun_fields = ['common_puns', 'halloween_pickup_lines', 'nsfw_puns']
        
        for field in pun_fields:
            puns = self.common_data[field]
            for i, pun in enumerate(puns):
                with self.subTest(field=field, index=i):
                    self.assertIsInstance(pun, str, f"{field}[{i}] 應該是字串")
                    self.assertGreater(len(pun.strip()), 0, f"{field}[{i}] 不應該為空")
    
    def test_character_types(self):
        """測試角色類型"""
        if 'character_types' in self.common_data:
            char_types = self.common_data['character_types']
            self.assertIsInstance(char_types, dict, "character_types 應該是字典格式")
            
            # 檢查是否有常見的萬聖節角色
            expected_chars = ['witch', 'ghost', 'vampire', 'werewolf', 'zombie']
            for char in expected_chars:
                self.assertIn(char, char_types, f"缺少常見角色: {char}")
    
    def test_locations(self):
        """測試地點"""
        if 'locations' in self.common_data:
            locations = self.common_data['locations']
            self.assertIsInstance(locations, dict, "locations 應該是字典格式")
            
            # 檢查是否有常見的萬聖節地點
            expected_locations = ['haunted_house', 'pumpkin_patch', 'graveyard']
            for location in expected_locations:
                self.assertIn(location, locations, f"缺少常見地點: {location}")


class TestGameLogic(unittest.TestCase):
    """測試遊戲邏輯"""
    
    def setUp(self):
        """設定測試環境"""
        # 匯入遊戲類別
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from main import HalloweenAdventure
        
        self.game = HalloweenAdventure()
        self.game.load_stories()
    
    def test_game_initialization(self):
        """測試遊戲初始化"""
        self.assertEqual(self.game.current_scene, "start")
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.visited_scenes), 0)
        self.assertEqual(self.game.player_name, "")
    
    def test_story_loading(self):
        """測試故事載入"""
        self.assertIsInstance(self.game.story_data, dict)
        self.assertGreater(len(self.game.story_data), 0)
        self.assertIn('start', self.game.story_data)
    
    def test_scene_display(self):
        """測試場景顯示"""
        # 測試正常場景
        with patch('builtins.print'):
            self.game.display_scene('start')
            self.assertIn('start', self.game.visited_scenes)
        
        # 測試不存在的場景
        with patch('builtins.print'):
            self.game.display_scene('nonexistent')
            # 應該不會拋出異常
    
    def test_score_calculation(self):
        """測試分數計算"""
        initial_score = self.game.score
        
        # 模擬結局場景
        ending_scene = {
            'title': '測試結局',
            'outcome': '測試結果',
            'is_ending': True,
            'score': 50
        }
        
        with patch('builtins.print'), patch('builtins.input', return_value='n'):
            result = self.game.handle_ending(ending_scene)
            self.assertEqual(self.game.score, initial_score + 50)
            self.assertFalse(result)  # 應該返回 False 表示遊戲結束
    
    def test_restart_functionality(self):
        """測試重新開始功能"""
        # 設定一些狀態
        self.game.current_scene = "some_scene"
        self.game.score = 100
        self.game.visited_scenes.add("start")
        
        # 重新開始
        with patch('builtins.print'), patch.object(self.game, 'play', return_value=None):
            self.game.restart_game()
        
        self.assertEqual(self.game.current_scene, "start")
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.visited_scenes), 0)


class TestGameFlow(unittest.TestCase):
    """測試遊戲流程"""
    
    def setUp(self):
        """設定測試環境"""
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from main import HalloweenAdventure
        
        self.game = HalloweenAdventure()
        self.game.load_stories()
    
    def test_start_to_ending_path(self):
        """測試從開始到結局的完整路徑"""
        # 測試一個簡單的路徑
        test_path = ['start', 'witch_encounter', 'broom_ride_success', 'rooftop_romance']
        
        for scene in test_path:
            if scene in self.game.story_data:
                scene_data = self.game.story_data[scene]
                if scene_data.get('is_ending', False):
                    self.assertIn('outcome', scene_data)
                    break
    
    def test_all_endings_reachable(self):
        """測試所有結局都可以到達"""
        ending_scenes = [scene_id for scene_id, scene_data in self.game.story_data.items() 
                        if scene_data.get('is_ending', False)]
        
        for ending_scene in ending_scenes:
            # 檢查是否有場景連接到這個結局
            reachable = False
            for scene_id, scene_data in self.game.story_data.items():
                if 'choices' in scene_data:
                    for choice in scene_data['choices']:
                        if choice['next_scene'] == ending_scene:
                            reachable = True
                            break
                if reachable:
                    break
            
            self.assertTrue(reachable, f"結局場景 {ending_scene} 無法到達")


def run_tests():
    """執行所有測試"""
    # 建立測試套件
    test_suite = unittest.TestSuite()
    
    # 添加測試類別
    test_classes = [TestStoryData, TestGameLogic, TestGameFlow]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # 執行測試
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # 回傳測試結果
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 開始執行 Tsext Adventure 測試...")
    print("=" * 50)
    
    success = run_tests()
    
    print("=" * 50)
    if success:
        print("✅ 所有測試通過！")
        sys.exit(0)
    else:
        print("❌ 部分測試失敗！")
        sys.exit(1)
