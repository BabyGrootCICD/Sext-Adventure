#!/usr/bin/env python3
"""
簡單的場景完整性檢查器
"""

import re
import os

def check_scenarios():
    """檢查場景完整性"""
    html_file = "web/index.html"
    
    if not os.path.exists(html_file):
        print("錯誤: web/index.html 不存在")
        return False
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Tsext Adventure - 場景完整性檢查")
    print("=" * 40)
    
    # 找出所有場景
    scene_pattern = r'"([a-zA-Z_][a-zA-Z0-9_]*)":\s*{'
    scenes = re.findall(scene_pattern, content)
    
    print(f"找到 {len(scenes)} 個場景:")
    for i, scene in enumerate(scenes, 1):
        print(f"  {i:2d}. {scene}")
    
    # 找出結局場景
    ending_pattern = r'"is_ending":\s*true'
    ending_matches = re.findall(ending_pattern, content)
    
    print(f"\n找到 {len(ending_matches)} 個結局場景")
    
    # 找出有選擇的場景
    choices_pattern = r'"choices":\s*\['
    choices_matches = re.findall(choices_pattern, content)
    
    print(f"找到 {len(choices_matches)} 個有選擇的場景")
    
    # 找出所有 next_scene 引用
    next_scene_pattern = r'"next_scene":\s*"([^"]+)"'
    next_scenes = re.findall(next_scene_pattern, content)
    
    print(f"找到 {len(next_scenes)} 個場景引用")
    
    # 檢查引用完整性
    all_referenced = set(next_scenes)
    all_scenes_set = set(scenes)
    
    # 找出未定義的引用
    undefined_refs = all_referenced - all_scenes_set
    
    if undefined_refs:
        print(f"\n[警告] 發現 {len(undefined_refs)} 個未定義的場景引用:")
        for ref in undefined_refs:
            print(f"  - {ref}")
    else:
        print("\n[OK] 所有場景引用都正確定義")
    
    # 找出沒有被引用的場景（除了結局）
    unreferenced = all_scenes_set - all_referenced
    
    # 移除可能的起始場景
    start_scenes = {'start', 'beginning', 'intro'}
    unreferenced = unreferenced - start_scenes
    
    if unreferenced:
        print(f"\n[警告] 發現 {len(unreferenced)} 個未被引用的場景:")
        for scene in unreferenced:
            print(f"  - {scene}")
    else:
        print("\n[OK] 所有場景都被正確引用")
    
    # 計算完整性分數
    total_issues = len(undefined_refs) + len(unreferenced)
    completeness_score = max(0, 100 - (total_issues * 5))
    
    print(f"\n完整性分數: {completeness_score}/100")
    
    if completeness_score == 100:
        print("[完美] 場景結構完美！")
    elif completeness_score >= 80:
        print("[良好] 場景結構良好")
    elif completeness_score >= 60:
        print("[警告] 場景結構需要改進")
    else:
        print("[錯誤] 場景結構有嚴重問題")
    
    print(f"\n統計摘要:")
    print(f"  總場景數: {len(scenes)}")
    print(f"  結局場景: {len(ending_matches)}")
    print(f"  有選擇的場景: {len(choices_matches)}")
    print(f"  場景引用: {len(next_scenes)}")
    print(f"  未定義引用: {len(undefined_refs)}")
    print(f"  未引用場景: {len(unreferenced)}")
    
    return completeness_score >= 80

if __name__ == "__main__":
    success = check_scenarios()
    exit(0 if success else 1)
