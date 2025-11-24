#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
貢獻分析器
分析 GitHub 倉庫的貢獻數據並產生統計資訊

作者: Tsext Adventure Team
授權: MIT License
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class ContributionAnalyzer:
    """貢獻分析器類別"""
    
    def __init__(self, github_client, owner: str, repo: str):
        """
        初始化分析器
        
        Args:
            github_client: GitHubClient 實例
            owner: 倉庫擁有者
            repo: 倉庫名稱
        """
        self.client = github_client
        self.owner = owner
        self.repo = repo
    
    def analyze_period(self, days: int = 30) -> Dict:
        """
        分析指定期間的貢獻數據
        
        Args:
            days: 分析的天數
            
        Returns:
            分析結果字典
        """
        logger.info(f"開始分析過去 {days} 天的貢獻數據...")
        
        since = datetime.now() - timedelta(days=days)
        
        # 獲取數據
        prs = self.client.get_pull_requests(self.owner, self.repo, since=since)
        issues = self.client.get_issues(self.owner, self.repo, since=since)
        commits = self.client.get_commits(self.owner, self.repo, since=since)
        
        logger.info(f"獲取到 {len(prs)} 個 PR, {len(issues)} 個 Issue, {len(commits)} 個 Commit")
        
        # 分析數據
        analysis = {
            'period': {
                'start_date': since.strftime('%Y-%m-%d'),
                'end_date': datetime.now().strftime('%Y-%m-%d'),
                'days': days
            },
            'overall_stats': self._calculate_overall_stats(prs, issues, commits),
            'contributor_stats': self._analyze_contributors(prs, issues, commits),
            'leaderboard': self._generate_leaderboard(prs, issues, commits),
            'category_breakdown': self._categorize_contributions(prs, issues)
        }
        
        logger.info("分析完成")
        return analysis
    
    def _calculate_overall_stats(
        self, 
        prs: List[Dict], 
        issues: List[Dict],
        commits: List[Dict]
    ) -> Dict:
        """計算總體統計"""
        total_prs = len(prs)
        merged_prs = len([pr for pr in prs if pr.get('merged_at')])
        total_issues = len(issues)
        total_commits = len(commits)
        
        # 統計獨特貢獻者
        contributors = set()
        for pr in prs:
            if pr.get('user'):
                contributors.add(pr['user']['login'])
        for issue in issues:
            if issue.get('user'):
                contributors.add(issue['user']['login'])
        for commit in commits:
            if commit.get('author') and commit['author']:
                contributors.add(commit['author'].get('login', 'unknown'))
        
        return {
            'total_prs': total_prs,
            'merged_prs': merged_prs,
            'open_prs': total_prs - merged_prs,
            'total_issues': total_issues,
            'total_commits': total_commits,
            'active_contributors': len(contributors),
            'pr_merge_rate': (merged_prs / total_prs * 100) if total_prs > 0 else 0,
            'avg_prs_per_contributor': total_prs / len(contributors) if contributors else 0
        }
    
    def _analyze_contributors(
        self,
        prs: List[Dict],
        issues: List[Dict],
        commits: List[Dict]
    ) -> Dict:
        """分析貢獻者統計"""
        contributor_stats = defaultdict(lambda: {
            'prs': 0,
            'merged_prs': 0,
            'issues': 0,
            'commits': 0,
            'total_score': 0
        })
        
        # 分析 PR
        for pr in prs:
            if pr.get('user'):
                author = pr['user']['login']
                contributor_stats[author]['prs'] += 1
                
                if pr.get('merged_at'):
                    contributor_stats[author]['merged_prs'] += 1
        
        # 分析 Issue
        for issue in issues:
            if issue.get('user'):
                author = issue['user']['login']
                contributor_stats[author]['issues'] += 1
        
        # 分析 Commit
        for commit in commits:
            if commit.get('author') and commit['author']:
                author = commit['author'].get('login', 'unknown')
                if author != 'unknown':
                    contributor_stats[author]['commits'] += 1
        
        # 計算總分（PR 權重最高，然後是 Commit，最後是 Issue）
        for author, stats in contributor_stats.items():
            stats['total_score'] = (
                stats['merged_prs'] * 5 +
                stats['prs'] * 3 +
                stats['commits'] * 2 +
                stats['issues'] * 1
            )
        
        return dict(contributor_stats)
    
    def _generate_leaderboard(
        self,
        prs: List[Dict],
        issues: List[Dict],
        commits: List[Dict]
    ) -> List[Dict]:
        """生成排行榜"""
        contributor_stats = self._analyze_contributors(prs, issues, commits)
        
        # 按總分排序
        leaderboard = [
            {
                'username': username,
                'rank': 0,  # 稍後設定
                **stats
            }
            for username, stats in contributor_stats.items()
        ]
        
        leaderboard.sort(key=lambda x: x['total_score'], reverse=True)
        
        # 設定排名
        for i, contributor in enumerate(leaderboard, 1):
            contributor['rank'] = i
        
        return leaderboard
    
    def _categorize_contributions(
        self,
        prs: List[Dict],
        issues: List[Dict]
    ) -> Dict:
        """按類別分類貢獻"""
        categories = {
            'feature': {'count': 0, 'contributors': set()},
            'bugfix': {'count': 0, 'contributors': set()},
            'documentation': {'count': 0, 'contributors': set()},
            'enhancement': {'count': 0, 'contributors': set()},
            'other': {'count': 0, 'contributors': set()}
        }
        
        # 分析 PR 標籤和標題
        for pr in prs:
            category = self._detect_category(pr)
            categories[category]['count'] += 1
            if pr.get('user'):
                categories[category]['contributors'].add(pr['user']['login'])
        
        # 分析 Issue
        for issue in issues:
            category = self._detect_category(issue)
            categories[category]['count'] += 1
            if issue.get('user'):
                categories[category]['contributors'].add(issue['user']['login'])
        
        # 轉換 set 為數量
        for category in categories:
            categories[category]['contributors'] = len(categories[category]['contributors'])
        
        return categories
    
    def _detect_category(self, item: Dict) -> str:
        """檢測貢獻類別"""
        title = item.get('title', '').lower()
        labels = [label['name'].lower() for label in item.get('labels', [])]
        
        # 功能
        if any(keyword in title for keyword in ['feature', 'add', 'new', '新功能', '新增']):
            return 'feature'
        if any(label in ['feature', 'enhancement'] for label in labels):
            return 'feature'
        
        # Bug 修復
        if any(keyword in title for keyword in ['fix', 'bug', 'bugfix', '修復', '錯誤']):
            return 'bugfix'
        if any(label in ['bug', 'bugfix'] for label in labels):
            return 'bugfix'
        
        # 文檔
        if any(keyword in title for keyword in ['doc', 'documentation', 'readme', '文檔', '說明']):
            return 'documentation'
        if any(label in ['documentation', 'docs'] for label in labels):
            return 'documentation'
        
        # 改進
        if any(keyword in title for keyword in ['improve', 'refactor', 'optimize', '改進', '優化']):
            return 'enhancement'
        if 'enhancement' in labels:
            return 'enhancement'
        
        return 'other'
    
    def get_top_contributors(self, count: int = 10) -> List[Dict]:
        """
        獲取前 N 名貢獻者
        
        Args:
            count: 返回的貢獻者數量
            
        Returns:
            前 N 名貢獻者列表
        """
        analysis = self.analyze_period()
        return analysis['leaderboard'][:count]

