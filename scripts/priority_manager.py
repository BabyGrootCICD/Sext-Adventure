#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions 優先級管理系統
用於根據貢獻者等級自動設定 PR 和 Issue 的優先級

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

from github_api import GitHubAPI, ContributorTracker

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PriorityManager:
    """優先級管理器"""
    
    def __init__(self, github_api: GitHubAPI, owner: str, repo: str):
        self.github_api = github_api
        self.owner = owner
        self.repo = repo
        self.tracker = ContributorTracker(github_api, owner, repo)
        
        # 優先級配置
        self.priority_config = {
            'maintainer': {
                'level': 'high',
                'color': 'ff0000',  # 紅色
                'description': '高優先級 - 維護者 PR',
                'auto_assign_reviewers': True,
                'auto_merge': False,
                'urgent_threshold': 1  # 1 小時內處理
            },
            'core': {
                'level': 'high',
                'color': 'ff6b00',  # 橙色
                'description': '高優先級 - 核心貢獻者 PR',
                'auto_assign_reviewers': True,
                'auto_merge': False,
                'urgent_threshold': 4  # 4 小時內處理
            },
            'active': {
                'level': 'medium',
                'color': 'ffaa00',  # 黃色
                'description': '中優先級 - 活躍貢獻者 PR',
                'auto_assign_reviewers': False,
                'auto_merge': False,
                'urgent_threshold': 24  # 24 小時內處理
            },
            'novice': {
                'level': 'normal',
                'color': '00aaff',  # 藍色
                'description': '普通優先級 - 新手貢獻者 PR',
                'auto_assign_reviewers': False,
                'auto_merge': False,
                'urgent_threshold': 72  # 72 小時內處理
            }
        }
        
        # 特殊優先級規則
        self.special_rules = {
            'bug_fix': {
                'priority_boost': 2,  # 提升 2 個等級
                'keywords': ['bug', 'fix', '修復', '錯誤', 'issue', 'problem']
            },
            'security': {
                'priority_boost': 3,  # 提升 3 個等級
                'keywords': ['security', 'vulnerability', '安全', '漏洞', 'cve']
            },
            'urgent': {
                'priority_boost': 2,  # 提升 2 個等級
                'keywords': ['urgent', 'critical', '緊急', '關鍵', 'hotfix']
            },
            'feature': {
                'priority_boost': 1,  # 提升 1 個等級
                'keywords': ['feature', 'enhancement', '功能', '改進', 'new']
            }
        }
    
    def get_contributor_level(self, username: str) -> str:
        """獲取貢獻者等級"""
        try:
            # 獲取用戶的 PR 和 Issue 數據
            prs = self.github_api.get_pull_requests(self.owner, self.repo, state='all')
            issues = self.github_api.get_issues(self.owner, self.repo, state='all')
            
            user_prs = [pr for pr in prs if pr['user']['login'] == username]
            user_issues = [issue for issue in issues if issue['user']['login'] == username]
            
            # 計算貢獻分數
            total_score = len(user_prs) * 3 + len(user_issues)
            
            # 根據分數分類
            if total_score >= 50 or len(user_prs) >= 15:
                return 'maintainer'
            elif total_score >= 20 or len(user_prs) >= 8:
                return 'core'
            elif total_score >= 5 or len(user_prs) >= 2:
                return 'active'
            else:
                return 'novice'
                
        except Exception as e:
            logger.error(f"獲取貢獻者等級時發生錯誤: {e}")
            return 'novice'
    
    def calculate_priority(self, title: str, body: str, labels: List[str], 
                          author: str) -> Dict:
        """計算優先級"""
        # 獲取基礎優先級
        contributor_level = self.get_contributor_level(author)
        base_priority = self.priority_config[contributor_level]
        
        # 檢查特殊規則
        priority_boost = 0
        applied_rules = []
        
        content = (title + ' ' + body).lower()
        label_names = [label.lower() for label in labels]
        
        for rule_name, rule_config in self.special_rules.items():
            keywords = rule_config['keywords']
            
            # 檢查標題和內容
            if any(keyword in content for keyword in keywords):
                priority_boost = max(priority_boost, rule_config['priority_boost'])
                applied_rules.append(rule_name)
            
            # 檢查標籤
            if any(keyword in label_names for keyword in keywords):
                priority_boost = max(priority_boost, rule_config['priority_boost'])
                applied_rules.append(f"{rule_name}_label")
        
        # 計算最終優先級
        final_priority = self._apply_priority_boost(base_priority, priority_boost)
        
        return {
            'base_level': contributor_level,
            'base_priority': base_priority,
            'priority_boost': priority_boost,
            'applied_rules': applied_rules,
            'final_priority': final_priority,
            'author': author
        }
    
    def _apply_priority_boost(self, base_priority: Dict, boost: int) -> Dict:
        """應用優先級提升"""
        priority_levels = ['normal', 'medium', 'high', 'urgent']
        
        current_index = priority_levels.index(base_priority['level'])
        new_index = min(current_index + boost, len(priority_levels) - 1)
        
        new_level = priority_levels[new_index]
        
        # 更新配置
        final_priority = base_priority.copy()
        final_priority['level'] = new_level
        
        # 根據新等級調整顏色和描述
        color_map = {
            'normal': '00aaff',  # 藍色
            'medium': 'ffaa00',  # 黃色
            'high': 'ff6b00',    # 橙色
            'urgent': 'ff0000'   # 紅色
        }
        
        final_priority['color'] = color_map[new_level]
        final_priority['description'] = f"{new_level.title()} 優先級"
        
        return final_priority
    
    def set_pr_priority(self, pr_number: int, priority_info: Dict) -> bool:
        """設定 PR 優先級"""
        try:
            # 添加優先級標籤
            label_name = f"priority-{priority_info['final_priority']['level']}"
            label_color = priority_info['final_priority']['color']
            label_description = priority_info['final_priority']['description']
            
            # 確保標籤存在
            self._ensure_label_exists(label_name, label_color, label_description)
            
            # 添加標籤到 PR
            self._add_label_to_pr(pr_number, label_name)
            
            # 添加特殊規則標籤
            for rule in priority_info['applied_rules']:
                rule_label = f"rule-{rule}"
                self._ensure_label_exists(rule_label, '00ff00', f"特殊規則: {rule}")
                self._add_label_to_pr(pr_number, rule_label)
            
            # 自動分配審查者
            if priority_info['final_priority'].get('auto_assign_reviewers'):
                self._assign_reviewers(pr_number, priority_info['base_level'])
            
            # 添加優先級評論
            self._add_priority_comment(pr_number, priority_info)
            
            logger.info(f"成功設定 PR #{pr_number} 的優先級為 {priority_info['final_priority']['level']}")
            return True
            
        except Exception as e:
            logger.error(f"設定 PR 優先級時發生錯誤: {e}")
            return False
    
    def set_issue_priority(self, issue_number: int, priority_info: Dict) -> bool:
        """設定 Issue 優先級"""
        try:
            # 添加優先級標籤
            label_name = f"priority-{priority_info['final_priority']['level']}"
            label_color = priority_info['final_priority']['color']
            label_description = priority_info['final_priority']['description']
            
            # 確保標籤存在
            self._ensure_label_exists(label_name, label_color, label_description)
            
            # 添加標籤到 Issue
            self._add_label_to_issue(issue_number, label_name)
            
            # 添加特殊規則標籤
            for rule in priority_info['applied_rules']:
                rule_label = f"rule-{rule}"
                self._ensure_label_exists(rule_label, '00ff00', f"特殊規則: {rule}")
                self._add_label_to_issue(issue_number, rule_label)
            
            # 自動分配處理者
            if priority_info['final_priority'].get('auto_assign_reviewers'):
                self._assign_issue_handler(issue_number, priority_info['base_level'])
            
            # 添加優先級評論
            self._add_priority_comment(issue_number, priority_info, is_issue=True)
            
            logger.info(f"成功設定 Issue #{issue_number} 的優先級為 {priority_info['final_priority']['level']}")
            return True
            
        except Exception as e:
            logger.error(f"設定 Issue 優先級時發生錯誤: {e}")
            return False
    
    def _ensure_label_exists(self, label_name: str, color: str, description: str):
        """確保標籤存在"""
        try:
            # 檢查標籤是否存在
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/labels/{label_name}"
            response = requests.get(url, headers=self.github_api.headers)
            
            if response.status_code == 404:
                # 標籤不存在，創建它
                create_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/labels"
                payload = {
                    'name': label_name,
                    'color': color,
                    'description': description
                }
                
                response = requests.post(create_url, json=payload, headers=self.github_api.headers)
                response.raise_for_status()
                logger.info(f"成功創建標籤: {label_name}")
            
        except Exception as e:
            logger.error(f"確保標籤存在時發生錯誤: {e}")
    
    def _add_label_to_pr(self, pr_number: int, label_name: str):
        """添加標籤到 PR"""
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{pr_number}/labels"
        payload = {'labels': [label_name]}
        
        response = requests.post(url, json=payload, headers=self.github_api.headers)
        response.raise_for_status()
    
    def _add_label_to_issue(self, issue_number: int, label_name: str):
        """添加標籤到 Issue"""
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{issue_number}/labels"
        payload = {'labels': [label_name]}
        
        response = requests.post(url, json=payload, headers=self.github_api.headers)
        response.raise_for_status()
    
    def _assign_reviewers(self, pr_number: int, contributor_level: str):
        """分配審查者"""
        # 根據貢獻者等級分配不同的審查者
        reviewer_map = {
            'maintainer': ['maintainer1', 'maintainer2'],
            'core': ['maintainer1'],
            'active': ['core1'],
            'novice': ['active1']
        }
        
        reviewers = reviewer_map.get(contributor_level, [])
        
        if reviewers:
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls/{pr_number}/requested_reviewers"
            payload = {'reviewers': reviewers}
            
            try:
                response = requests.post(url, json=payload, headers=self.github_api.headers)
                response.raise_for_status()
                logger.info(f"成功分配審查者給 PR #{pr_number}")
            except Exception as e:
                logger.error(f"分配審查者時發生錯誤: {e}")
    
    def _assign_issue_handler(self, issue_number: int, contributor_level: str):
        """分配 Issue 處理者"""
        # 根據貢獻者等級分配不同的處理者
        handler_map = {
            'maintainer': ['maintainer1'],
            'core': ['core1'],
            'active': ['active1'],
            'novice': ['novice1']
        }
        
        assignees = handler_map.get(contributor_level, [])
        
        if assignees:
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{issue_number}/assignees"
            payload = {'assignees': assignees}
            
            try:
                response = requests.post(url, json=payload, headers=self.github_api.headers)
                response.raise_for_status()
                logger.info(f"成功分配處理者給 Issue #{issue_number}")
            except Exception as e:
                logger.error(f"分配處理者時發生錯誤: {e}")
    
    def _add_priority_comment(self, pr_number: int, priority_info: Dict, is_issue: bool = False):
        """添加優先級評論"""
        item_type = "Issue" if is_issue else "Pull Request"
        
        comment = f"""🤖 **自動優先級設定**

**{item_type} 優先級**: {priority_info['final_priority']['level'].upper()}
**貢獻者等級**: {priority_info['base_level']}
**作者**: @{priority_info['author']}

"""
        
        if priority_info['applied_rules']:
            comment += f"**應用規則**: {', '.join(priority_info['applied_rules'])}\n"
            comment += f"**優先級提升**: +{priority_info['priority_boost']} 等級\n"
        
        comment += f"""
**處理時限**: {priority_info['final_priority'].get('urgent_threshold', 24)} 小時內

---
*此評論由 Tsext Adventure 優先級管理系統自動生成*
"""
        
        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues/{pr_number}/comments"
        payload = {'body': comment}
        
        try:
            response = requests.post(url, json=payload, headers=self.github_api.headers)
            response.raise_for_status()
            logger.info(f"成功添加優先級評論到 {item_type} #{pr_number}")
        except Exception as e:
            logger.error(f"添加優先級評論時發生錯誤: {e}")
    
    def process_pending_items(self) -> Dict:
        """處理待處理的 PR 和 Issue"""
        logger.info("開始處理待處理的 PR 和 Issue...")
        
        results = {
            'prs_processed': 0,
            'issues_processed': 0,
            'errors': []
        }
        
        try:
            # 獲取待處理的 PR
            prs = self.github_api.get_pull_requests(self.owner, self.repo, state='open')
            
            for pr in prs:
                try:
                    # 檢查是否已經設定過優先級
                    labels = [label['name'] for label in pr.get('labels', [])]
                    if any(label.startswith('priority-') for label in labels):
                        continue
                    
                    # 計算優先級
                    priority_info = self.calculate_priority(
                        pr['title'],
                        pr.get('body', ''),
                        labels,
                        pr['user']['login']
                    )
                    
                    # 設定優先級
                    if self.set_pr_priority(pr['number'], priority_info):
                        results['prs_processed'] += 1
                    
                except Exception as e:
                    error_msg = f"處理 PR #{pr['number']} 時發生錯誤: {e}"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)
            
            # 獲取待處理的 Issue
            issues = self.github_api.get_issues(self.owner, self.repo, state='open')
            
            for issue in issues:
                # 跳過 PR（Issue API 也會返回 PR）
                if 'pull_request' in issue:
                    continue
                
                try:
                    # 檢查是否已經設定過優先級
                    labels = [label['name'] for label in issue.get('labels', [])]
                    if any(label.startswith('priority-') for label in labels):
                        continue
                    
                    # 計算優先級
                    priority_info = self.calculate_priority(
                        issue['title'],
                        issue.get('body', ''),
                        labels,
                        issue['user']['login']
                    )
                    
                    # 設定優先級
                    if self.set_issue_priority(issue['number'], priority_info):
                        results['issues_processed'] += 1
                    
                except Exception as e:
                    error_msg = f"處理 Issue #{issue['number']} 時發生錯誤: {e}"
                    results['errors'].append(error_msg)
                    logger.error(error_msg)
            
        except Exception as e:
            error_msg = f"處理待處理項目時發生錯誤: {e}"
            results['errors'].append(error_msg)
            logger.error(error_msg)
        
        logger.info(f"處理完成: {results['prs_processed']} 個 PR, {results['issues_processed']} 個 Issue")
        return results


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"
    REPO = "Sext-Adventure"
    
    try:
        # 初始化優先級管理器
        github_api = GitHubAPI()
        priority_manager = PriorityManager(github_api, OWNER, REPO)
        
        # 處理待處理的項目
        logger.info("開始處理待處理的 PR 和 Issue...")
        results = priority_manager.process_pending_items()
        
        # 輸出結果
        print(f"\n🎯 優先級處理完成!")
        print(f"📝 處理的 PR: {results['prs_processed']} 個")
        print(f"📋 處理的 Issue: {results['issues_processed']} 個")
        
        if results['errors']:
            print(f"❌ 錯誤數量: {len(results['errors'])}")
            for error in results['errors'][:5]:  # 只顯示前5個錯誤
                print(f"  - {error}")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
