#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
貢獻者追蹤腳本
自動更新 README.md 中的貢獻者區塊

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List
import logging
import sys

# 添加當前目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from github_api import GitHubAPI, ContributorTracker

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class READMEUpdater:
    """README.md 更新器"""
    
    def __init__(self, readme_path: str = "README.md"):
        self.readme_path = readme_path
    
    def read_readme(self) -> str:
        """讀取 README.md 內容"""
        try:
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"找不到 {self.readme_path} 檔案")
            raise
    
    def write_readme(self, content: str):
        """寫入 README.md 內容"""
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def find_contributors_section(self, content: str) -> tuple:
        """找到貢獻者區塊的位置"""
        # 尋找貢獻者區塊的開始和結束
        start_pattern = r'## 🌟 貢獻者.*?\n'
        end_pattern = r'\n## [^#]'
        
        start_match = re.search(start_pattern, content, re.DOTALL)
        if not start_match:
            # 如果找不到，在 README 末尾添加
            return len(content), len(content)
        
        start_pos = start_match.start()
        
        # 找到下一個 ## 標題
        remaining_content = content[start_pos:]
        end_match = re.search(end_pattern, remaining_content)
        
        if end_match:
            end_pos = start_pos + end_match.start()
        else:
            end_pos = len(content)
        
        return start_pos, end_pos
    
    def update_contributors_section(self, content: str, new_contributors_markdown: str) -> str:
        """更新貢獻者區塊"""
        start_pos, end_pos = self.find_contributors_section(content)
        
        if start_pos == end_pos:
            # 如果找不到現有區塊，在末尾添加
            if not content.endswith('\n'):
                content += '\n'
            content += '\n' + new_contributors_markdown + '\n'
        else:
            # 替換現有區塊
            content = content[:start_pos] + new_contributors_markdown + content[end_pos:]
        
        return content
    
    def add_contribution_stats(self, content: str, stats: Dict) -> str:
        """添加貢獻統計資訊"""
        stats_section = f"""
## 📊 貢獻統計

### 總體數據
- **總貢獻者**: {stats.get('total_contributors', 0)} 人
- **本月活躍**: {stats.get('monthly_active', 0)} 人
- **總 PR 數**: {stats.get('total_prs', 0)} 個
- **總 Issue 數**: {stats.get('total_issues', 0)} 個

### 貢獻者等級分布
- 👑 **維護者**: {stats.get('maintainers', 0)} 人
- 🥇 **核心貢獻者**: {stats.get('core_contributors', 0)} 人
- 🥈 **活躍貢獻者**: {stats.get('active_contributors', 0)} 人
- 🥉 **新手貢獻者**: {stats.get('novice_contributors', 0)} 人

*最後更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # 在貢獻者區塊後添加統計
        contributors_pos = content.find('## 🌟 貢獻者')
        if contributors_pos != -1:
            # 找到貢獻者區塊的結尾
            next_section = content.find('\n## ', contributors_pos + 1)
            if next_section != -1:
                content = content[:next_section] + stats_section + content[next_section:]
            else:
                content += stats_section
        
        return content


class ContributionAnalyzer:
    """貢獻分析器"""
    
    def __init__(self, monthly_stats: Dict):
        self.monthly_stats = monthly_stats
    
    def analyze_contribution_trends(self) -> Dict:
        """分析貢獻趨勢"""
        analysis = {
            'top_story_contributors': [],
            'top_technical_contributors': [],
            'top_bug_hunters': [],
            'top_ui_designers': [],
            'most_helpful': []
        }
        
        for username, stats in self.monthly_stats.items():
            # 故事內容貢獻者
            if stats.get('story_content', 0) > 0:
                analysis['top_story_contributors'].append({
                    'username': username,
                    'count': stats['story_content']
                })
            
            # 技術改進貢獻者
            if stats.get('technical_improvements', 0) > 0:
                analysis['top_technical_contributors'].append({
                    'username': username,
                    'count': stats['technical_improvements']
                })
            
            # Bug 修復者
            if stats.get('bug_fixes', 0) > 0:
                analysis['top_bug_hunters'].append({
                    'username': username,
                    'count': stats['bug_fixes']
                })
            
            # UI 設計師
            if stats.get('ui_improvements', 0) > 0:
                analysis['top_ui_designers'].append({
                    'username': username,
                    'count': stats['ui_improvements']
                })
            
            # 最熱心幫助者
            if stats.get('community_help', 0) > 0:
                analysis['most_helpful'].append({
                    'username': username,
                    'count': stats['community_help']
                })
        
        # 排序
        for key in analysis:
            analysis[key].sort(key=lambda x: x['count'], reverse=True)
            analysis[key] = analysis[key][:5]  # 只保留前5名
        
        return analysis
    
    def generate_monthly_report(self) -> str:
        """生成月度報告"""
        analysis = self.analyze_contribution_trends()
        
        report = f"""
# 📈 月度貢獻報告 - {datetime.now().strftime('%Y年%m月')}

## 🏆 本月之星

### 🎭 最佳劇情獎
"""
        
        if analysis['top_story_contributors']:
            top_story = analysis['top_story_contributors'][0]
            report += f"**🥇 @{top_story['username']}** - {top_story['count']} 個故事內容 PR\n\n"
        else:
            report += "本月無故事內容貢獻\n\n"
        
        report += "### 🛠️ 技術創新獎\n"
        if analysis['top_technical_contributors']:
            top_tech = analysis['top_technical_contributors'][0]
            report += f"**🥇 @{top_tech['username']}** - {top_tech['count']} 個技術改進 PR\n\n"
        else:
            report += "本月無技術改進貢獻\n\n"
        
        report += "### 🐛 Bug獵人獎\n"
        if analysis['top_bug_hunters']:
            top_bug = analysis['top_bug_hunters'][0]
            report += f"**🥇 @{top_bug['username']}** - {top_bug['count']} 個 Bug 修復 PR\n\n"
        else:
            report += "本月無 Bug 修復貢獻\n\n"
        
        report += "### 🎨 設計大師獎\n"
        if analysis['top_ui_designers']:
            top_ui = analysis['top_ui_designers'][0]
            report += f"**🥇 @{top_ui['username']}** - {top_ui['count']} 個 UI/UX 改進 PR\n\n"
        else:
            report += "本月無 UI/UX 改進貢獻\n\n"
        
        report += "### 🌟 社區之星\n"
        if analysis['most_helpful']:
            top_helpful = analysis['most_helpful'][0]
            report += f"**🥇 @{top_helpful['username']}** - {top_helpful['count']} 次社區幫助\n\n"
        else:
            report += "本月無社區幫助記錄\n\n"
        
        report += "## 📊 詳細統計\n\n"
        report += "| 貢獻者 | 故事內容 | 技術改進 | Bug修復 | UI設計 | 社區幫助 |\n"
        report += "|--------|----------|----------|---------|--------|----------|\n"
        
        for username, stats in self.monthly_stats.items():
            report += f"| @{username} | {stats.get('story_content', 0)} | "
            report += f"{stats.get('technical_improvements', 0)} | "
            report += f"{stats.get('bug_fixes', 0)} | "
            report += f"{stats.get('ui_improvements', 0)} | "
            report += f"{stats.get('community_help', 0)} |\n"
        
        return report


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"
    REPO = "Sext-Adventure"
    
    try:
        # 初始化組件
        github_api = GitHubAPI()
        tracker = ContributorTracker(github_api, OWNER, REPO)
        readme_updater = READMEUpdater()
        
        # 獲取貢獻者數據
        logger.info("正在獲取貢獻者數據...")
        categories = tracker.categorize_contributors()
        
        # 生成貢獻者 Markdown
        contributors_markdown = tracker.generate_contributors_markdown(categories)
        
        # 獲取月度統計
        logger.info("正在獲取月度統計...")
        monthly_stats = tracker.get_monthly_stats()
        
        # 讀取現有 README
        logger.info("正在讀取 README.md...")
        readme_content = readme_updater.read_readme()
        
        # 更新貢獻者區塊
        logger.info("正在更新貢獻者區塊...")
        updated_content = readme_updater.update_contributors_section(
            readme_content, contributors_markdown
        )
        
        # 添加統計資訊
        stats = {
            'total_contributors': sum(len(contributors) for contributors in categories.values()),
            'monthly_active': len(monthly_stats),
            'total_prs': sum(stats.get('total_prs', 0) for stats in monthly_stats.values()),
            'total_issues': len(monthly_stats),
            'maintainers': len(categories['maintainer']),
            'core_contributors': len(categories['core']),
            'active_contributors': len(categories['active']),
            'novice_contributors': len(categories['novice'])
        }
        
        updated_content = readme_updater.add_contribution_stats(updated_content, stats)
        
        # 寫入更新後的 README
        logger.info("正在寫入更新後的 README.md...")
        readme_updater.write_readme(updated_content)
        
        # 生成月度報告
        logger.info("正在生成月度報告...")
        analyzer = ContributionAnalyzer(monthly_stats)
        monthly_report = analyzer.generate_monthly_report()
        
        # 保存月度報告
        report_file = f"monthly_report_{datetime.now().strftime('%Y_%m')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(monthly_report)
        
        logger.info(f"月度報告已保存到 {report_file}")
        
        # 輸出摘要
        print("\n✅ 貢獻者追蹤完成!")
        print(f"📊 總貢獻者: {stats['total_contributors']} 人")
        print(f"📈 本月活躍: {stats['monthly_active']} 人")
        print(f"📝 README.md 已更新")
        print(f"📋 月度報告已生成: {report_file}")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
