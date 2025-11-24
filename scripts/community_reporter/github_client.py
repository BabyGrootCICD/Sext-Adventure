#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub API 客戶端
簡化版的 GitHub API 整合，專注於貢獻數據獲取

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHub API 客戶端類別"""
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化 GitHub API 客戶端
        
        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            logger.warning("未提供 GitHub Token，API 請求可能受到限制")
        
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Community-Pulse-Reporter'
        }
        
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """
        獲取倉庫資訊
        
        Args:
            owner: 倉庫擁有者
            repo: 倉庫名稱
            
        Returns:
            倉庫資訊字典
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        """
        獲取貢獻者列表
        
        Args:
            owner: 倉庫擁有者
            repo: 倉庫名稱
            
        Returns:
            貢獻者列表
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        all_contributors = []
        page = 1
        
        while True:
            response = requests.get(
                url, 
                headers=self.headers, 
                params={'per_page': 100, 'page': page}
            )
            response.raise_for_status()
            
            contributors = response.json()
            if not contributors:
                break
                
            all_contributors.extend(contributors)
            page += 1
            
            # 限制最多 1000 個貢獻者
            if len(all_contributors) >= 1000:
                break
        
        return all_contributors
    
    def get_pull_requests(
        self, 
        owner: str, 
        repo: str, 
        state: str = 'all',
        since: Optional[datetime] = None
    ) -> List[Dict]:
        """
        獲取 Pull Request 列表
        
        Args:
            owner: 倉庫擁有者
            repo: 倉庫名稱
            state: PR 狀態 ('open', 'closed', 'all')
            since: 開始時間
            
        Returns:
            PR 列表
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
        params = {'state': state, 'per_page': 100, 'sort': 'created', 'direction': 'desc'}
        
        all_prs = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            prs = response.json()
            if not prs:
                break
            
            # 如果指定了 since，過濾日期
            if since:
                filtered_prs = [
                    pr for pr in prs 
                    if datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00')) >= since
                ]
                all_prs.extend(filtered_prs)
                
                # 如果這一頁有 PR 早於 since，說明後面的都更早，可以停止
                if len(filtered_prs) < len(prs):
                    break
            else:
                all_prs.extend(prs)
            
            page += 1
            
            # 限制
            if len(all_prs) >= 1000:
                break
        
        return all_prs
    
    def get_issues(
        self,
        owner: str,
        repo: str,
        state: str = 'all',
        since: Optional[datetime] = None
    ) -> List[Dict]:
        """
        獲取 Issue 列表（不包含 PR）
        
        Args:
            owner: 倉庫擁有者
            repo: 倉庫名稱
            state: Issue 狀態
            since: 開始時間
            
        Returns:
            Issue 列表
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {'state': state, 'per_page': 100, 'sort': 'created', 'direction': 'desc'}
        
        all_issues = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            issues = response.json()
            if not issues:
                break
            
            # 過濾掉 PR（GitHub API 的 issues endpoint 會包含 PR）
            issues = [issue for issue in issues if 'pull_request' not in issue]
            
            # 如果指定了 since，過濾日期
            if since:
                filtered_issues = [
                    issue for issue in issues
                    if datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00')) >= since
                ]
                all_issues.extend(filtered_issues)
                
                if len(filtered_issues) < len(issues):
                    break
            else:
                all_issues.extend(issues)
            
            page += 1
            
            if len(all_issues) >= 1000:
                break
        
        return all_issues
    
    def get_commits(
        self,
        owner: str,
        repo: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None
    ) -> List[Dict]:
        """
        獲取 Commit 列表
        
        Args:
            owner: 倉庫擁有者
            repo: 倉庫名稱
            since: 開始時間
            until: 結束時間
            
        Returns:
            Commit 列表
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/commits"
        params = {'per_page': 100}
        
        if since:
            params['since'] = since.isoformat()
        if until:
            params['until'] = until.isoformat()
        
        all_commits = []
        page = 1
        
        while True:
            params['page'] = page
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            commits = response.json()
            if not commits:
                break
                
            all_commits.extend(commits)
            page += 1
            
            if len(all_commits) >= 1000:
                break
        
        return all_commits

