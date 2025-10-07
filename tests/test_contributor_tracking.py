#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
貢獻者追蹤系統測試腳本
測試 GitHub API 整合和貢獻者追蹤功能

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

# 添加 scripts 目錄到 Python 路徑
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from github_api import GitHubAPI, ContributorTracker
from track_contributors import READMEUpdater, ContributionAnalyzer

class TestGitHubAPI(unittest.TestCase):
    """測試 GitHub API 類別"""
    
    def setUp(self):
        """設定測試環境"""
        self.api = GitHubAPI(token="test_token")
        self.owner = "test_owner"
        self.repo = "test_repo"
    
    @patch('requests.get')
    def test_get_repo_info(self, mock_get):
        """測試獲取倉庫資訊"""
        # 模擬 API 回應
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'test_repo',
            'full_name': 'test_owner/test_repo',
            'description': 'Test repository'
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 執行測試
        result = self.api.get_repo_info(self.owner, self.repo)
        
        # 驗證結果
        self.assertEqual(result['name'], 'test_repo')
        self.assertEqual(result['full_name'], 'test_owner/test_repo')
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_get_contributors(self, mock_get):
        """測試獲取貢獻者列表"""
        # 模擬 API 回應
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'login': 'user1',
                'avatar_url': 'https://example.com/avatar1.jpg',
                'html_url': 'https://github.com/user1',
                'contributions': 10
            },
            {
                'login': 'user2',
                'avatar_url': 'https://example.com/avatar2.jpg',
                'html_url': 'https://github.com/user2',
                'contributions': 5
            }
        ]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 執行測試
        result = self.api.get_contributors(self.owner, self.repo)
        
        # 驗證結果
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['login'], 'user1')
        self.assertEqual(result[1]['login'], 'user2')
        mock_get.assert_called_once()


class TestContributorTracker(unittest.TestCase):
    """測試貢獻者追蹤器"""
    
    def setUp(self):
        """設定測試環境"""
        self.mock_api = Mock(spec=GitHubAPI)
        self.tracker = ContributorTracker(self.mock_api, "test_owner", "test_repo")
    
    def test_categorize_contributors(self):
        """測試貢獻者分類"""
        # 模擬 API 回應
        self.mock_api.get_contributors.return_value = [
            {
                'login': 'maintainer',
                'avatar_url': 'https://example.com/maintainer.jpg',
                'html_url': 'https://github.com/maintainer',
                'contributions': 100
            },
            {
                'login': 'novice',
                'avatar_url': 'https://example.com/novice.jpg',
                'html_url': 'https://github.com/novice',
                'contributions': 1
            }
        ]
        
        self.mock_api.get_user_pr_count.side_effect = lambda owner, repo, username: {
            'maintainer': 20,
            'novice': 1
        }.get(username, 0)
        
        self.mock_api.get_user_issue_count.side_effect = lambda owner, repo, username: {
            'maintainer': 10,
            'novice': 0
        }.get(username, 0)
        
        # 執行測試
        result = self.tracker.categorize_contributors()
        
        # 驗證結果
        self.assertIn('maintainer', result)
        self.assertIn('novice', result)
        self.assertEqual(len(result['maintainer']), 1)
        self.assertEqual(len(result['novice']), 1)
        self.assertEqual(result['maintainer'][0]['username'], 'maintainer')
        self.assertEqual(result['novice'][0]['username'], 'novice')
    
    def test_generate_contributors_markdown(self):
        """測試生成貢獻者 Markdown"""
        categories = {
            'maintainer': [{
                'username': 'test_maintainer',
                'avatar_url': 'https://example.com/test.jpg',
                'html_url': 'https://github.com/test_maintainer',
                'contributions': 50,
                'pr_count': 10,
                'issue_count': 5,
                'total_score': 35
            }],
            'novice': []
        }
        
        # 執行測試
        result = self.tracker.generate_contributors_markdown(categories)
        
        # 驗證結果
        self.assertIn('## 🌟 貢獻者 (Contributors)', result)
        self.assertIn('### 👑 專案維護者', result)
        self.assertIn('@test_maintainer', result)
        self.assertIn('10 PRs, 5 Issues', result)


class TestREADMEUpdater(unittest.TestCase):
    """測試 README 更新器"""
    
    def setUp(self):
        """設定測試環境"""
        self.temp_dir = tempfile.mkdtemp()
        self.readme_path = os.path.join(self.temp_dir, 'README.md')
        self.updater = READMEUpdater(self.readme_path)
    
    def tearDown(self):
        """清理測試環境"""
        shutil.rmtree(self.temp_dir)
    
    def test_read_write_readme(self):
        """測試讀寫 README"""
        test_content = "# Test README\n\nThis is a test."
        
        # 寫入測試內容
        self.updater.write_readme(test_content)
        
        # 讀取並驗證
        result = self.updater.read_readme()
        self.assertEqual(result, test_content)
    
    def test_find_contributors_section(self):
        """測試尋找貢獻者區塊"""
        content = """# Test README

## 🌟 貢獻者 (Contributors)
Some content here.

## Other Section
More content.
"""
        
        # 寫入測試內容
        self.updater.write_readme(content)
        
        # 執行測試
        start_pos, end_pos = self.updater.find_contributors_section(content)
        
        # 驗證結果
        self.assertGreater(start_pos, 0)
        self.assertGreater(end_pos, start_pos)
        self.assertIn('## 🌟 貢獻者', content[start_pos:end_pos])
    
    def test_update_contributors_section(self):
        """測試更新貢獻者區塊"""
        original_content = """# Test README

## 🌟 貢獻者 (Contributors)
Old content.

## Other Section
More content.
"""
        
        new_contributors = """## 🌟 貢獻者 (Contributors)

### 👑 專案維護者
- [@test_user](https://github.com/test_user) - Test maintainer
"""
        
        # 寫入原始內容
        self.updater.write_readme(original_content)
        
        # 執行測試
        result = self.updater.update_contributors_section(original_content, new_contributors)
        
        # 驗證結果
        self.assertIn('@test_user', result)
        self.assertNotIn('Old content', result)
        self.assertIn('## Other Section', result)


class TestContributionAnalyzer(unittest.TestCase):
    """測試貢獻分析器"""
    
    def setUp(self):
        """設定測試環境"""
        self.monthly_stats = {
            'user1': {
                'story_content': 3,
                'technical_improvements': 2,
                'bug_fixes': 1,
                'ui_improvements': 0,
                'community_help': 5,
                'total_prs': 6
            },
            'user2': {
                'story_content': 1,
                'technical_improvements': 0,
                'bug_fixes': 2,
                'ui_improvements': 3,
                'community_help': 2,
                'total_prs': 6
            }
        }
        self.analyzer = ContributionAnalyzer(self.monthly_stats)
    
    def test_analyze_contribution_trends(self):
        """測試分析貢獻趨勢"""
        result = self.analyzer.analyze_contribution_trends()
        
        # 驗證結果
        self.assertIn('top_story_contributors', result)
        self.assertIn('top_bug_hunters', result)
        self.assertIn('top_ui_designers', result)
        
        # 驗證排序
        self.assertEqual(result['top_story_contributors'][0]['username'], 'user1')
        self.assertEqual(result['top_bug_hunters'][0]['username'], 'user2')
        self.assertEqual(result['top_ui_designers'][0]['username'], 'user2')
    
    def test_generate_monthly_report(self):
        """測試生成月度報告"""
        result = self.analyzer.generate_monthly_report()
        
        # 驗證結果
        self.assertIn('月度貢獻報告', result)
        self.assertIn('本月之星', result)
        self.assertIn('@user1', result)
        self.assertIn('@user2', result)
        self.assertIn('詳細統計', result)


class TestIntegration(unittest.TestCase):
    """整合測試"""
    
    def test_import_modules(self):
        """測試模組導入"""
        # 測試所有模組都能正確導入
        try:
            from github_api import GitHubAPI, ContributorTracker
            from track_contributors import READMEUpdater, ContributionAnalyzer
            self.assertTrue(True, "所有模組導入成功")
        except ImportError as e:
            self.fail(f"模組導入失敗: {e}")
    
    def test_config_loading(self):
        """測試配置檔案載入"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'contributor_config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            self.assertIn('github', config)
            self.assertIn('contribution_levels', config)
        else:
            self.skipTest("配置檔案不存在")


def mock_open():
    """模擬 open 函數"""
    return MagicMock()


if __name__ == '__main__':
    # 設定測試環境
    print("🧪 開始執行貢獻者追蹤系統測試...")
    print("=" * 50)
    
    # 運行測試
    unittest.main(verbosity=2)
    
    print("=" * 50)
    print("✅ 測試完成！")
