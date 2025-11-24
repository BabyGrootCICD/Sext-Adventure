#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
報告生成器
根據分析結果生成美觀的 Markdown 報告

作者: Tsext Adventure Team
授權: MIT License
"""

from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """報告生成器類別"""
    
    def __init__(self, repo_owner: str, repo_name: str):
        """
        初始化報告生成器
        
        Args:
            repo_owner: 倉庫擁有者
            repo_name: 倉庫名稱
        """
        self.repo_owner = repo_owner
        self.repo_name = repo_name
    
    def generate_report(self, analysis: Dict, include_stats: bool = True) -> str:
        """
        生成完整報告
        
        Args:
            analysis: 分析結果字典
            include_stats: 是否包含詳細統計
            
        Returns:
            Markdown 格式的報告
        """
        logger.info("開始生成報告...")
        
        report_parts = [
            self._generate_header(analysis),
            self._generate_overview(analysis),
            self._generate_leaderboard(analysis),
        ]
        
        if include_stats:
            report_parts.extend([
                self._generate_category_breakdown(analysis),
                self._generate_detailed_stats(analysis)
            ])
        
        report_parts.append(self._generate_footer())
        
        report = '\n\n'.join(report_parts)
        logger.info("報告生成完成")
        return report
    
    def _generate_header(self, analysis: Dict) -> str:
        """生成報告標題"""
        period = analysis['period']
        
        header = f"""# 📊 Community Pulse Report

## {self.repo_owner}/{self.repo_name}

**報告期間 | Report Period**: {period['start_date']} ~ {period['end_date']} ({period['days']} days)

---"""
        
        return header
    
    def _generate_overview(self, analysis: Dict) -> str:
        """生成總覽"""
        stats = analysis['overall_stats']
        
        overview = f"""## 📈 總覽 | Overview

### 核心指標 | Key Metrics

| 指標 Metric | 數量 Count |
|-------------|-----------|
| 👥 活躍貢獻者 Active Contributors | **{stats['active_contributors']}** |
| 🔀 總 Pull Requests | **{stats['total_prs']}** |
| ✅ 已合併 PR Merged PRs | **{stats['merged_prs']}** ({stats['pr_merge_rate']:.1f}%) |
| 📝 總 Issues | **{stats['total_issues']}** |
| 💾 總 Commits | **{stats['total_commits']}** |
| 📊 平均每人 PR 數 Avg PRs/Contributor | **{stats['avg_prs_per_contributor']:.1f}** |"""
        
        return overview
    
    def _generate_leaderboard(self, analysis: Dict) -> str:
        """生成排行榜"""
        leaderboard = analysis['leaderboard'][:10]  # 只顯示前 10 名
        
        if not leaderboard:
            return "## 🏆 貢獻者排行榜 | Contributor Leaderboard\n\n無貢獻者數據 | No contributor data available"
        
        board = """## 🏆 貢獻者排行榜 | Contributor Leaderboard

### 🌟 Top Contributors

| 排名<br>Rank | 貢獻者<br>Contributor | 分數<br>Score | PRs | 已合併<br>Merged | Issues | Commits |
|:---:|---------|:-----:|:---:|:--------:|:------:|:-------:|"""
        
        # 排名表情符號
        medals = {1: '🥇', 2: '🥈', 3: '🥉'}
        
        for contributor in leaderboard:
            rank = contributor['rank']
            medal = medals.get(rank, f"{rank}")
            
            board += f"\n| {medal} | **[@{contributor['username']}](https://github.com/{contributor['username']})** | {contributor['total_score']} | {contributor['prs']} | {contributor['merged_prs']} | {contributor['issues']} | {contributor['commits']} |"
        
        return board
    
    def _generate_category_breakdown(self, analysis: Dict) -> str:
        """生成類別分析"""
        categories = analysis['category_breakdown']
        
        breakdown = """## 📊 貢獻類別分析 | Contribution Categories

### 類別分佈 | Category Distribution

"""
        
        category_names = {
            'feature': '✨ 新功能 Features',
            'bugfix': '🐛 Bug 修復 Bug Fixes',
            'documentation': '📖 文檔 Documentation',
            'enhancement': '⚡ 改進 Enhancements',
            'other': '📦 其他 Others'
        }
        
        # 生成統計表
        breakdown += "| 類別 Category | 數量 Count | 貢獻者 Contributors |\n"
        breakdown += "|--------------|:----------:|:------------------:|\n"
        
        for category, data in categories.items():
            name = category_names.get(category, category)
            breakdown += f"| {name} | {data['count']} | {data['contributors']} |\n"
        
        return breakdown
    
    def _generate_detailed_stats(self, analysis: Dict) -> str:
        """生成詳細統計"""
        contributor_stats = analysis['contributor_stats']
        
        if not contributor_stats:
            return ""
        
        stats = """## 📋 詳細統計 | Detailed Statistics

### 所有貢獻者 | All Contributors

<details>
<summary>點擊展開完整列表 | Click to expand full list</summary>

| 貢獻者 Contributor | PRs | 已合併 Merged | Issues | Commits | 總分 Score |
|-------------------|:---:|:------------:|:------:|:-------:|:----------:|
"""
        
        # 按總分排序
        sorted_contributors = sorted(
            contributor_stats.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        for username, data in sorted_contributors:
            stats += f"| [@{username}](https://github.com/{username}) | {data['prs']} | {data['merged_prs']} | {data['issues']} | {data['commits']} | {data['total_score']} |\n"
        
        stats += "\n</details>"
        
        return stats
    
    def _generate_footer(self) -> str:
        """生成報告頁腳"""
        footer = f"""---

### 📌 關於此報告 | About This Report

此報告由 [Community Pulse Reporter](https://github.com/marketplace/actions/community-pulse-reporter) 自動生成。

**評分規則 | Scoring Rules**:
- 已合併 PR (Merged PR): 5 分
- PR (Pull Request): 3 分  
- Commit: 2 分
- Issue: 1 分

**生成時間 | Generated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

💡 想要為你的專案生成類似報告？[查看使用說明](https://github.com/{self.repo_owner}/{self.repo_name})
"""
        
        return footer
    
    def save_report(self, report: str, filename: str) -> str:
        """
        保存報告到文件
        
        Args:
            report: 報告內容
            filename: 文件名
            
        Returns:
            文件路徑
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"報告已保存到: {filename}")
        return filename
    
    def generate_summary(self, analysis: Dict) -> str:
        """
        生成簡短摘要（用於 GitHub Actions 輸出）
        
        Args:
            analysis: 分析結果
            
        Returns:
            摘要字符串
        """
        stats = analysis['overall_stats']
        leaderboard = analysis['leaderboard'][:3]
        
        summary = f"""## 📊 Community Pulse Summary

### 核心數據
- 👥 活躍貢獻者: {stats['active_contributors']}
- 🔀 總 PRs: {stats['total_prs']} (已合併: {stats['merged_prs']})
- 📝 總 Issues: {stats['total_issues']}
- 💾 總 Commits: {stats['total_commits']}

### 🏆 Top 3 貢獻者
"""
        
        for i, contributor in enumerate(leaderboard, 1):
            medals = {1: '🥇', 2: '🥈', 3: '🥉'}
            summary += f"{medals[i]} @{contributor['username']} - {contributor['total_score']} 分\n"
        
        return summary

