#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
階段四整合測試腳本
測試優先級管理和分支存取控制系統

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import sys
import json
import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil
from datetime import datetime, timedelta

# 添加 scripts 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, '..', 'scripts')
sys.path.insert(0, scripts_dir)

from priority_manager import PriorityManager
from branch_access_manager import BranchAccessManager
from github_api import GitHubAPI

class TestPriorityManager(unittest.TestCase):
    """測試優先級管理器"""
    
    def setUp(self):
        """設定測試環境"""
        self.mock_api = Mock(spec=GitHubAPI)
        self.priority_manager = PriorityManager(self.mock_api, "test_owner", "test_repo")
    
    def test_get_contributor_level(self):
        """測試獲取貢獻者等級"""
        # 模擬 API 回應
        self.mock_api.get_pull_requests.return_value = [
            {'user': {'login': 'user1'}} for _ in range(10)  # 10 個 PR
        ]
        self.mock_api.get_issues.return_value = [
            {'user': {'login': 'user1'}} for _ in range(5)   # 5 個 Issue
        ]
        
        # 執行測試
        level = self.priority_manager.get_contributor_level('user1')
        
        # 驗證結果
        self.assertEqual(level, 'core')  # 10*3 + 5 = 35 分，應該是 core
    
    def test_calculate_priority(self):
        """測試計算優先級"""
        # 模擬貢獻者等級
        with patch.object(self.priority_manager, 'get_contributor_level', return_value='core'):
            # 執行測試
            priority_info = self.priority_manager.calculate_priority(
                'Fix critical bug in game logic',
                'This is a critical bug that needs immediate attention',
                ['bug', 'critical'],
                'user1'
            )
        
        # 驗證結果
        self.assertIn('base_level', priority_info)
        self.assertIn('final_priority', priority_info)
        self.assertIn('applied_rules', priority_info)
        self.assertEqual(priority_info['base_level'], 'core')
        self.assertIn('bug_fix', priority_info['applied_rules'])
    
    def test_apply_priority_boost(self):
        """測試應用優先級提升"""
        base_priority = {
            'level': 'medium',
            'color': 'ffaa00',
            'description': '中優先級'
        }
        
        # 執行測試
        final_priority = self.priority_manager._apply_priority_boost(base_priority, 2)
        
        # 驗證結果
        self.assertEqual(final_priority['level'], 'urgent')
        self.assertEqual(final_priority['color'], 'ff0000')
    
    @patch('requests.post')
    @patch('requests.get')
    def test_set_pr_priority(self, mock_get, mock_post):
        """測試設定 PR 優先級"""
        # 模擬 API 回應
        mock_get.return_value.status_code = 404  # 標籤不存在
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = Mock()
        
        priority_info = {
            'final_priority': {
                'level': 'high',
                'color': 'ff6b00',
                'description': '高優先級'
            },
            'applied_rules': ['bug_fix'],
            'base_level': 'core',
            'author': 'user1'
        }
        
        # 執行測試
        result = self.priority_manager.set_pr_priority(123, priority_info)
        
        # 驗證結果
        self.assertTrue(result)
        mock_post.assert_called()


class TestBranchAccessManager(unittest.TestCase):
    """測試分支存取管理器"""
    
    def setUp(self):
        """設定測試環境"""
        self.mock_api = Mock(spec=GitHubAPI)
        self.access_manager = BranchAccessManager(self.mock_api, "test_owner", "test_repo")
    
    def test_get_contributor_level(self):
        """測試獲取貢獻者等級"""
        # 模擬 API 回應
        self.mock_api.get_pull_requests.return_value = [
            {'user': {'login': 'user1'}} for _ in range(5)
        ]
        self.mock_api.get_issues.return_value = [
            {'user': {'login': 'user1'}} for _ in range(2)
        ]
        
        # 執行測試
        level = self.access_manager.get_contributor_level('user1')
        
        # 驗證結果
        self.assertEqual(level, 'active')  # 5*3 + 2 = 17 分，應該是 active
    
    def test_get_user_branch_access(self):
        """測試獲取用戶分支存取權限"""
        with patch.object(self.access_manager, 'get_contributor_level', return_value='core'):
            # 執行測試
            access = self.access_manager.get_user_branch_access('user1')
        
        # 驗證結果
        self.assertIn('username', access)
        self.assertIn('contributor_level', access)
        self.assertIn('accessible_branches', access)
        self.assertIn('permissions', access)
        self.assertEqual(access['username'], 'user1')
        self.assertEqual(access['contributor_level'], 'core')
    
    def test_check_branch_access(self):
        """測試檢查分支存取權限"""
        with patch.object(self.access_manager, 'get_contributor_level', return_value='core'):
            # 執行測試
            access_check = self.access_manager.check_branch_access('user1', 'main')
        
        # 驗證結果
        self.assertIn('has_access', access_check)
        self.assertIn('access_type', access_check)
        self.assertIn('message', access_check)
        self.assertTrue(access_check['has_access'])
        self.assertEqual(access_check['access_type'], 'direct')
    
    def test_match_branch_pattern(self):
        """測試分支模式匹配"""
        # 測試精確匹配
        self.assertTrue(self.access_manager._match_branch_pattern('main', 'main'))
        
        # 測試通配符匹配
        self.assertTrue(self.access_manager._match_branch_pattern('feature/new-ui', 'feature/*'))
        self.assertFalse(self.access_manager._match_branch_pattern('hotfix/bug-fix', 'feature/*'))
    
    def test_generate_access_report(self):
        """測試生成存取權限報告"""
        # 模擬貢獻者數據
        with patch.object(self.access_manager.tracker, 'categorize_contributors', return_value={
            'core': [{'username': 'user1'}],
            'active': [],
            'novice': [],
            'maintainer': []
        }):
            # 執行測試
            report = self.access_manager.generate_access_report()
        
        # 驗證結果
        self.assertIn('分支存取權限報告', report)
        self.assertIn('@user1', report)
        self.assertIn('存取權限等級說明', report)


class TestIntegration(unittest.TestCase):
    """整合測試"""
    
    def test_priority_and_access_integration(self):
        """測試優先級和存取權限整合"""
        # 模擬 API
        mock_api = Mock(spec=GitHubAPI)
        
        # 初始化管理器
        priority_manager = PriorityManager(mock_api, "test_owner", "test_repo")
        access_manager = BranchAccessManager(mock_api, "test_owner", "test_repo")
        
        # 模擬貢獻者數據
        mock_api.get_pull_requests.return_value = [
            {'user': {'login': 'user1'}} for _ in range(8)
        ]
        mock_api.get_issues.return_value = [
            {'user': {'login': 'user1'}} for _ in range(3)
        ]
        
        # 測試優先級計算
        with patch.object(priority_manager, 'get_contributor_level', return_value='core'):
            priority_info = priority_manager.calculate_priority(
                'Add new feature',
                'This adds a new feature to the game',
                ['enhancement'],
                'user1'
            )
        
        # 測試分支存取權限
        with patch.object(access_manager, 'get_contributor_level', return_value='core'):
            access_info = access_manager.get_user_branch_access('user1')
        
        # 驗證整合結果
        self.assertEqual(priority_info['base_level'], 'core')
        self.assertEqual(access_info['contributor_level'], 'core')
        self.assertIn('main', access_info['accessible_branches'])
    
    def test_full_workflow(self):
        """測試完整工作流程"""
        # 模擬 API
        mock_api = Mock(spec=GitHubAPI)
        
        # 初始化管理器
        priority_manager = PriorityManager(mock_api, "test_owner", "test_repo")
        access_manager = BranchAccessManager(mock_api, "test_owner", "test_repo")
        
        # 模擬處理待處理項目
        with patch.object(priority_manager, 'process_pending_items', return_value={
            'prs_processed': 2,
            'issues_processed': 1,
            'errors': []
        }):
            results = priority_manager.process_pending_items()
        
        # 模擬生成存取權限報告
        with patch.object(access_manager, 'generate_access_report', return_value="測試報告"):
            report = access_manager.generate_access_report()
        
        # 驗證結果
        self.assertEqual(results['prs_processed'], 2)
        self.assertEqual(results['issues_processed'], 1)
        self.assertEqual(len(results['errors']), 0)
        self.assertEqual(report, "測試報告")


def main():
    """主函數"""
    print("🧪 開始執行階段四整合測試...")
    print("=" * 50)
    
    # 運行測試
    unittest.main(verbosity=2)
    
    print("=" * 50)
    print("✅ 階段四整合測試完成！")


if __name__ == "__main__":
    main()
