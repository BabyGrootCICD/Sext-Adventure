#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tsext Adventure: Halloween Haunt
一個搞笑瑟瑟文字冒險遊戲的萬聖節特別版本

作者: Tsext Adventure Team
授權: MIT License
"""

import json
import os
import random
import sys
from typing import Dict, List, Any


class HalloweenAdventure:
    """萬聖節冒險遊戲主類別"""
    
    def __init__(self):
        self.story_data = {}
        self.current_scene = "start"
        self.player_name = ""
        self.score = 0
        self.visited_scenes = set()
        
    def load_stories(self):
        """載入故事資料"""
        try:
            # 載入萬聖節故事
            with open('stories/halloween.json', 'r', encoding='utf-8') as f:
                self.story_data = json.load(f)
            print("✅ 故事資料載入成功！")
        except FileNotFoundError:
            print("❌ 找不到 stories/halloween.json 檔案")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ JSON 格式錯誤: {e}")
            sys.exit(1)
    
    def display_scene(self, scene_id: str):
        """顯示場景內容"""
        if scene_id not in self.story_data:
            print("❌ 找不到場景資料")
            return
        
        scene = self.story_data[scene_id]
        
        # 顯示場景標題
        print(f"\n{'='*50}")
        print(f"🎃 {scene.get('title', scene_id.upper())} 🎃")
        print(f"{'='*50}")
        
        # 顯示場景描述
        if 'description' in scene:
            print(f"\n{scene['description']}")
        
        # 顯示選擇選項
        if 'choices' in scene:
            print(f"\n你的選擇：")
            for i, choice in enumerate(scene['choices'], 1):
                print(f"{i}. {choice['option']}")
        
        # 如果是結局
        if scene.get('is_ending', False):
            self.handle_ending(scene)
            return
        
        # 記錄已訪問的場景
        self.visited_scenes.add(scene_id)
    
    def handle_ending(self, scene: Dict[str, Any]):
        """處理結局"""
        print(f"\n🎭 結局：{scene.get('title', '未知結局')}")
        if 'outcome' in scene:
            print(f"\n{scene['outcome']}")
        
        # 計算分數
        if 'score' in scene:
            self.score += scene['score']
        
        print(f"\n🏆 你的分數：{self.score}")
        print(f"📍 探索場景數：{len(self.visited_scenes)}")
        
        # 詢問是否重新開始
        while True:
            choice = input("\n是否要重新開始？(y/n): ").lower().strip()
            if choice in ['y', 'yes', '是']:
                self.restart_game()
                break
            elif choice in ['n', 'no', '否']:
                print("👻 感謝遊玩！萬聖節快樂！")
                return False  # 返回 False 表示遊戲結束
            else:
                print("請輸入 y 或 n")
    
    def restart_game(self):
        """重新開始遊戲"""
        self.current_scene = "start"
        self.score = 0
        self.visited_scenes.clear()
        print("\n🔄 重新開始遊戲...")
        return self.play()
    
    def get_user_choice(self, choices: List[Dict[str, Any]]) -> str:
        """獲取用戶選擇"""
        while True:
            try:
                choice_num = input(f"\n請選擇 (1-{len(choices)}): ").strip()
                choice_index = int(choice_num) - 1
                
                if 0 <= choice_index < len(choices):
                    return choices[choice_index]['next_scene']
                else:
                    print(f"請輸入 1 到 {len(choices)} 之間的數字")
            except ValueError:
                print("請輸入有效的數字")
            except KeyboardInterrupt:
                print("\n\n👻 遊戲結束！")
                raise KeyboardInterrupt("用戶中斷遊戲")
    
    def play(self):
        """主要遊戲循環"""
        while True:
            # 顯示當前場景
            self.display_scene(self.current_scene)
            
            # 檢查是否為結局
            if self.story_data.get(self.current_scene, {}).get('is_ending', False):
                break
            
            # 獲取選擇
            scene = self.story_data[self.current_scene]
            if 'choices' in scene:
                next_scene = self.get_user_choice(scene['choices'])
                self.current_scene = next_scene
            else:
                print("❌ 場景沒有選擇選項")
                break
    
    def start(self):
        """開始遊戲"""
        print("🎃" * 20)
        print("    Tsext Adventure: Halloween Haunt")
        print("        萬聖節瑟瑟冒險遊戲")
        print("🎃" * 20)
        
        print("\n⚠️  NSFW 警告：本遊戲包含成人暗示和幽默，適合 18 歲以上玩家")
        
        # 獲取玩家名稱
        while True:
            try:
                name = input("\n請輸入你的名字: ").strip()
                if name:
                    self.player_name = name
                    break
                print("請輸入有效的名字")
            except (EOFError, KeyboardInterrupt):
                print("\n👻 遊戲結束！")
                return
        
        print(f"\n👻 歡迎 {self.player_name}！準備好參加萬聖節靈異約會趴了嗎？")
        print("💡 提示：輸入 'start' 開始遊戲，或直接按 Enter 開始")
        
        try:
            start_input = input().strip().lower()
            if start_input == 'start' or start_input == '':
                self.load_stories()
                self.play()
            else:
                print("👻 感謝遊玩！")
        except (EOFError, KeyboardInterrupt):
            print("\n👻 遊戲結束！")


def main():
    """主函數"""
    game = HalloweenAdventure()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\n\n👻 遊戲結束！")
    except Exception as e:
        print(f"\n❌ 遊戲發生錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
