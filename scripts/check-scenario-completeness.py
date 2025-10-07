#!/usr/bin/env python3
"""
檢查遊戲場景完整性 - 確保所有場景都有對應的結局
"""

import json
import re
import os
from typing import Dict, Set, List, Tuple

class ScenarioChecker:
    def __init__(self, html_file="web/index.html"):
        self.html_file = html_file
        self.scenarios = {}
        self.endings = set()
        self.choices = {}
        self.orphaned_scenarios = set()
        self.unreachable_scenarios = set()
        
    def extract_scenarios(self):
        """從 HTML 檔案中提取場景資料"""
        if not os.path.exists(self.html_file):
            print(f"錯誤: {self.html_file} 不存在")
            return False
            
        with open(self.html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 尋找 storyData 物件
        pattern = r'const storyData = ({.*?});'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print("錯誤: 找不到 storyData 物件")
            return False
            
        try:
            # 解析 JSON 資料
            story_data_str = match.group(1)
            
            # 更強健的 JSON 修正
            # 1. 移除尾隨逗號
            story_data_str = re.sub(r',(\s*[}\]])', r'\1', story_data_str)
            
            # 2. 為未加引號的鍵加上引號
            story_data_str = re.sub(r'(\w+):', r'"\1":', story_data_str)
            
            # 3. 修正可能的 JavaScript 註釋
            story_data_str = re.sub(r'//.*?\n', '\n', story_data_str)
            
            # 4. 修正可能的單引號
            story_data_str = re.sub(r"'([^']*)':", r'"\1":', story_data_str)
            
            # 5. 處理可能的 undefined 值
            story_data_str = re.sub(r':\s*undefined', ': null', story_data_str)
            
            self.scenarios = json.loads(story_data_str)
            print(f"成功提取 {len(self.scenarios)} 個場景")
            return True
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            print("嘗試手動分析場景...")
            
            # 如果 JSON 解析失敗，嘗試手動分析
            return self.manual_scenario_analysis(story_data_str)
    
    def manual_scenario_analysis(self, story_data_str):
        """手動分析場景資料"""
        print("使用手動分析方法...")
        
        # 使用正則表達式找出所有場景
        scene_pattern = r'"([^"]+)":\s*{'
        scenes = re.findall(scene_pattern, story_data_str)
        
        print(f"找到 {len(scenes)} 個場景:")
        for scene in scenes:
            print(f"  - {scene}")
        
        # 找出結局場景
        ending_pattern = r'"is_ending":\s*true'
        endings = re.findall(ending_pattern, story_data_str)
        
        print(f"找到 {len(endings)} 個結局場景")
        
        # 簡單的場景統計
        self.scenarios = {scene: {} for scene in scenes}
        self.endings = set()
        
        # 嘗試找出結局場景
        for scene in scenes:
            scene_block_pattern = rf'"{scene}":\s*{{(.*?)}}'
            scene_match = re.search(scene_block_pattern, story_data_str, re.DOTALL)
            if scene_match:
                scene_content = scene_match.group(1)
                if '"is_ending":\s*true' in scene_content:
                    self.endings.add(scene)
        
        print(f"成功分析 {len(self.scenarios)} 個場景，其中 {len(self.endings)} 個是結局")
        return True
    
    def analyze_scenarios(self):
        """分析場景結構"""
        print("\n分析場景結構...")
        
        # 找出所有結局
        for scene_id, scene_data in self.scenarios.items():
            if scene_data.get('is_ending', False):
                self.endings.add(scene_id)
                print(f"[結局] {scene_id} - {scene_data.get('title', '無標題')}")
        
        # 找出所有選擇和目標場景
        for scene_id, scene_data in self.scenarios.items():
            if 'choices' in scene_data:
                self.choices[scene_id] = []
                for choice in scene_data['choices']:
                    if 'next_scene' in choice:
                        target = choice['next_scene']
                        self.choices[scene_id].append(target)
        
        print(f"\n統計資料:")
        print(f"  總場景數: {len(self.scenarios)}")
        print(f"  結局場景: {len(self.endings)}")
        print(f"  有選擇的場景: {len(self.choices)}")
    
    def find_orphaned_scenarios(self):
        """找出沒有被引用的場景（孤兒場景）"""
        print("\n檢查孤兒場景...")
        
        referenced_scenarios = set()
        
        # 從選擇中找出所有被引用的場景
        for choices_list in self.choices.values():
            for target in choices_list:
                referenced_scenarios.add(target)
        
        # 檢查起始場景
        start_scenarios = ['start', 'beginning', 'intro']
        for start_scene in start_scenarios:
            if start_scene in self.scenarios:
                referenced_scenarios.add(start_scene)
                break
        
        # 找出孤兒場景
        all_scenarios = set(self.scenarios.keys())
        self.orphaned_scenarios = all_scenarios - referenced_scenarios - self.endings
        
        if self.orphaned_scenarios:
            print("[警告] 發現孤兒場景（沒有被引用的場景）:")
            for scene_id in self.orphaned_scenarios:
                scene_data = self.scenarios[scene_id]
                print(f"  - {scene_id}: {scene_data.get('title', '無標題')}")
        else:
            print("[OK] 沒有發現孤兒場景")
    
    def find_unreachable_scenarios(self):
        """找出無法到達的場景"""
        print("\n檢查不可達場景...")
        
        # 從起始場景開始進行深度優先搜索
        visited = set()
        
        def dfs(scene_id):
            if scene_id in visited:
                return
            visited.add(scene_id)
            
            if scene_id in self.choices:
                for target in self.choices[scene_id]:
                    dfs(target)
        
        # 從可能的起始場景開始
        start_scenarios = ['start', 'beginning', 'intro']
        for start_scene in start_scenarios:
            if start_scene in self.scenarios:
                dfs(start_scene)
                break
        
        # 如果找不到起始場景，嘗試從第一個場景開始
        if not visited and self.scenarios:
            first_scene = list(self.scenarios.keys())[0]
            dfs(first_scene)
        
        # 找出不可達場景
        all_scenarios = set(self.scenarios.keys())
        self.unreachable_scenarios = all_scenarios - visited
        
        if self.unreachable_scenarios:
            print("[警告] 發現不可達場景:")
            for scene_id in self.unreachable_scenarios:
                scene_data = self.scenarios[scene_id]
                print(f"  - {scene_id}: {scene_data.get('title', '無標題')}")
        else:
            print("[OK] 沒有發現不可達場景")
    
    def check_scenario_continuity(self):
        """檢查場景的連續性"""
        print("\n檢查場景連續性...")
        
        broken_links = []
        
        for scene_id, choices_list in self.choices.items():
            for i, target in enumerate(choices_list):
                if target not in self.scenarios:
                    broken_links.append({
                        'from': scene_id,
                        'to': target,
                        'choice_index': i
                    })
        
        if broken_links:
            print("[錯誤] 發現斷裂的連結:")
            for link in broken_links:
                scene_data = self.scenarios[link['from']]
                print(f"  - {link['from']} ({scene_data.get('title', '無標題')})")
                print(f"    選擇 {link['choice_index']} 指向不存在的場景: {link['to']}")
        else:
            print("[OK] 所有場景連結都完整")
    
    def generate_report(self):
        """生成檢查報告"""
        print("\n" + "="*60)
        print("場景完整性檢查報告")
        print("="*60)
        
        print(f"\n基本統計:")
        print(f"  總場景數: {len(self.scenarios)}")
        print(f"  結局場景: {len(self.endings)}")
        print(f"  有選擇的場景: {len(self.choices)}")
        print(f"  孤兒場景: {len(self.orphaned_scenarios)}")
        print(f"  不可達場景: {len(self.unreachable_scenarios)}")
        
        # 計算完整性分數
        total_issues = len(self.orphaned_scenarios) + len(self.unreachable_scenarios)
        completeness_score = max(0, 100 - (total_issues * 10))
        
        print(f"\n完整性分數: {completeness_score}/100")
        
        if completeness_score == 100:
            print("[完美] 恭喜！所有場景都完美連接！")
        elif completeness_score >= 80:
            print("[良好] 場景結構良好，只有少數問題需要修復")
        elif completeness_score >= 60:
            print("[警告] 場景結構有一些問題，建議修復")
        else:
            print("[錯誤] 場景結構有嚴重問題，需要大幅修復")
        
        print(f"\n建議:")
        if self.orphaned_scenarios:
            print(f"  - 修復 {len(self.orphaned_scenarios)} 個孤兒場景")
        if self.unreachable_scenarios:
            print(f"  - 修復 {len(self.unreachable_scenarios)} 個不可達場景")
        if completeness_score == 100:
            print("  - 場景結構完美，無需修復")
        
        return completeness_score
    
    def run_check(self):
        """執行完整的場景檢查"""
        print("Tsext Adventure - 場景完整性檢查器")
        print("="*50)
        
        if not self.extract_scenarios():
            return False
        
        self.analyze_scenarios()
        self.find_orphaned_scenarios()
        self.find_unreachable_scenarios()
        self.check_scenario_continuity()
        
        score = self.generate_report()
        return score == 100


def main():
    """主程式"""
    checker = ScenarioChecker()
    success = checker.run_check()
    
    if success:
        print("\n[成功] 場景檢查完成 - 所有場景都完美連接！")
        return 0
    else:
        print("\n[警告] 場景檢查完成 - 發現需要修復的問題")
        return 1


if __name__ == "__main__":
    exit(main())
