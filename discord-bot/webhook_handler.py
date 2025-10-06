#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Webhook 處理器
用於接收 GitHub 事件並自動更新 Discord 角色

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import hmac
import hashlib
import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional
from flask import Flask, request, jsonify
import requests

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

class GitHubWebhookHandler:
    """GitHub Webhook 處理器"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        self.webhook_secret = os.getenv('GITHUB_WEBHOOK_SECRET')
        
        # GitHub API 設定
        self.github_api_url = 'https://api.github.com'
        self.github_headers = {
            'Authorization': f'token {self.github_token}' if self.github_token else None,
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Tsext-Adventure-Webhook-Handler'
        }
        self.github_headers = {k: v for k, v in self.github_headers.items() if v is not None}
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """驗證 Webhook 簽名"""
        if not self.webhook_secret:
            logger.warning("未設定 Webhook 密鑰，跳過簽名驗證")
            return True
        
        expected_signature = 'sha256=' + hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    async def handle_pull_request_event(self, payload: Dict):
        """處理 Pull Request 事件"""
        action = payload.get('action')
        pr = payload.get('pull_request', {})
        
        if action not in ['opened', 'closed', 'merged']:
            return
        
        author = pr.get('user', {}).get('login')
        if not author:
            return
        
        # 獲取貢獻者等級
        contributor_level = await self.get_contributor_level(author)
        
        # 發送 Discord 通知
        await self.send_discord_notification(action, pr, contributor_level)
        
        # 如果是合併的 PR，更新貢獻者等級
        if action == 'closed' and pr.get('merged'):
            await self.update_contributor_level(author, contributor_level)
    
    async def handle_issue_event(self, payload: Dict):
        """處理 Issue 事件"""
        action = payload.get('action')
        issue = payload.get('issue', {})
        
        if action not in ['opened', 'closed']:
            return
        
        author = issue.get('user', {}).get('login')
        if not author:
            return
        
        # 獲取貢獻者等級
        contributor_level = await self.get_contributor_level(author)
        
        # 發送 Discord 通知
        await self.send_discord_notification(action, issue, contributor_level, is_issue=True)
    
    async def get_contributor_level(self, username: str) -> str:
        """獲取貢獻者等級"""
        try:
            # 獲取用戶的 PR 和 Issue 數據
            prs = await self._get_user_prs(username)
            issues = await self._get_user_issues(username)
            
            # 計算貢獻分數
            total_score = len(prs) * 3 + len(issues)
            
            # 根據分數分類
            if total_score >= 50 or len(prs) >= 15:
                return 'maintainer'
            elif total_score >= 20 or len(prs) >= 8:
                return 'core'
            elif total_score >= 5 or len(prs) >= 2:
                return 'active'
            else:
                return 'novice'
                
        except Exception as e:
            logger.error(f"獲取貢獻者等級時發生錯誤: {e}")
            return 'novice'
    
    async def _get_user_prs(self, username: str) -> list:
        """獲取用戶的 PR 列表"""
        url = f"{self.github_api_url}/search/issues"
        params = {
            'q': f'author:{username} repo:BabyGrootCICD/Sext-Adventure type:pr',
            'per_page': 100
        }
        
        try:
            response = requests.get(url, headers=self.github_headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except Exception as e:
            logger.error(f"獲取 PR 數據時發生錯誤: {e}")
            return []
    
    async def _get_user_issues(self, username: str) -> list:
        """獲取用戶的 Issue 列表"""
        url = f"{self.github_api_url}/search/issues"
        params = {
            'q': f'author:{username} repo:BabyGrootCICD/Sext-Adventure type:issue',
            'per_page': 100
        }
        
        try:
            response = requests.get(url, headers=self.github_headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except Exception as e:
            logger.error(f"獲取 Issue 數據時發生錯誤: {e}")
            return []
    
    async def send_discord_notification(self, action: str, item: Dict, contributor_level: str, is_issue: bool = False):
        """發送 Discord 通知"""
        if not self.discord_webhook_url:
            logger.warning("未設定 Discord Webhook URL")
            return
        
        item_type = "Issue" if is_issue else "Pull Request"
        author = item.get('user', {}).get('login')
        title = item.get('title', '')
        url = item.get('html_url', '')
        
        # 設定顏色和表情符號
        color_map = {
            'opened': 0x00ff00,  # 綠色
            'closed': 0xff0000,  # 紅色
            'merged': 0x0099ff   # 藍色
        }
        
        emoji_map = {
            'opened': '🆕',
            'closed': '❌',
            'merged': '✅'
        }
        
        # 創建 Discord Embed
        embed = {
            "title": f"{emoji_map.get(action, '📝')} {item_type} {action.title()}",
            "description": f"**{title}**\n\n作者: {author}\n等級: {contributor_level}",
            "url": url,
            "color": color_map.get(action, 0x666666),
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "Tsext Adventure Community"
            }
        }
        
        # 發送到 Discord
        payload = {
            "embeds": [embed]
        }
        
        try:
            response = requests.post(self.discord_webhook_url, json=payload)
            response.raise_for_status()
            logger.info(f"成功發送 Discord 通知: {action} {item_type}")
        except Exception as e:
            logger.error(f"發送 Discord 通知時發生錯誤: {e}")
    
    async def update_contributor_level(self, username: str, level: str):
        """更新貢獻者等級（這裡可以整合 Discord Bot API）"""
        logger.info(f"更新貢獻者 {username} 的等級為 {level}")
        # 這裡可以調用 Discord Bot API 來更新角色
        # 或者發送訊息到 Discord 頻道通知管理員手動更新


# 全域處理器實例
webhook_handler = GitHubWebhookHandler()


@app.route('/webhook', methods=['POST'])
async def github_webhook():
    """GitHub Webhook 端點"""
    try:
        # 獲取請求數據
        payload = request.get_data()
        signature = request.headers.get('X-Hub-Signature-256', '')
        
        # 驗證簽名
        if not webhook_handler.verify_signature(payload, signature):
            logger.error("Webhook 簽名驗證失敗")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # 解析 JSON
        data = json.loads(payload.decode('utf-8'))
        event_type = request.headers.get('X-GitHub-Event')
        
        logger.info(f"收到 GitHub 事件: {event_type}")
        
        # 處理不同類型的事件
        if event_type == 'pull_request':
            await webhook_handler.handle_pull_request_event(data)
        elif event_type == 'issues':
            await webhook_handler.handle_issue_event(data)
        else:
            logger.info(f"忽略事件類型: {event_type}")
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"處理 Webhook 時發生錯誤: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Tsext Adventure Webhook Handler'
    })


@app.route('/test', methods=['POST'])
def test_webhook():
    """測試 Webhook 端點"""
    try:
        data = request.get_json()
        
        # 模擬 GitHub 事件
        test_payload = {
            'action': 'opened',
            'pull_request': {
                'title': '測試 PR',
                'user': {'login': 'test_user'},
                'html_url': 'https://github.com/test/repo/pull/1'
            }
        }
        
        # 處理測試事件
        asyncio.create_task(webhook_handler.handle_pull_request_event(test_payload))
        
        return jsonify({'status': 'test event processed'}), 200
        
    except Exception as e:
        logger.error(f"測試 Webhook 時發生錯誤: {e}")
        return jsonify({'error': 'Test failed'}), 500


if __name__ == '__main__':
    # 設定環境變數
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"啟動 Webhook 處理器，端口: {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
