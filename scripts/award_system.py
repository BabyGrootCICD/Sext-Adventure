#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自動評選系統
用於自動評選月度貢獻獎項

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import sys

# 添加 scripts 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from monthly_stats import MonthlyStatsAnalyzer
from github_api import GitHubAPI

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AwardSystem:
    """獎項評選系統"""
    
    def __init__(self, github_api: GitHubAPI, owner: str, repo: str):
        self.github_api = github_api
        self.owner = owner
        self.repo = repo
        self.analyzer = MonthlyStatsAnalyzer(github_api, owner, repo)
        
        # 獎項配置
        self.award_categories = {
            'best_story': {
                'name': '🎭 最佳劇情獎',
                'description': '最有創意的故事內容',
                'weight': 3.0,
                'keywords': ['story', 'scene', 'content', '劇情', '場景', '結局', 'ending']
            },
            'technical_innovation': {
                'name': '🛠️ 技術創新獎',
                'description': '最佳技術改進',
                'weight': 2.0,
                'keywords': ['feature', 'enhancement', '功能', '改進', 'optimization', 'performance']
            },
            'bug_hunter': {
                'name': '🐛 Bug獵人獎',
                'description': '發現和修復最多問題',
                'weight': 2.0,
                'keywords': ['bug', 'fix', '修復', '錯誤', 'issue', 'problem']
            },
            'design_master': {
                'name': '🎨 設計大師獎',
                'description': '最佳UI/UX改進',
                'weight': 2.0,
                'keywords': ['ui', 'design', 'interface', '界面', '設計', 'css', 'html']
            },
            'community_star': {
                'name': '🌟 社區之星',
                'description': '最熱心幫助新手的貢獻者',
                'weight': 1.0,
                'keywords': ['help', 'support', '幫助', '支援', 'question', 'answer']
            },
            'consistency_champion': {
                'name': '🔥 持續貢獻獎',
                'description': '最持續穩定的貢獻者',
                'weight': 1.5,
                'keywords': []
            },
            'collaboration_hero': {
                'name': '🤝 協作英雄獎',
                'description': '最善於協作的貢獻者',
                'weight': 1.5,
                'keywords': []
            }
        }
    
    def evaluate_monthly_awards(self, days: int = 30) -> Dict:
        """評選月度獎項"""
        logger.info(f"開始評選過去 {days} 天的月度獎項...")
        
        # 獲取月度分析數據
        analysis = self.analyzer.analyze_monthly_contributions(days)
        contributors = analysis['contributor_stats']
        
        # 評選各類獎項
        awards = {}
        
        for award_id, award_config in self.award_categories.items():
            logger.info(f"評選 {award_config['name']}...")
            winner = self._evaluate_award(award_id, award_config, contributors, analysis)
            if winner:
                awards[award_id] = winner
        
        # 生成評選報告
        report = self._generate_award_report(awards, analysis)
        
        return {
            'period': analysis['period'],
            'awards': awards,
            'report': report,
            'analysis': analysis
        }
    
    def _evaluate_award(self, award_id: str, award_config: Dict, 
                       contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選單個獎項"""
        
        if award_id == 'best_story':
            return self._evaluate_story_award(contributors, analysis)
        elif award_id == 'technical_innovation':
            return self._evaluate_technical_award(contributors, analysis)
        elif award_id == 'bug_hunter':
            return self._evaluate_bug_hunter_award(contributors, analysis)
        elif award_id == 'design_master':
            return self._evaluate_design_award(contributors, analysis)
        elif award_id == 'community_star':
            return self._evaluate_community_award(contributors, analysis)
        elif award_id == 'consistency_champion':
            return self._evaluate_consistency_award(contributors, analysis)
        elif award_id == 'collaboration_hero':
            return self._evaluate_collaboration_award(contributors, analysis)
        
        return None
    
    def _evaluate_story_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選最佳劇情獎"""
        story_scores = {}
        
        for author, stats in contributors.items():
            if stats['story_content'] > 0:
                # 故事內容權重更高
                score = stats['story_content'] * 3.0 + stats['total_score'] * 0.1
                story_scores[author] = {
                    'score': score,
                    'story_count': stats['story_content'],
                    'total_contributions': stats['prs'] + stats['issues']
                }
        
        if not story_scores:
            return None
        
        winner = max(story_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'best_story'
        }
    
    def _evaluate_technical_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選技術創新獎"""
        tech_scores = {}
        
        for author, stats in contributors.items():
            if stats['technical_improvements'] > 0:
                # 技術改進權重
                score = stats['technical_improvements'] * 2.0 + stats['merged_prs'] * 1.5
                tech_scores[author] = {
                    'score': score,
                    'tech_count': stats['technical_improvements'],
                    'merged_prs': stats['merged_prs']
                }
        
        if not tech_scores:
            return None
        
        winner = max(tech_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'technical_innovation'
        }
    
    def _evaluate_bug_hunter_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選Bug獵人獎"""
        bug_scores = {}
        
        for author, stats in contributors.items():
            if stats['bug_fixes'] > 0:
                # Bug修復權重
                score = stats['bug_fixes'] * 2.0 + stats['merged_prs'] * 1.0
                bug_scores[author] = {
                    'score': score,
                    'bug_count': stats['bug_fixes'],
                    'merged_prs': stats['merged_prs']
                }
        
        if not bug_scores:
            return None
        
        winner = max(bug_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'bug_hunter'
        }
    
    def _evaluate_design_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選設計大師獎"""
        design_scores = {}
        
        for author, stats in contributors.items():
            if stats['ui_improvements'] > 0:
                # UI改進權重
                score = stats['ui_improvements'] * 2.0 + stats['total_score'] * 0.1
                design_scores[author] = {
                    'score': score,
                    'ui_count': stats['ui_improvements'],
                    'total_contributions': stats['prs'] + stats['issues']
                }
        
        if not design_scores:
            return None
        
        winner = max(design_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'design_master'
        }
    
    def _evaluate_community_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選社區之星"""
        community_scores = {}
        
        for author, stats in contributors.items():
            if stats['community_help'] > 0:
                # 社區幫助權重
                score = stats['community_help'] * 1.0 + stats['issues'] * 0.5
                community_scores[author] = {
                    'score': score,
                    'help_score': stats['community_help'],
                    'issues_created': stats['issues']
                }
        
        if not community_scores:
            return None
        
        winner = max(community_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'community_star'
        }
    
    def _evaluate_consistency_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選持續貢獻獎"""
        consistency_scores = {}
        
        for author, stats in contributors.items():
            # 基於總貢獻數和一致性
            total_contributions = stats['prs'] + stats['issues']
            if total_contributions >= 3:  # 至少3個貢獻
                # 一致性分數 = 總貢獻數 + 合併率加分
                merge_rate = (stats['merged_prs'] / stats['prs']) if stats['prs'] > 0 else 0
                score = total_contributions + merge_rate * 2.0
                
                consistency_scores[author] = {
                    'score': score,
                    'total_contributions': total_contributions,
                    'merge_rate': merge_rate
                }
        
        if not consistency_scores:
            return None
        
        winner = max(consistency_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'consistency_champion'
        }
    
    def _evaluate_collaboration_award(self, contributors: Dict, analysis: Dict) -> Optional[Dict]:
        """評選協作英雄獎"""
        # 這個獎項需要更複雜的分析，暫時基於總貢獻分數
        collaboration_scores = {}
        
        for author, stats in contributors.items():
            # 基於多樣性貢獻（不同類型的貢獻）
            diversity_score = sum([
                1 if stats['story_content'] > 0 else 0,
                1 if stats['technical_improvements'] > 0 else 0,
                1 if stats['bug_fixes'] > 0 else 0,
                1 if stats['ui_improvements'] > 0 else 0,
                1 if stats['community_help'] > 0 else 0
            ])
            
            if diversity_score >= 2:  # 至少2種不同類型的貢獻
                score = diversity_score * 1.5 + stats['total_score'] * 0.1
                collaboration_scores[author] = {
                    'score': score,
                    'diversity_score': diversity_score,
                    'total_score': stats['total_score']
                }
        
        if not collaboration_scores:
            return None
        
        winner = max(collaboration_scores.items(), key=lambda x: x[1]['score'])
        
        return {
            'winner': winner[0],
            'score': winner[1]['score'],
            'details': winner[1],
            'category': 'collaboration_hero'
        }
    
    def _generate_award_report(self, awards: Dict, analysis: Dict) -> str:
        """生成獎項報告"""
        period = analysis['period']
        overall = analysis['overall_stats']
        
        report = f"""# 🏆 Tsext Adventure 月度貢獻獎獲獎者

## 📅 評選期間
**開始日期**: {period['start_date']}  
**結束日期**: {period['end_date']}  
**評選天數**: {period['days']} 天

## 📊 本期統計
- **總貢獻者**: {overall['active_contributors']} 人
- **總 PR 數**: {overall['total_prs']} 個
- **總 Issue 數**: {overall['total_issues']} 個
- **PR 合併率**: {overall['pr_merge_rate']:.1f}%

## 🎉 獲獎者名單

"""
        
        # 生成各獎項獲獎者
        for award_id, award_data in awards.items():
            award_config = self.award_categories[award_id]
            winner = award_data['winner']
            score = award_data['score']
            details = award_data['details']
            
            report += f"### {award_config['name']}\n"
            report += f"**獲獎者**: @{winner}\n"
            report += f"**評選標準**: {award_config['description']}\n"
            report += f"**評選分數**: {score:.2f}\n"
            
            # 添加詳細信息
            if award_id == 'best_story':
                report += f"**故事內容 PR**: {details['story_count']} 個\n"
            elif award_id == 'technical_innovation':
                report += f"**技術改進 PR**: {details['tech_count']} 個\n"
            elif award_id == 'bug_hunter':
                report += f"**Bug 修復 PR**: {details['bug_count']} 個\n"
            elif award_id == 'design_master':
                report += f"**UI 改進 PR**: {details['ui_count']} 個\n"
            elif award_id == 'community_star':
                report += f"**社區幫助分數**: {details['help_score']:.1f}\n"
            elif award_id == 'consistency_champion':
                report += f"**總貢獻數**: {details['total_contributions']} 個\n"
            elif award_id == 'collaboration_hero':
                report += f"**貢獻多樣性**: {details['diversity_score']} 種類型\n"
            
            report += "\n"
        
        # 添加特別感謝
        report += f"""## 🙏 特別感謝

感謝所有在本月為 Tsext Adventure 做出貢獻的開發者們！

### 所有貢獻者
"""
        
        contributors = analysis['contributor_stats']
        sorted_contributors = sorted(
            contributors.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        for author, stats in sorted_contributors:
            report += f"- **@{author}** - {stats['total_score']:.1f} 分 "
            report += f"({stats['prs']} PRs, {stats['issues']} Issues)\n"
        
        report += f"""
## 🎯 下月目標

讓我們繼續努力，為 Tsext Adventure 創造更多精彩內容！

- 🎭 更多創意故事內容
- 🛠️ 持續技術改進
- 🐛 積極修復問題
- 🎨 優化用戶體驗
- 🌟 加強社區互動

---

*評選時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*Tsext Adventure 自動評選系統*
"""
        
        return report
    
    def save_awards(self, awards_data: Dict, filename: Optional[str] = None) -> str:
        """保存獎項數據"""
        if not filename:
            timestamp = datetime.now().strftime('%Y_%m_%d')
            filename = f"monthly_awards_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(awards_data, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"獎項數據已保存到: {filename}")
        return filename
    
    def save_award_report(self, report: str, filename: Optional[str] = None) -> str:
        """保存獎項報告"""
        if not filename:
            timestamp = datetime.now().strftime('%Y_%m')
            filename = f"monthly_awards_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"獎項報告已保存到: {filename}")
        return filename


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"
    REPO = "Sext-Adventure"
    
    try:
        # 初始化獎項系統
        github_api = GitHubAPI()
        award_system = AwardSystem(github_api, OWNER, REPO)
        
        # 評選月度獎項
        logger.info("開始月度獎項評選...")
        awards_data = award_system.evaluate_monthly_awards(30)
        
        # 保存結果
        awards_file = award_system.save_awards(awards_data)
        report_file = award_system.save_award_report(awards_data['report'])
        
        # 輸出摘要
        awards = awards_data['awards']
        print(f"\n🏆 月度獎項評選完成!")
        print(f"📊 評選獎項數: {len(awards)}")
        
        for award_id, award_data in awards.items():
            award_config = award_system.award_categories[award_id]
            print(f"🎉 {award_config['name']}: @{award_data['winner']}")
        
        print(f"📋 獎項數據: {awards_file}")
        print(f"📄 獎項報告: {report_file}")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
