#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公告機制
用於自動發布月度報告和獎項公告

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import sys

# 添加 scripts 目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from monthly_stats import MonthlyStatsAnalyzer
from award_system import AwardSystem
from github_api import GitHubAPI

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnnouncementSystem:
    """公告系統"""
    
    def __init__(self, github_api: GitHubAPI, owner: str, repo: str):
        self.github_api = github_api
        self.owner = owner
        self.repo = repo
        self.analyzer = MonthlyStatsAnalyzer(github_api, owner, repo)
        self.award_system = AwardSystem(github_api, owner, repo)
        
        # 公告配置
        self.announcement_config = {
            'discord_webhook_url': os.getenv('DISCORD_WEBHOOK_URL'),
            'github_discussion_category': 'Announcements',
            'enable_discord': True,
            'enable_github_discussion': True,
            'enable_github_issue': False
        }
    
    def publish_monthly_announcement(self, days: int = 30) -> Dict:
        """發布月度公告"""
        logger.info("開始生成和發布月度公告...")
        
        # 生成月度統計
        analysis = self.analyzer.analyze_monthly_contributions(days)
        monthly_report = self.analyzer.generate_monthly_report(analysis)
        
        # 生成獎項評選
        awards_data = self.award_system.evaluate_monthly_awards(days)
        award_report = awards_data['report']
        
        # 生成綜合公告
        announcement = self._generate_comprehensive_announcement(analysis, awards_data)
        
        # 發布到各個平台
        results = {
            'discord': False,
            'github_discussion': False,
            'github_issue': False
        }
        
        if self.announcement_config['enable_discord']:
            results['discord'] = self._publish_to_discord(announcement)
        
        if self.announcement_config['enable_github_discussion']:
            results['github_discussion'] = self._publish_to_github_discussion(announcement)
        
        if self.announcement_config['enable_github_issue']:
            results['github_issue'] = self._publish_to_github_issue(announcement)
        
        return {
            'announcement': announcement,
            'monthly_report': monthly_report,
            'award_report': award_report,
            'publish_results': results,
            'analysis': analysis,
            'awards': awards_data
        }
    
    def _generate_comprehensive_announcement(self, analysis: Dict, awards_data: Dict) -> str:
        """生成綜合公告"""
        period = analysis['period']
        overall = analysis['overall_stats']
        awards = awards_data['awards']
        
        # 獲取獲獎者列表
        winners = []
        for award_id, award_data in awards.items():
            award_config = self.award_system.award_categories[award_id]
            winners.append(f"🏆 **{award_config['name']}**: @{award_data['winner']}")
        
        announcement = f"""# 🎉 Tsext Adventure 月度貢獻報告 - {period['end_date'][:7]}

## 📊 本月亮點

我們很高興地宣布，在過去 {period['days']} 天中，Tsext Adventure 專案取得了令人矚目的進展！

### 🚀 核心數據
- **活躍貢獻者**: {overall['active_contributors']} 人
- **Pull Requests**: {overall['total_prs']} 個 (合併率: {overall['pr_merge_rate']:.1f}%)
- **Issues**: {overall['total_issues']} 個
- **平均每人貢獻**: {overall['avg_prs_per_contributor']:.1f} 個 PR

## 🏆 月度獲獎者

恭喜以下獲獎者！你們的貢獻讓 Tsext Adventure 變得更加精彩：

{chr(10).join(winners)}

## 🌟 特別感謝

感謝所有在本月為專案做出貢獻的開發者們！每一位貢獻者都是 Tsext Adventure 社區的重要一員。

### 所有貢獻者
"""
        
        # 添加所有貢獻者
        contributors = analysis['contributor_stats']
        sorted_contributors = sorted(
            contributors.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        for i, (author, stats) in enumerate(sorted_contributors, 1):
            announcement += f"{i}. **@{author}** - {stats['total_score']:.1f} 分 "
            announcement += f"({stats['prs']} PRs, {stats['issues']} Issues)\n"
        
        announcement += f"""
## 🎯 下月展望

讓我們繼續攜手前進，為 Tsext Adventure 創造更多精彩內容：

- 🎭 **故事內容**: 更多創意劇情和場景
- 🛠️ **技術改進**: 持續優化遊戲體驗
- 🐛 **問題修復**: 積極解決用戶反饋
- 🎨 **UI/UX**: 提升界面設計和用戶體驗
- 🌟 **社區建設**: 加強開發者之間的協作

## 📚 相關連結

- [📊 完整月度報告](https://github.com/{self.owner}/{self.repo}/blob/main/monthly_report_{period['end_date'][:7].replace('-', '_')}.md)
- [🏆 詳細獎項報告](https://github.com/{self.owner}/{self.repo}/blob/main/monthly_awards_{period['end_date'][:7].replace('-', '_')}.md)
- [🎮 線上遊戲](https://babygrootcicd.github.io/Sext-Adventure/)
- [📖 貢獻指南](https://github.com/{self.owner}/{self.repo}/blob/main/CONTRIBUTING.md)

---

*公告發布時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*  
*Tsext Adventure 自動公告系統*

#TsextAdventure #開源 #遊戲開發 #社區貢獻
"""
        
        return announcement
    
    def _publish_to_discord(self, announcement: str) -> bool:
        """發布到 Discord"""
        if not self.announcement_config['discord_webhook_url']:
            logger.warning("未設定 Discord Webhook URL")
            return False
        
        try:
            # 分割長訊息
            if len(announcement) > 2000:
                chunks = self._split_message(announcement, 2000)
                for chunk in chunks:
                    payload = {"content": chunk}
                    response = requests.post(
                        self.announcement_config['discord_webhook_url'],
                        json=payload
                    )
                    response.raise_for_status()
            else:
                payload = {"content": announcement}
                response = requests.post(
                    self.announcement_config['discord_webhook_url'],
                    json=payload
                )
                response.raise_for_status()
            
            logger.info("成功發布到 Discord")
            return True
            
        except Exception as e:
            logger.error(f"發布到 Discord 時發生錯誤: {e}")
            return False
    
    def _publish_to_github_discussion(self, announcement: str) -> bool:
        """發布到 GitHub Discussion"""
        try:
            # 創建 Discussion
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/discussions"
            
            payload = {
                "title": f"🎉 Tsext Adventure 月度貢獻報告 - {datetime.now().strftime('%Y年%m月')}",
                "body": announcement,
                "category": self.announcement_config['github_discussion_category']
            }
            
            headers = {
                'Authorization': f'token {self.github_api.token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Tsext-Adventure-Announcement-System'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            logger.info("成功發布到 GitHub Discussion")
            return True
            
        except Exception as e:
            logger.error(f"發布到 GitHub Discussion 時發生錯誤: {e}")
            return False
    
    def _publish_to_github_issue(self, announcement: str) -> bool:
        """發布到 GitHub Issue"""
        try:
            # 創建 Issue
            url = f"https://api.github.com/repos/{self.owner}/{self.repo}/issues"
            
            payload = {
                "title": f"🎉 Tsext Adventure 月度貢獻報告 - {datetime.now().strftime('%Y年%m月')}",
                "body": announcement,
                "labels": ["announcement", "monthly-report"]
            }
            
            headers = {
                'Authorization': f'token {self.github_api.token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Tsext-Adventure-Announcement-System'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            logger.info("成功發布到 GitHub Issue")
            return True
            
        except Exception as e:
            logger.error(f"發布到 GitHub Issue 時發生錯誤: {e}")
            return False
    
    def _split_message(self, message: str, max_length: int) -> List[str]:
        """分割長訊息"""
        chunks = []
        current_chunk = ""
        
        lines = message.split('\n')
        
        for line in lines:
            if len(current_chunk + line + '\n') <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def send_achievement_notification(self, username: str, achievement: str, 
                                    description: str) -> bool:
        """發送成就通知"""
        if not self.announcement_config['discord_webhook_url']:
            return False
        
        notification = f"""🎉 **成就解鎖通知**

**用戶**: @{username}
**成就**: {achievement}
**描述**: {description}

恭喜獲得新成就！繼續保持優秀的表現！ 🏆

*Tsext Adventure 成就系統*
"""
        
        try:
            payload = {"content": notification}
            response = requests.post(
                self.announcement_config['discord_webhook_url'],
                json=payload
            )
            response.raise_for_status()
            
            logger.info(f"成功發送成就通知給 {username}")
            return True
            
        except Exception as e:
            logger.error(f"發送成就通知時發生錯誤: {e}")
            return False
    
    def send_contribution_notification(self, username: str, contribution_type: str, 
                                     title: str, url: str) -> bool:
        """發送貢獻通知"""
        if not self.announcement_config['discord_webhook_url']:
            return False
        
        emoji_map = {
            'pr': '🔀',
            'issue': '📝',
            'story': '🎭',
            'bug': '🐛',
            'feature': '✨'
        }
        
        emoji = emoji_map.get(contribution_type, '📝')
        
        notification = f"""{emoji} **新貢獻通知**

**貢獻者**: @{username}
**類型**: {contribution_type.upper()}
**標題**: {title}
**連結**: {url}

感謝你的貢獻！社區因你而更精彩！ 🌟

*Tsext Adventure 貢獻追蹤系統*
"""
        
        try:
            payload = {"content": notification}
            response = requests.post(
                self.announcement_config['discord_webhook_url'],
                json=payload
            )
            response.raise_for_status()
            
            logger.info(f"成功發送貢獻通知給 {username}")
            return True
            
        except Exception as e:
            logger.error(f"發送貢獻通知時發生錯誤: {e}")
            return False
    
    def save_announcement(self, announcement_data: Dict, filename: Optional[str] = None) -> str:
        """保存公告數據"""
        if not filename:
            timestamp = datetime.now().strftime('%Y_%m_%d')
            filename = f"announcement_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(announcement_data, f, ensure_ascii=False, indent=2, default=str)
        
        logger.info(f"公告數據已保存到: {filename}")
        return filename


def main():
    """主函數"""
    # 設定倉庫資訊
    OWNER = "BabyGrootCICD"
    REPO = "Sext-Adventure"
    
    try:
        # 初始化公告系統
        github_api = GitHubAPI()
        announcement_system = AnnouncementSystem(github_api, OWNER, REPO)
        
        # 發布月度公告
        logger.info("開始發布月度公告...")
        announcement_data = announcement_system.publish_monthly_announcement(30)
        
        # 保存結果
        announcement_file = announcement_system.save_announcement(announcement_data)
        
        # 輸出摘要
        results = announcement_data['publish_results']
        print(f"\n📢 月度公告發布完成!")
        print(f"📊 月度統計: 已生成")
        print(f"🏆 獎項評選: 已生成")
        print(f"📢 Discord: {'✅' if results['discord'] else '❌'}")
        print(f"💬 GitHub Discussion: {'✅' if results['github_discussion'] else '❌'}")
        print(f"📝 GitHub Issue: {'✅' if results['github_issue'] else '❌'}")
        print(f"📋 公告數據: {announcement_file}")
        
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")
        raise


if __name__ == "__main__":
    main()
