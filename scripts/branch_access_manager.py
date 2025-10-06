#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分支存取控制系統
用於根據貢獻者等級管理分支存取權限

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
import logging
import sys

# 添加 scripts 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from github_api import GitHubAPI, ContributorTracker

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BranchAccessManager:
    """分支存取管理器"""
    
    def __init__(self, github_api: GitHubAPI, owner: str, repo: str):
        self.github_api = github_api
        self.owner = owner
        self.repo = repo
        self.tracker = ContributorTracker(github_api, owner, repo)
        
        # 分支存取配置
        self.branch_access_config = {
            'maintainer': {
                'branches': ['main', 'dev', 'feature/*', 'hotfix/*', 'release/*', 'experimental/*'],
                'permissions': {
                    'push': True,
                    'force_push': True,
                    'delete': True,
                    'merge': True,
                    'create_branch': True
                },
                'description': '完整存取權限 - 所有分支'
            },
            'core': {
                'branches': ['main', 'dev', 'feature/*', 'hotfix/*'],
                'permissions': {
                    'push': True,
                    'force_push': False,
                    'delete': False,
                    'merge': True,
                    'create_branch': True
                },
                'description': '核心存取權限 - 主要分支和功能分支'
            },
            'active': {
                'branches': ['dev', 'feature/*'],
                'permissions': {
                    'push': True,
                    'force_push': False,
                    'delete': False,
                    'merge': False,
                    'create_branch': True
                },
                'description': '活躍存取權限 - 開發分支和功能分支'
            },
            'novice': {
                'branches': ['feature/*'],
                'permissions': {
                    'push': True,
                    'force_push': False,
                    'delete': False,
                    'merge': False,
                    'create_branch': True
                },
                'description': '新手存取權限 - 僅功能分支'
            }
        }
        
        # 分支保護規則配置
        self.branch_protection_config = {
            'main': {
                'required_status_checks': {
                    'strict': True,
                    'contexts': ['ci', 'tests', 'lint']
                },
                'enforce_admins': True,
                'required_pull_request_reviews': {
                    'required_approving_review_count': 2,
                    'dismiss_stale_reviews': True,
                    'require_code_owner_reviews': True
                },
                'restrictions': {
                    'users': ['maintainer1', 'maintainer2'],
                    'teams': ['maintainers']
                }
            },
            'dev': {
                'required_status_checks': {
                    'strict': True,
                    'contexts': ['ci', 'tests']
                },
                'enforce_admins': False,
                'required_pull_request_reviews': {
                    'required_approving_review_count': 1,
                    'dismiss_stale_reviews': True,
                    'require_code_owner_reviews': False
                },
                'restrictions': {
                    'users': ['maintainer1', 'core1', 'core2'],
                    'teams': ['maintainers', 'core-contributors']
                }
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
    
    def get_user_branch_access(self, username: str) -> Dict:
        """獲取用戶的分支存取權限"""
        contributor_level = self.get_contributor_level(username)
        access_config = self.branch_access_config[contributor_level]
        
        return {
            'username': username,
            'contributor_level': contributor_level,
            'accessible_branches': access_config['branches'],
            'permissions': access_config['permissions'],
            'description': access_config['description']
        }
    
    def check_branch_access(self, username: str, branch_name: str) -> Dict:
        """檢查用戶對特定分支的存取權限"""
        user_access = self.get_user_branch_access(username)
        accessible_branches = user_access['accessible_branches']
        
        # 檢查是否可以直接存取
        has_access = False
        access_type = 'denied'
        
        for pattern in accessible_branches:
            if self._match_branch_pattern(branch_name, pattern):
                has_access = True
                access_type = 'direct'
                break
        
        # 檢查是否需要 PR
        if not has_access:
            # 檢查是否可以通過 PR 存取
            if self._can_access_via_pr(username, branch_name):
                has_access = True
                access_type = 'via_pr'
        
        return {
            'username': username,
            'branch_name': branch_name,
            'has_access': has_access,
            'access_type': access_type,
            'contributor_level': user_access['contributor_level'],
            'permissions': user_access['permissions'] if has_access else {},
            'message': self._get_access_message(has_access, access_type, user_access['contributor_level'])
        }
    
    def _match_branch_pattern(self, branch_name: str, pattern: str) -> bool:
        """檢查分支名稱是否匹配模式"""
        if pattern == branch_name:
            return True
        
        if pattern.endswith('/*'):
            prefix = pattern[:-2]
            return branch_name.startswith(prefix + '/')
        
        return False
    
    def _can_access_via_pr(self, username: str, branch_name: str) -> bool:
        """檢查是否可以通過 PR 存取分支"""
        contributor_level = self.get_contributor_level(username)
        
        # 所有貢獻者都可以通過 PR 存取任何分支
        return True
    
    def _get_access_message(self, has_access: bool, access_type: str, contributor_level: str) -> str:
        """獲取存取權限訊息"""
        if not has_access:
            return f"❌ 存取被拒絕 - {contributor_level} 等級無法存取此分支"
        
        if access_type == 'direct':
            return f"✅ 直接存取 - {contributor_level} 等級可以直接推送到此分支"
        elif access_type == 'via_pr':
            return f"⚠️ 需要 PR - {contributor_level} 等級需要通過 Pull Request 存取此分支"
        
        return "❓ 未知存取類型"
    
    def setup_branch_protection(self, branch_name: str) -> bool:
        """設定分支保護規則"""
        if branch_name not in self.branch_protection_config:
            logger.warning(f"分支 {branch_name} 沒有保護規則配置")
            return False
        
        try:
            protection_config = self.branch_protection_config[branch_name]
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/branches/{branch_name}/protection"
            
            response = requests.put(url, json=protection_config, headers=self.github_api.headers)
            response.raise_for_status()
            
            logger.info(f"成功設定分支 {branch_name} 的保護規則")
            return True
            
        except Exception as e:
            logger.error(f"設定分支保護規則時發生錯誤: {e}")
            return False
    
    def grant_branch_access(self, username: str, branch_name: str) -> bool:
        """授予分支存取權限"""
        try:
            # 檢查當前存取權限
            access_check = self.check_branch_access(username, branch_name)
            
            if access_check['has_access']:
                logger.info(f"用戶 {username} 已經有分支 {branch_name} 的存取權限")
                return True
            
            # 獲取用戶等級
            contributor_level = self.get_contributor_level(username)
            
            # 根據等級決定存取方式
            if contributor_level in ['maintainer', 'core']:
                # 高級貢獻者可以直接存取
                return self._grant_direct_access(username, branch_name)
            else:
                # 其他貢獻者需要通過 PR
                return self._create_access_pr(username, branch_name)
            
        except Exception as e:
            logger.error(f"授予分支存取權限時發生錯誤: {e}")
            return False
    
    def _grant_direct_access(self, username: str, branch_name: str) -> bool:
        """授予直接存取權限"""
        try:
            # 添加用戶到分支保護規則的允許列表
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/branches/{branch_name}/protection/restrictions/users"
            payload = {'users': [username]}
            
            response = requests.post(url, json=payload, headers=self.github_api.headers)
            response.raise_for_status()
            
            logger.info(f"成功授予用戶 {username} 對分支 {branch_name} 的直接存取權限")
            return True
            
        except Exception as e:
            logger.error(f"授予直接存取權限時發生錯誤: {e}")
            return False
    
    def _create_access_pr(self, username: str, branch_name: str) -> bool:
        """創建存取 PR"""
        try:
            # 創建功能分支
            feature_branch = f"feature/{username}-access-{branch_name}"
            
            # 創建 PR
            pr_title = f"🔓 請求存取分支 {branch_name}"
            pr_body = f"""## 分支存取請求

**請求者**: @{username}
**目標分支**: `{branch_name}`
**請求原因**: 需要存取此分支進行開發工作

### 存取權限說明
- 貢獻者等級: {self.get_contributor_level(username)}
- 請求存取類型: 通過 Pull Request

### 審查要點
- [ ] 確認用戶的貢獻者等級
- [ ] 驗證存取需求的合理性
- [ ] 檢查用戶的歷史貢獻記錄

---
*此 PR 由 Tsext Adventure 分支存取控制系統自動創建*
"""
            
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/pulls"
            payload = {
                'title': pr_title,
                'body': pr_body,
                'head': feature_branch,
                'base': branch_name
            }
            
            response = requests.post(url, json=payload, headers=self.github_api.headers)
            response.raise_for_status()
            
            logger.info(f"成功為用戶 {username} 創建分支 {branch_name} 的存取 PR")
            return True
            
        except Exception as e:
            logger.error(f"創建存取 PR 時發生錯誤: {e}")
            return False
    
    def revoke_branch_access(self, username: str, branch_name: str) -> bool:
        """撤銷分支存取權限"""
        try:
            # 從分支保護規則中移除用戶
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/branches/{branch_name}/protection/restrictions/users/{username}"
            
            response = requests.delete(url, headers=self.github_api.headers)
            response.raise_for_status()
            
            logger.info(f"成功撤銷用戶 {username} 對分支 {branch_name} 的存取權限")
            return True
            
        except Exception as e:
            logger.error(f"撤銷分支存取權限時發生錯誤: {e}")
            return False
    
    def list_branch_access(self) -> Dict:
        """列出所有分支存取權限"""
        logger.info("開始列出所有分支存取權限...")
        
        # 獲取所有貢獻者
        contributors = self.tracker.categorize_contributors()
        
        access_summary = {
            'maintainer': [],
            'core': [],
            'active': [],
            'novice': []
        }
        
        for level, contributor_list in contributors.items():
            for contributor in contributor_list:
                username = contributor['username']
                user_access = self.get_user_branch_access(username)
                
                access_summary[level].append({
                    'username': username,
                    'accessible_branches': user_access['accessible_branches'],
                    'permissions': user_access['permissions'],
                    'description': user_access['description']
                })
        
        return access_summary
    
    def generate_access_report(self) -> str:
        """生成存取權限報告"""
        access_summary = self.list_branch_access()
        
        report = f"""# 🔐 Tsext Adventure 分支存取權限報告

## 📊 存取權限概覽

"""
        
        for level, contributors in access_summary.items():
            if contributors:
                level_config = self.branch_access_config[level]
                report += f"### {level_config['description']}\n\n"
                
                for contributor in contributors:
                    report += f"**@{contributor['username']}**\n"
                    report += f"- 可存取分支: {', '.join(contributor['accessible_branches'])}\n"
                    report += f"- 權限: {', '.join([k for k, v in contributor['permissions'].items() if v])}\n\n"
        
        report += f"""## 🔒 分支保護規則

"""
        
        for branch, config in self.branch_protection_config.items():
            report += f"### {branch} 分支\n"
            report += f"- 必需狀態檢查: {', '.join(config['required_status_checks']['contexts'])}\n"
            report += f"- 必需審查數: {config['required_pull_request_reviews']['required_approving_review_count']}\n"
            report += f"- 限制用戶: {', '.join(config['restrictions']['users'])}\n\n"
        
        report += f"""
## 📋 存取權限等級說明

| 等級 | 可存取分支 | 主要權限 | 描述 |
|------|------------|----------|------|
| 👑 維護者 | 所有分支 | 完整權限 | 可以推送到任何分支，包括 main |
| 🥇 核心貢獻者 | main, dev, feature/* | 推送 + 合併 | 可以推送到主要分支 |
| 🥈 活躍貢獻者 | dev, feature/* | 推送 | 可以推送到開發分支 |
| 🥉 新手貢獻者 | feature/* | 推送 | 只能推送到功能分支 |

## 🚀 如何請求存取權限

1. **自動存取**: 根據你的貢獻者等級自動獲得相應權限
2. **手動請求**: 創建 Issue 標記 `branch-access-request`
3. **PR 請求**: 通過 Pull Request 請求存取特定分支

---

*報告生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*Tsext Adventure 分支存取控制系統*
"""
        
        return report
    
    def save_access_report(self, report: str, filename: Optional[str] = None) -> str:
        """保存存取權限報告"""
        if not filename:
            timestamp = datetime.now().strftime('%Y_%m_%d')
            filename = f"branch_access_report_{timestamp}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"存取權限報告已保存到: {filename}")
        return filename


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"
    REPO = "Sext-Adventure"
    
    try:
        # 初始化分支存取管理器
        github_api = GitHubAPI()
        access_manager = BranchAccessManager(github_api, OWNER, REPO)
        
        # 生成存取權限報告
        logger.info("開始生成分支存取權限報告...")
        report = access_manager.generate_access_report()
        
        # 保存報告
        report_file = access_manager.save_access_report(report)
        
        # 列出存取權限
        access_summary = access_manager.list_branch_access()
        
        # 輸出摘要
        print(f"\n🔐 分支存取權限管理完成!")
        print(f"📊 維護者: {len(access_summary['maintainer'])} 人")
        print(f"🥇 核心貢獻者: {len(access_summary['core'])} 人")
        print(f"🥈 活躍貢獻者: {len(access_summary['active'])} 人")
        print(f"🥉 新手貢獻者: {len(access_summary['novice'])} 人")
        print(f"📄 存取權限報告: {report_file}")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
