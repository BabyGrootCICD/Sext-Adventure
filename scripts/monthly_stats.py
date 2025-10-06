#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月度統計腳本
用於分析月度貢獻數據和生成統計報告

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from collections import defaultdict
import sys

# 添加 scripts 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from github_api import GitHubAPI, ContributorTracker

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MonthlyStatsAnalyzer:
    """月度統計分析器"""
    
    def __init__(self, github_api: GitHubAPI, owner: str, repo: str):
        self.github_api = github_api
        self.owner = owner
        self.repo = repo
        self.tracker = ContributorTracker(github_api, owner, repo)
    
    def analyze_monthly_contributions(self, days: int = 30) -> Dict:
        """分析月度貢獻數據"""
        logger.info(f"開始分析過去 {days} 天的貢獻數據...")
        
        since = datetime.now() - timedelta(days=days)
        
        # 獲取 PR 和 Issue 數據
        prs = self.github_api.get_pull_requests(self.owner, self.repo, since=since)
        issues = self.github_api.get_issues(self.owner, self.repo, since=since)
        
        # 分析數據
        analysis = {
            'period': {
                'start_date': since.strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d'),
                'days': days
            },
            'overall_stats': self._calculate_overall_stats(prs, issues),
            'contributor_stats': self._analyze_contributor_stats(prs, issues),
            'category_analysis': self._analyze_by_category(prs, issues),
            'trend_analysis': self._analyze_trends(prs, issues, days),
            'achievement_analysis': self._analyze_achievements(prs, issues)
        }
        
        logger.info("月度貢獻分析完成")
        return analysis
    
    def _calculate_overall_stats(self, prs: List[Dict], issues: List[Dict]) -> Dict:
        """計算總體統計"""
        total_prs = len(prs)
        total_issues = len(issues)
        merged_prs = len([pr for pr in prs if pr.get('merged_at')])
        
        # 計算活躍貢獻者
        contributors = set()
        for pr in prs:
            contributors.add(pr['user']['login'])
        for issue in issues:
            contributors.add(issue['user']['login'])
        
        return {
            'total_prs': total_prs,
            'merged_prs': merged_prs,
            'total_issues': total_issues,
            'active_contributors': len(contributors),
            'pr_merge_rate': (merged_prs / total_prs * 100) if total_prs > 0 else 0,
            'avg_prs_per_contributor': total_prs / len(contributors) if contributors else 0
        }
    
    def _analyze_contributor_stats(self, prs: List[Dict], issues: List[Dict]) -> Dict:
        """分析貢獻者統計"""
        contributor_stats = defaultdict(lambda: {
            'prs': 0,
            'issues': 0,
            'merged_prs': 0,
            'story_content': 0,
            'technical_improvements': 0,
            'bug_fixes': 0,
            'ui_improvements': 0,
            'community_help': 0,
            'total_score': 0
        })
        
        # 分析 PR
        for pr in prs:
            author = pr['user']['login']
            contributor_stats[author]['prs'] += 1
            
            if pr.get('merged_at'):
                contributor_stats[author]['merged_prs'] += 1
            
            # 分類分析
            category = self._categorize_contribution(pr['title'], pr.get('labels', []))
            contributor_stats[author][category] += 1
        
        # 分析 Issue
        for issue in issues:
            author = issue['user']['login']
            contributor_stats[author]['issues'] += 1
            
            # 社區幫助分數（基於評論數）
            comments = issue.get('comments', 0)
            contributor_stats[author]['community_help'] += comments
        
        # 計算總分
        for author, stats in contributor_stats.items():
            stats['total_score'] = (
                stats['prs'] * 3 +
                stats['issues'] * 1 +
                stats['merged_prs'] * 2 +
                stats['community_help'] * 0.5
            )
        
        return dict(contributor_stats)
    
    def _categorize_contribution(self, title: str, labels: List[Dict]) -> str:
        """分類貢獻類型"""
        title_lower = title.lower()
        label_names = [label['name'].lower() for label in labels]
        
        # 故事內容
        story_keywords = ['story', 'scene', 'content', '劇情', '場景', '結局', 'ending']
        if any(keyword in title_lower for keyword in story_keywords):
            return 'story_content'
        
        # 技術改進
        tech_keywords = ['feature', 'enhancement', '功能', '改進', 'optimization', 'performance']
        if any(keyword in title_lower for keyword in tech_keywords):
            return 'technical_improvements'
        
        # Bug 修復
        bug_keywords = ['bug', 'fix', '修復', '錯誤', 'issue', 'problem']
        if any(keyword in title_lower for keyword in bug_keywords):
            return 'bug_fixes'
        
        # UI 改進
        ui_keywords = ['ui', 'design', 'interface', '界面', '設計', 'css', 'html']
        if any(keyword in title_lower for keyword in ui_keywords):
            return 'ui_improvements'
        
        # 預設為技術改進
        return 'technical_improvements'
    
    def _analyze_by_category(self, prs: List[Dict], issues: List[Dict]) -> Dict:
        """按類別分析"""
        categories = {
            'story_content': {'prs': 0, 'issues': 0, 'contributors': set()},
            'technical_improvements': {'prs': 0, 'issues': 0, 'contributors': set()},
            'bug_fixes': {'prs': 0, 'issues': 0, 'contributors': set()},
            'ui_improvements': {'prs': 0, 'issues': 0, 'contributors': set()}
        }
        
        # 分析 PR
        for pr in prs:
            category = self._categorize_contribution(pr['title'], pr.get('labels', []))
            categories[category]['prs'] += 1
            categories[category]['contributors'].add(pr['user']['login'])
        
        # 分析 Issue
        for issue in issues:
            # Issue 主要歸類為社區幫助
            categories['technical_improvements']['issues'] += 1
            categories['technical_improvements']['contributors'].add(issue['user']['login'])
        
        # 轉換 set 為數量
        for category in categories:
            categories[category]['contributors'] = len(categories[category]['contributors'])
        
        return categories
    
    def _analyze_trends(self, prs: List[Dict], issues: List[Dict], days: int) -> Dict:
        """分析趨勢"""
        # 按日期分組
        daily_stats = defaultdict(lambda: {'prs': 0, 'issues': 0})
        
        for pr in prs:
            date = pr['created_at'][:10]  # YYYY-MM-DD
            daily_stats[date]['prs'] += 1
        
        for issue in issues:
            date = issue['created_at'][:10]
            daily_stats[date]['issues'] += 1
        
        # 計算趨勢
        dates = sorted(daily_stats.keys())
        if len(dates) < 2:
            return {'trend': 'insufficient_data'}
        
        # 簡單的線性趨勢分析
        pr_trend = self._calculate_trend([daily_stats[date]['prs'] for date in dates])
        issue_trend = self._calculate_trend([daily_stats[date]['issues'] for date in dates])
        
        return {
            'pr_trend': pr_trend,
            'issue_trend': issue_trend,
            'daily_stats': dict(daily_stats),
            'most_active_day': max(daily_stats.items(), key=lambda x: x[1]['prs'] + x[1]['issues'])
        }
    
    def _calculate_trend(self, values: List[int]) -> str:
        """計算趨勢方向"""
        if len(values) < 2:
            return 'stable'
        
        # 簡單的趨勢計算
        first_half = sum(values[:len(values)//2]) / (len(values)//2)
        second_half = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        if second_half > first_half * 1.2:
            return 'increasing'
        elif second_half < first_half * 0.8:
            return 'decreasing'
        else:
            return 'stable'
    
    def _analyze_achievements(self, prs: List[Dict], issues: List[Dict]) -> Dict:
        """分析成就相關數據"""
        achievements = {
            'first_time_contributors': set(),
            'high_impact_contributions': [],
            'consistency_scores': {},
            'collaboration_scores': {}
        }
        
        # 分析首次貢獻者
        all_contributors = set()
        for pr in prs:
            all_contributors.add(pr['user']['login'])
        for issue in issues:
            all_contributors.add(issue['user']['login'])
        
        # 這裡可以添加更複雜的首次貢獻者檢測邏輯
        achievements['first_time_contributors'] = list(all_contributors)
        
        # 分析高影響力貢獻
        for pr in prs:
            if pr.get('merged_at'):
                achievements['high_impact_contributions'].append({
                    'author': pr['user']['login'],
                    'title': pr['title'],
                    'url': pr['html_url'],
                    'impact_score': self._calculate_impact_score(pr)
                })
        
        # 按影響力排序
        achievements['high_impact_contributions'].sort(
            key=lambda x: x['impact_score'], reverse=True
        )
        
        return achievements
    
    def _calculate_impact_score(self, pr: Dict) -> float:
        """計算 PR 的影響力分數"""
        score = 1.0
        
        # 基於標籤加分
        labels = [label['name'].lower() for label in pr.get('labels', [])]
        if 'enhancement' in labels:
            score += 2.0
        if 'bug' in labels:
            score += 1.5
        if 'feature' in labels:
            score += 3.0
        
        # 基於評論數加分
        score += pr.get('comments', 0) * 0.1
        
        # 基於檔案變更數加分
        score += pr.get('changed_files', 0) * 0.2
        
        return score
    
    def generate_monthly_report(self, analysis: Dict) -> str:
        """生成月度報告"""
        period = analysis['period']
        overall = analysis['overall_stats']
        contributors = analysis['contributor_stats']
        categories = analysis['category_analysis']
        trends = analysis['trend_analysis']
        achievements = analysis['achievement_analysis']
        
        report = f"""# 📊 Tsext Adventure 月度貢獻報告

## 📅 報告期間
**開始日期**: {period['start_date']}  
**結束日期**: {period['end_date']}  
**分析天數**: {period['days']} 天

## 📈 總體統計

### 核心指標
- **總 Pull Requests**: {overall['total_prs']} 個
- **已合併 PR**: {overall['merged_prs']} 個
- **總 Issues**: {overall['total_issues']} 個
- **活躍貢獻者**: {overall['active_contributors']} 人
- **PR 合併率**: {overall['pr_merge_rate']:.1f}%
- **平均每人 PR 數**: {overall['avg_prs_per_contributor']:.1f} 個

### 趨勢分析
- **PR 趨勢**: {trends.get('pr_trend', 'N/A')}
- **Issue 趨勢**: {trends.get('issue_trend', 'N/A')}
- **最活躍日期**: {trends.get('most_active_day', ('N/A', {}))[0]}

## 🏆 貢獻者排行榜

### 總貢獻分數 Top 10
"""
        
        # 按總分排序貢獻者
        sorted_contributors = sorted(
            contributors.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )[:10]
        
        for i, (author, stats) in enumerate(sorted_contributors, 1):
            report += f"{i}. **@{author}** - {stats['total_score']:.1f} 分 "
            report += f"({stats['prs']} PRs, {stats['issues']} Issues)\n"
        
        report += f"""
## 📊 類別分析

### 故事內容
- **PR 數**: {categories['story_content']['prs']} 個
- **貢獻者**: {categories['story_content']['contributors']} 人

### 技術改進
- **PR 數**: {categories['technical_improvements']['prs']} 個
- **貢獻者**: {categories['technical_improvements']['contributors']} 人

### Bug 修復
- **PR 數**: {categories['bug_fixes']['prs']} 個
- **貢獻者**: {categories['bug_fixes']['contributors']} 人

### UI 改進
- **PR 數**: {categories['ui_improvements']['prs']} 個
- **貢獻者**: {categories['ui_improvements']['contributors']} 人

## 🎯 高影響力貢獻

"""
        
        # 顯示高影響力貢獻
        for contribution in achievements['high_impact_contributions'][:5]:
            report += f"- **[{contribution['title']}]({contribution['url']})** "
            report += f"by @{contribution['author']} "
            report += f"(影響力: {contribution['impact_score']:.1f})\n"
        
        report += f"""
## 🌟 本月亮點

### 首次貢獻者
"""
        
        for contributor in achievements['first_time_contributors'][:5]:
            report += f"- @{contributor}\n"
        
        report += f"""
## 📋 詳細數據

### 貢獻者詳細統計
| 貢獻者 | PRs | Issues | 故事內容 | 技術改進 | Bug修復 | UI改進 | 總分 |
|--------|-----|--------|----------|----------|---------|--------|------|
"""
        
        for author, stats in sorted_contributors:
            report += f"| @{author} | {stats['prs']} | {stats['issues']} | "
            report += f"{stats['story_content']} | {stats['technical_improvements']} | "
            report += f"{stats['bug_fixes']} | {stats['ui_improvements']} | "
            report += f"{stats['total_score']:.1f} |\n"
        
        report += f"""
---

*報告生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*Tsext Adventure 貢獻者追蹤系統*
"""
        
        return report
    
    def save_analysis(self, analysis: Dict, filename: Optional[str] = None) -> str:
        """保存分析結果"""
        if not filename:
            timestamp = datetime.now().strftime('%Y_%m_%d')
            filename = f"monthly_analysis_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"分析結果已保存到: {filename}")
        return filename
    
    def save_report(self, report: str, filename: Optional[str] = None) -> str:
        """保存報告"""
        if not filename:
            timestamp = datetime.now().strftime('%Y_%m')
            filename = f"monthly_report_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"報告已保存到: {filename}")
        return filename


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"
    REPO = "Sext-Adventure"
    
    try:
        # 初始化分析器
        github_api = GitHubAPI()
        analyzer = MonthlyStatsAnalyzer(github_api, OWNER, REPO)
        
        # 分析月度數據
        logger.info("開始月度統計分析...")
        analysis = analyzer.analyze_monthly_contributions(30)
        
        # 生成報告
        logger.info("生成月度報告...")
        report = analyzer.generate_monthly_report(analysis)
        
        # 保存結果
        analysis_file = analyzer.save_analysis(analysis)
        report_file = analyzer.save_report(report)
        
        # 輸出摘要
        overall = analysis['overall_stats']
        print(f"\n📊 月度統計分析完成!")
        print(f"📈 總 PR 數: {overall['total_prs']}")
        print(f"📝 總 Issue 數: {overall['total_issues']}")
        print(f"👥 活躍貢獻者: {overall['active_contributors']}")
        print(f"📋 分析結果: {analysis_file}")
        print(f"📄 月度報告: {report_file}")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
