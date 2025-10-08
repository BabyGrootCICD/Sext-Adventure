#!/usr/bin/env python3
"""
格式化聖誕節場景為 HTML 格式
"""

import json

def format_scene_for_html(scene_id, scene_data):
    """格式化單個場景為 HTML 格式"""
    lines = []
    lines.append(f'            "{scene_id}": {{')
    lines.append(f'                "title": "{scene_data["title"]}",')
    
    # 處理描述中的換行
    desc = scene_data["description"].replace('\n', '\\n')
    lines.append(f'                "description": "{desc}",')
    
    if scene_data.get('is_ending', False):
        lines.append(f'                "is_ending": true,')
        outcome = scene_data["outcome"].replace('\n', '\\n')
        lines.append(f'                "outcome": "{outcome}",')
        lines.append(f'                "score": {scene_data["score"]}')
    else:
        lines.append(f'                "choices": [')
        for i, choice in enumerate(scene_data['choices']):
            comma = ',' if i < len(scene_data['choices']) - 1 else ''
            lines.append(f'                    {{"option": "{choice["option"]}", "next_scene": "{choice["next_scene"]}"}}{comma}')
        lines.append(f'                ]')
    
    lines.append(f'            }}')
    return '\n'.join(lines)

def main():
    """主程式"""
    with open('christmas_scenes.json', 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    print("生成 HTML 格式的場景代碼...")
    
    formatted_scenes = []
    for scene_id, scene_data in scenes.items():
        formatted = format_scene_for_html(scene_id, scene_data)
        formatted_scenes.append(formatted)
    
    # 保存到文件
    output = ',\n'.join(formatted_scenes)
    with open('christmas_scenes_formatted.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"已格式化 {len(scenes)} 個場景")
    print("保存到 christmas_scenes_formatted.txt")
    
    # 統計
    endings = sum(1 for s in scenes.values() if s.get('is_ending', False))
    choices = sum(1 for s in scenes.values() if 'choices' in s)
    print(f"\n統計:")
    print(f"  總場景數: {len(scenes)}")
    print(f"  結局場景: {endings}")
    print(f"  選擇場景: {choices}")

if __name__ == "__main__":
    main()
