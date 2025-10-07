#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub API 整合腳本
用於追蹤貢獻者數據和自動化貢獻者認可系統

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GitHubAPI:
    """GitHub API 整合類別"""
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化 GitHub API 客戶端
        
        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}' if self.token else None,
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Tsext-Adventure-Contributor-Tracker'
        }
        # 移除 None 值
        self.headers = {k: v for k, v in self.headers.items() if v is not None}
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """獲取倉庫資訊"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        """獲取貢獻者列表"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_pull_requests(self, owner: str, repo: str, state: str = 'all', 
                         since: Optional[datetime] = None) -> List[Dict]:
        """獲取 Pull Request 列表"""
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {'state': state, 'per_page': 100}
        
        if since:
            params['since'] = since.isoformat()
        
        all_prs = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            prs = response.json()
            if not prs:
                break
                
            all_prs.extend(prs)
            page += 1
            
            # GitHub API 限制
            if len(all_prs) >= 1000:
                break
        
        return all_prs
    
    def get_issues(self, owner: str, repo: str, state: str = 'all',
                  since: Optional[datetime] = None) -> List[Dict]:
        """獲取 Issue 列表"""
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': state, 'per_page': 100}
        
        if since:
            params['since'] = since.isoformat()
        
        all_issues = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            issues = response.json()
            if not issues:
                break
                
            all_issues.extend(issues)
            page += 1
            
            if len(all_issues) >= 1000:
                break
        
        return all_issues
    
    def get_user_pr_count(self, owner: str, repo: str, username: str) -> int:
        """獲取特定用戶的 PR 數量"""
        prs = self.get_pull_requests(owner, repo, state='all')
        return len([pr for pr in prs if pr['user']['login'] == username])
    
    def get_user_issue_count(self, owner: str, repo: str, username: str) -> int:
        """獲取特定用戶的 Issue 數量"""
        issues = self.get_issues(owner, repo, state='all')
        return len([issue for issue in issues if issue['user']['login'] == username])


class ContributorTracker:
    """貢獻者追蹤器"""
    
    def __init__(self, github_api: GitHubAPI, owner: str, repo: str):
        self.github_api = github_api
        self.owner = owner
        self.repo = repo
    
    def categorize_contributors(self) -> Dict[str, List[Dict]]:
        """根據貢獻量分類貢獻者"""
        contributors = self.github_api.get_contributors(self.owner, self.repo)
        
        categories = {
            'maintainer': [],
            'core': [],
            'active': [],
            'novice': []
        }
        
        for contributor in contributors:
            username = contributor['login']
            pr_count = self.github_api.get_user_pr_count(self.owner, self.repo, username)
            issue_count = self.github_api.get_user_issue_count(self.owner, self.repo, username)
            
            # 計算總貢獻分數
            total_score = pr_count * 3 + issue_count  # PR 權重更高
            
            contributor_data = {
                'username': username,
                'avatar_url': contributor['avatar_url'],
                'html_url': contributor['html_url'],
                'contributions': contributor['contributions'],
                'pr_count': pr_count,
                'issue_count': issue_count,
                'total_score': total_score
            }
            
            # 分類邏輯
            if total_score >= 50 or pr_count >= 15:
                categories['maintainer'].append(contributor_data)
            elif total_score >= 20 or pr_count >= 8:
                categories['core'].append(contributor_data)
            elif total_score >= 5 or pr_count >= 2:
                categories['active'].append(contributor_data)
            else:
                categories['novice'].append(contributor_data)
        
        # 按貢獻分數排序
        for category in categories.values():
            category.sort(key=lambda x: x['total_score'], reverse=True)
        
        return categories
    
    def generate_contributors_markdown(self, categories: Dict[str, List[Dict]]) -> str:
        """生成貢獻者 Markdown"""
        markdown = "## 🌟 貢獻者 (Contributors)\n\n"
        
        level_info = {
            'maintainer': {
                'emoji': '👑',
                'name': '專案維護者',
                'description': '長期維護專案的核心成員'
            },
            'core': {
                'emoji': '🥇',
                'name': '核心貢獻者',
                'description': '重大功能開發者'
            },
            'active': {
                'emoji': '🥈',
                'name': '活躍貢獻者',
                'description': '持續貢獻的社區成員'
            },
            'novice': {
                'emoji': '🥉',
                'name': '新手貢獻者',
                'description': '首次貢獻者'
            }
        }
        
        for level, contributors in categories.items():
            if contributors:
                info = level_info[level]
                markdown += f"### {info['emoji']} {info['name']}\n"
                markdown += f"*{info['description']}*\n\n"
                
                for contributor in contributors:
                    markdown += f"- [@{contributor['username']}]({contributor['html_url']}) "
                    markdown += f"- {contributor['pr_count']} PRs, {contributor['issue_count']} Issues "
                    markdown += f"- {contributor['contributions']} 總貢獻\n"
                
                markdown += "\n"
        
        return markdown
    
    def get_monthly_stats(self, days: int = 30) -> Dict[str, Dict]:
        """獲取月度統計數據"""
        since = datetime.now() - timedelta(days=days)
        
        prs = self.github_api.get_pull_requests(self.owner, self.repo, since=since)
        issues = self.github_api.get_issues(self.owner, self.repo, since=since)
        
        stats = {}
        
        # 分析 PR 數據
        for pr in prs:
            author = pr['user']['login']
            if author not in stats:
                stats[author] = {
                    'story_content': 0,
                    'technical_improvements': 0,
                    'bug_fixes': 0,
                    'ui_improvements': 0,
                    'community_help': 0,
                    'total_prs': 0
                }
            
            stats[author]['total_prs'] += 1
            
            # 根據 PR 標籤和標題分類
            labels = [label['name'].lower() for label in pr.get('labels', [])]
            title = pr['title'].lower()
            
            if any(keyword in title for keyword in ['story', 'scene', 'content', '劇情', '場景']):
                stats[author]['story_content'] += 1
            elif any(keyword in title for keyword in ['feature', 'enhancement', '功能', '改進']):
                stats[author]['technical_improvements'] += 1
            elif any(keyword in title for keyword in ['bug', 'fix', '修復', '錯誤']):
                stats[author]['bug_fixes'] += 1
            elif any(keyword in title for keyword in ['ui', 'design', 'interface', '界面', '設計']):
                stats[author]['ui_improvements'] += 1
        
        # 分析 Issue 數據（社區幫助）
        for issue in issues:
            if issue.get('pull_request'):  # 跳過 PR
                continue
                
            author = issue['user']['login']
            if author not in stats:
                stats[author] = {
                    'story_content': 0,
                    'technical_improvements': 0,
                    'bug_fixes': 0,
                    'ui_improvements': 0,
                    'community_help': 0,
                    'total_prs': 0
                }
            
            # 計算社區幫助分數（回答問題、提供建議等）
            comments = issue.get('comments', 0)
            stats[author]['community_help'] += comments
        
        return stats


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"  # 替換為實際的 GitHub 用戶名
    REPO = "Sext-Adventure"   # 替換為實際的倉庫名
    
    # 初始化 GitHub API
    github_api = GitHubAPI()
    tracker = ContributorTracker(github_api, OWNER, REPO)
    
    try:
        # 獲取並分類貢獻者
        logger.info("正在獲取貢獻者數據...")
        categories = tracker.categorize_contributors()
        
        # 生成 Markdown
        logger.info("正在生成貢獻者 Markdown...")
        markdown = tracker.generate_contributors_markdown(categories)
        
        # 保存到檔案
        output_file = "CONTRIBUTORS.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        
        logger.info(f"貢獻者數據已保存到 {output_file}")
        
        # 獲取月度統計
        logger.info("正在獲取月度統計...")
        monthly_stats = tracker.get_monthly_stats()
        
        # 保存月度統計
        stats_file = "monthly_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(monthly_stats, f, ensure_ascii=False, indent=2)
        
        logger.info(f"月度統計已保存到 {stats_file}")
        
        # 輸出摘要
        print("\n📊 貢獻者統計摘要:")
        for level, contributors in categories.items():
            if contributors:
                print(f"  {level}: {len(contributors)} 人")
        
        print(f"\n📈 月度活躍貢獻者: {len(monthly_stats)} 人")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
