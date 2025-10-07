#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
階段三整合測試腳本
測試月度統計、獎項評選和公告系統

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

from monthly_stats import MonthlyStatsAnalyzer
from award_system import AwardSystem
from announcement_system import AnnouncementSystem
from github_api import GitHubAPI

class TestMonthlyStatsAnalyzer(unittest.TestCase):
    """測試月度統計分析器"""
    
    def setUp(self):
        """設定測試環境"""
        self.mock_api = Mock(spec=GitHubAPI)
        self.analyzer = MonthlyStatsAnalyzer(self.mock_api, "test_owner", "test_repo")
    
    def test_analyze_monthly_contributions(self):
        """測試月度貢獻分析"""
        # 模擬 API 回應
        self.mock_api.get_pull_requests.return_value = [
            {
                'user': {'login': 'user1'},
                'title': 'Add new story scene',
                'created_at': '2024-10-01T10:00:00Z',
                'merged_at': '2024-10-01T11:00:00Z',
                'labels': [{'name': 'story'}],
                'comments': 2
            }
        ]
        
        self.mock_api.get_issues.return_value = [
            {
                'user': {'login': 'user2'},
                'title': 'Bug in game logic',
                'created_at': '2024-10-02T10:00:00Z',
                'comments': 5
            }
        ]
        
        # 執行測試
        result = self.analyzer.analyze_monthly_contributions(30)
        
        # 驗證結果
        self.assertIn('period', result)
        self.assertIn('overall_stats', result)
        self.assertIn('contributor_stats', result)
        self.assertIn('category_analysis', result)
        
        # 驗證總體統計
        overall = result['overall_stats']
        self.assertEqual(overall['total_prs'], 1)
        self.assertEqual(overall['total_issues'], 1)
        self.assertEqual(overall['active_contributors'], 2)
    
    def test_generate_monthly_report(self):
        """測試生成月度報告"""
        # 模擬分析數據
        analysis = {
            'period': {
                'start_date': '2024-10-01',
                'end_date': '2024-10-31',
                'days': 30
            },
            'overall_stats': {
                'total_prs': 5,
                'merged_prs': 4,
                'total_issues': 3,
                'active_contributors': 2,
                'pr_merge_rate': 80.0,
                'avg_prs_per_contributor': 2.5
            },
            'contributor_stats': {
                'user1': {
                    'prs': 3,
                    'issues': 1,
                    'total_score': 10.0,
                    'story_content': 2,
                    'technical_improvements': 1,
                    'bug_fixes': 0,
                    'ui_improvements': 0,
                    'community_help': 0
                }
            },
            'category_analysis': {
                'story_content': {'prs': 2, 'contributors': 1},
                'technical_improvements': {'prs': 1, 'contributors': 1},
                'bug_fixes': {'prs': 0, 'contributors': 0},
                'ui_improvements': {'prs': 0, 'contributors': 0}
            },
            'trend_analysis': {
                'pr_trend': 'increasing',
                'issue_trend': 'stable'
            },
            'achievement_analysis': {
                'first_time_contributors': ['user1'],
                'high_impact_contributions': []
            }
        }
        
        # 執行測試
        report = self.analyzer.generate_monthly_report(analysis)
        
        # 驗證結果
        self.assertIn('Tsext Adventure 月度貢獻報告', report)
        self.assertIn('總 Pull Requests: 5', report)
        self.assertIn('活躍貢獻者: 2 人', report)
        self.assertIn('@user1', report)


class TestAwardSystem(unittest.TestCase):
    """測試獎項評選系統"""
    
    def setUp(self):
        """設定測試環境"""
        self.mock_api = Mock(spec=GitHubAPI)
        self.award_system = AwardSystem(self.mock_api, "test_owner", "test_repo")
    
    def test_evaluate_monthly_awards(self):
        """測試月度獎項評選"""
        # 模擬分析數據
        analysis = {
            'period': {
                'start_date': '2024-10-01',
                'end_date': '2024-10-31',
                'days': 30
            },
            'contributor_stats': {
                'user1': {
                    'prs': 3,
                    'issues': 1,
                    'merged_prs': 3,
                    'story_content': 2,
                    'technical_improvements': 1,
                    'bug_fixes': 0,
                    'ui_improvements': 0,
                    'community_help': 5,
                    'total_score': 15.0
                },
                'user2': {
                    'prs': 2,
                    'issues': 2,
                    'merged_prs': 1,
                    'story_content': 0,
                    'technical_improvements': 0,
                    'bug_fixes': 2,
                    'ui_improvements': 0,
                    'community_help': 2,
                    'total_score': 8.0
                }
            }
        }
        
        # 模擬分析器
        with patch.object(self.award_system.analyzer, 'analyze_monthly_contributions', return_value=analysis):
            # 執行測試
            result = self.award_system.evaluate_monthly_awards(30)
        
        # 驗證結果
        self.assertIn('awards', result)
        self.assertIn('report', result)
        
        # 驗證獎項
        awards = result['awards']
        self.assertGreater(len(awards), 0)
        
        # 驗證最佳劇情獎
        if 'best_story' in awards:
            self.assertEqual(awards['best_story']['winner'], 'user1')
    
    def test_generate_award_report(self):
        """測試生成獎項報告"""
        # 模擬獎項數據
        awards = {
            'best_story': {
                'winner': 'user1',
                'score': 8.0,
                'details': {'story_count': 2, 'total_contributions': 4},
                'category': 'best_story'
            }
        }
        
        analysis = {
            'period': {
                'start_date': '2024-10-01',
                'end_date': '2024-10-31',
                'days': 30
            },
            'overall_stats': {
                'active_contributors': 2,
                'total_prs': 5,
                'total_issues': 3,
                'pr_merge_rate': 80.0
            },
            'contributor_stats': {
                'user1': {'total_score': 15.0, 'prs': 3, 'issues': 1},
                'user2': {'total_score': 8.0, 'prs': 2, 'issues': 2}
            }
        }
        
        # 執行測試
        report = self.award_system._generate_award_report(awards, analysis)
        
        # 驗證結果
        self.assertIn('月度貢獻獎獲獎者', report)
        self.assertIn('@user1', report)
        self.assertIn('最佳劇情獎', report)


class TestAnnouncementSystem(unittest.TestCase):
    """測試公告系統"""
    
    def setUp(self):
        """設定測試環境"""
        self.mock_api = Mock(spec=GitHubAPI)
        self.announcement_system = AnnouncementSystem(self.mock_api, "test_owner", "test_repo")
    
    def test_generate_comprehensive_announcement(self):
        """測試生成綜合公告"""
        # 模擬分析數據
        analysis = {
            'period': {
                'start_date': '2024-10-01',
                'end_date': '2024-10-31',
                'days': 30
            },
            'overall_stats': {
                'active_contributors': 2,
                'total_prs': 5,
                'total_issues': 3,
                'pr_merge_rate': 80.0,
                'avg_prs_per_contributor': 2.5
            },
            'contributor_stats': {
                'user1': {'total_score': 15.0, 'prs': 3, 'issues': 1},
                'user2': {'total_score': 8.0, 'prs': 2, 'issues': 2}
            }
        }
        
        # 模擬獎項數據
        awards_data = {
            'awards': {
                'best_story': {
                    'winner': 'user1',
                    'score': 8.0,
                    'details': {'story_count': 2},
                    'category': 'best_story'
                }
            }
        }
        
        # 執行測試
        announcement = self.announcement_system._generate_comprehensive_announcement(analysis, awards_data)
        
        # 驗證結果
        self.assertIn('Tsext Adventure 月度貢獻報告', announcement)
        self.assertIn('@user1', announcement)
        self.assertIn('最佳劇情獎', announcement)
        self.assertIn('活躍貢獻者: 2 人', announcement)
    
    @patch('requests.post')
    def test_publish_to_discord(self, mock_post):
        """測試發布到 Discord"""
        # 設定環境變數
        os.environ['DISCORD_WEBHOOK_URL'] = 'https://discord.com/api/webhooks/test'
        
        # 模擬成功回應
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status = Mock()
        
        # 執行測試
        result = self.announcement_system._publish_to_discord("測試公告")
        
        # 驗證結果
        self.assertTrue(result)
        mock_post.assert_called_once()
        
        # 清理環境變數
        del os.environ['DISCORD_WEBHOOK_URL']
    
    def test_split_message(self):
        """測試分割長訊息"""
        long_message = "A" * 3000  # 3000 個字符的長訊息
        
        # 執行測試
        chunks = self.announcement_system._split_message(long_message, 1000)
        
        # 驗證結果
        self.assertGreater(len(chunks), 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 1000)


class TestIntegration(unittest.TestCase):
    """整合測試"""
    
    def test_full_workflow(self):
        """測試完整工作流程"""
        # 模擬所有組件
        mock_api = Mock(spec=GitHubAPI)
        
        # 模擬 API 回應
        mock_api.get_pull_requests.return_value = [
            {
                'user': {'login': 'user1'},
                'title': 'Add new story scene',
                'created_at': '2024-10-01T10:00:00Z',
                'merged_at': '2024-10-01T11:00:00Z',
                'labels': [{'name': 'story'}],
                'comments': 2
            }
        ]
        
        mock_api.get_issues.return_value = [
            {
                'user': {'login': 'user2'},
                'title': 'Bug in game logic',
                'created_at': '2024-10-02T10:00:00Z',
                'comments': 5
            }
        ]
        
        # 初始化組件
        analyzer = MonthlyStatsAnalyzer(mock_api, "test_owner", "test_repo")
        award_system = AwardSystem(mock_api, "test_owner", "test_repo")
        announcement_system = AnnouncementSystem(mock_api, "test_owner", "test_repo")
        
        # 執行完整流程
        with patch.object(announcement_system, '_publish_to_discord', return_value=True):
            with patch.object(announcement_system, '_publish_to_github_discussion', return_value=True):
                result = announcement_system.publish_monthly_announcement(30)
        
        # 驗證結果
        self.assertIn('announcement', result)
        self.assertIn('monthly_report', result)
        self.assertIn('award_report', result)
        self.assertIn('publish_results', result)
        
        # 驗證發布結果
        publish_results = result['publish_results']
        self.assertTrue(publish_results['discord'])
        self.assertTrue(publish_results['github_discussion'])


def main():
    """主函數"""
    print("🧪 開始執行階段三整合測試...")
    print("=" * 50)
    
    # 運行測試
    unittest.main(verbosity=2)
    
    print("=" * 50)
    print("✅ 階段三整合測試完成！")


if __name__ == "__main__":
    main()
