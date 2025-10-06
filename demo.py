#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tsext Adventure: Halloween Haunt 演示腳本
展示遊戲的基本功能和故事內容

作者: Tsext Adventure Team
授權: MIT License
"""

import json
import sys
import os


def show_game_info():
    """顯示遊戲資訊"""
    print("🎃" * 50)
    print("    Tsext Adventure: Halloween Haunt")
    print("        萬聖節瑟瑟冒險遊戲")
    print("🎃" * 50)
    print()
    print("📖 遊戲特色:")
    print("  • 搞笑萬聖節雙關語和成人幽默")
    print("  • 多種角色: 女巫、鬼魂、農夫女郎、黑貓")
    print("  • 多個結局: 浪漫、搞笑、冒險、神秘")
    print("  • 互動式故事選擇")
    print("  • 分數和成就系統")
    print()
    print("⚠️  NSFW 警告: 本遊戲包含成人暗示和幽默，適合 18 歲以上玩家")
    print()


def show_story_stats():
    """顯示故事統計資訊"""
    try:
        with open('stories/halloween.json', 'r', encoding='utf-8') as f:
            story_data = json.load(f)
        
        print("📊 故事統計:")
        print(f"  • 總場景數: {len(story_data)}")
        
        # 計算結局場景
        ending_scenes = [scene for scene in story_data.values() if scene.get('is_ending', False)]
        print(f"  • 結局場景數: {len(ending_scenes)}")
        
        # 計算有選擇的場景
        choice_scenes = [scene for scene in story_data.values() if 'choices' in scene]
        print(f"  • 選擇場景數: {len(choice_scenes)}")
        
        # 顯示結局類型
        print("  • 結局類型:")
        for scene in ending_scenes:
            title = scene.get('title', '未知結局')
            score = scene.get('score', 0)
            print(f"    - {title} (分數: {score})")
        
        print()
        
    except FileNotFoundError:
        print("❌ 找不到故事檔案")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")


def show_character_info():
    """顯示角色資訊"""
    try:
        with open('stories/common.json', 'r', encoding='utf-8') as f:
            common_data = json.load(f)
        
        print("👥 角色資訊:")
        if 'character_types' in common_data:
            for char_id, char_name in common_data['character_types'].items():
                print(f"  • {char_name} ({char_id})")
        
        print()
        
    except FileNotFoundError:
        print("❌ 找不到通用資料檔案")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")


def show_sample_puns():
    """顯示範例雙關語"""
    try:
        with open('stories/common.json', 'r', encoding='utf-8') as f:
            common_data = json.load(f)
        
        print("😂 範例雙關語:")
        if 'common_puns' in common_data:
            for i, pun in enumerate(common_data['common_puns'][:3], 1):
                print(f"  {i}. {pun}")
        
        print()
        
    except FileNotFoundError:
        print("❌ 找不到通用資料檔案")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")


def show_achievements():
    """顯示成就系統"""
    try:
        with open('stories/common.json', 'r', encoding='utf-8') as f:
            common_data = json.load(f)
        
        print("🏆 成就系統:")
        if 'achievements' in common_data:
            for achievement_id, achievement_name in common_data['achievements'].items():
                print(f"  • {achievement_name} ({achievement_id})")
        
        print()
        
    except FileNotFoundError:
        print("❌ 找不到通用資料檔案")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式錯誤: {e}")


def show_how_to_play():
    """顯示遊戲玩法"""
    print("🎮 如何遊玩:")
    print("  1. 運行 'python main.py' 啟動遊戲")
    print("  2. 輸入你的名字")
    print("  3. 輸入 'start' 或按 Enter 開始遊戲")
    print("  4. 根據場景描述選擇選項 (輸入數字)")
    print("  5. 享受故事發展和結局")
    print("  6. 在結局時選擇是否重新開始")
    print()
    print("💡 提示:")
    print("  • 每次遊戲都嘗試不同的選擇")
    print("  • 探索所有可能的故事分支")
    print("  • 注意萬聖節雙關語和幽默")
    print("  • 與不同角色互動獲得不同結局")
    print()


def show_contribution_info():
    """顯示貢獻資訊"""
    print("🤝 如何貢獻:")
    print("  • 添加新的故事分支")
    print("  • 創建新的萬聖節雙關語")
    print("  • 修復 Bug 和改進功能")
    print("  • 改進文件和測試")
    print()
    print("📚 更多資訊:")
    print("  • 查看 CONTRIBUTING.md 了解詳細流程")
    print("  • 查看 docs/ 資料夾了解技術文件")
    print("  • 加入 Discord 社群討論")
    print()


def main():
    """主函數"""
    show_game_info()
    show_story_stats()
    show_character_info()
    show_sample_puns()
    show_achievements()
    show_how_to_play()
    show_contribution_info()
    
    print("🎃 準備好開始你的萬聖節冒險了嗎？")
    print("   運行 'python main.py' 開始遊戲！")
    print()
    print("👻 Happy Halloween! 👻")


if __name__ == "__main__":
    main()
