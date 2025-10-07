#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tsext Adventure Discord Bot
用於管理貢獻者角色和自動化通知

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import discord
from discord.ext import commands, tasks
import requests

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContributorRoleManager:
    """貢獻者角色管理器"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.role_config = {
            'maintainer': {
                'name': '👑 專案維護者',
                'color': discord.Color.gold(),
                'permissions': ['manage_messages', 'manage_channels', 'kick_members']
            },
            'core': {
                'name': '🥇 核心貢獻者',
                'color': discord.Color.blue(),
                'permissions': ['manage_messages']
            },
            'active': {
                'name': '🥈 活躍貢獻者',
                'color': discord.Color.green(),
                'permissions': []
            },
            'novice': {
                'name': '🥉 新手貢獻者',
                'color': discord.Color.orange(),
                'permissions': []
            }
        }
    
    async def create_roles(self, guild: discord.Guild):
        """創建貢獻者角色"""
        for role_id, config in self.role_config.items():
            # 檢查角色是否已存在
            existing_role = discord.utils.get(guild.roles, name=config['name'])
            if existing_role:
                logger.info(f"角色 {config['name']} 已存在")
                continue
            
            try:
                # 創建角色
                permissions = discord.Permissions()
                for perm in config['permissions']:
                    setattr(permissions, perm, True)
                
                role = await guild.create_role(
                    name=config['name'],
                    color=config['color'],
                    permissions=permissions,
                    mentionable=True,
                    reason="Tsext Adventure 貢獻者角色系統"
                )
                logger.info(f"成功創建角色: {role.name}")
                
            except discord.Forbidden:
                logger.error(f"沒有權限創建角色: {config['name']}")
            except Exception as e:
                logger.error(f"創建角色時發生錯誤: {e}")
    
    async def assign_role(self, guild: discord.Guild, user: discord.Member, contributor_level: str):
        """分配貢獻者角色"""
        if contributor_level not in self.role_config:
            logger.error(f"未知的貢獻者等級: {contributor_level}")
            return False
        
        role_name = self.role_config[contributor_level]['name']
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            logger.error(f"找不到角色: {role_name}")
            return False
        
        try:
            # 移除舊的貢獻者角色
            await self.remove_contributor_roles(user)
            
            # 分配新角色
            await user.add_roles(role, reason=f"更新貢獻者等級為 {contributor_level}")
            logger.info(f"成功為 {user.display_name} 分配角色: {role.name}")
            return True
            
        except discord.Forbidden:
            logger.error(f"沒有權限為 {user.display_name} 分配角色")
            return False
        except Exception as e:
            logger.error(f"分配角色時發生錯誤: {e}")
            return False
    
    async def remove_contributor_roles(self, user: discord.Member):
        """移除所有貢獻者角色"""
        for role_config in self.role_config.values():
            role = discord.utils.get(user.roles, name=role_config['name'])
            if role:
                try:
                    await user.remove_roles(role, reason="更新貢獻者等級")
                    logger.info(f"移除 {user.display_name} 的角色: {role.name}")
                except Exception as e:
                    logger.error(f"移除角色時發生錯誤: {e}")


class GitHubIntegration:
    """GitHub 整合類別"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.token}' if self.token else None,
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Tsext-Adventure-Discord-Bot'
        }
        self.headers = {k: v for k, v in self.headers.items() if v is not None}
    
    async def get_contributor_level(self, username: str) -> Optional[str]:
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
            return None
    
    async def _get_user_prs(self, username: str) -> List[Dict]:
        """獲取用戶的 PR 列表"""
        url = f"{self.base_url}/search/issues"
        params = {
            'q': f'author:{username} repo:BabyGrootCICD/Sext-Adventure type:pr',
            'per_page': 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except Exception as e:
            logger.error(f"獲取 PR 數據時發生錯誤: {e}")
            return []
    
    async def _get_user_issues(self, username: str) -> List[Dict]:
        """獲取用戶的 Issue 列表"""
        url = f"{self.base_url}/search/issues"
        params = {
            'q': f'author:{username} repo:BabyGrootCICD/Sext-Adventure type:issue',
            'per_page': 100
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [])
        except Exception as e:
            logger.error(f"獲取 Issue 數據時發生錯誤: {e}")
            return []


class TsextAdventureBot(commands.Bot):
    """Tsext Adventure Discord Bot"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        self.role_manager = ContributorRoleManager(self)
        self.github = GitHubIntegration()
        self.user_mapping = {}  # Discord ID -> GitHub username 映射
    
    async def on_ready(self):
        """Bot 準備就緒時觸發"""
        logger.info(f'{self.user} 已上線！')
        logger.info(f'已連接到 {len(self.guilds)} 個伺服器')
        
        # 創建貢獻者角色
        for guild in self.guilds:
            await self.role_manager.create_roles(guild)
        
        # 啟動定期更新任務
        self.update_contributor_roles.start()
    
    async def on_member_join(self, member: discord.Member):
        """新成員加入時觸發"""
        welcome_channel = discord.utils.get(member.guild.channels, name='welcome')
        if welcome_channel:
            embed = discord.Embed(
                title="🎉 歡迎加入 Tsext Adventure 社區！",
                description=f"歡迎 {member.mention}！\n\n"
                           "我們是一個開源的萬聖節文字冒險遊戲專案。\n"
                           "你可以：\n"
                           "• 貢獻故事內容\n"
                           "• 報告 Bug\n"
                           "• 提出新功能建議\n"
                           "• 參與討論\n\n"
                           "使用 `!help` 查看可用命令！",
                color=discord.Color.orange()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.set_footer(text="Tsext Adventure Community")
            
            await welcome_channel.send(embed=embed)
    
    @commands.command(name='link')
    async def link_github(self, ctx, github_username: str):
        """連結 GitHub 帳號"""
        if ctx.author.id in self.user_mapping:
            await ctx.send("❌ 你已經連結了 GitHub 帳號！")
            return
        
        # 驗證 GitHub 用戶是否存在
        contributor_level = await self.github.get_contributor_level(github_username)
        if contributor_level is None:
            await ctx.send("❌ 找不到該 GitHub 用戶或無法獲取貢獻數據！")
            return
        
        # 儲存映射
        self.user_mapping[ctx.author.id] = github_username
        
        # 分配角色
        success = await self.role_manager.assign_role(ctx.guild, ctx.author, contributor_level)
        
        if success:
            embed = discord.Embed(
                title="✅ GitHub 帳號連結成功！",
                description=f"已連結 GitHub 帳號: `{github_username}`\n"
                           f"貢獻者等級: **{contributor_level}**\n"
                           f"已分配角色: {self.role_manager.role_config[contributor_level]['name']}",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ 分配角色時發生錯誤，請聯繫管理員！")
    
    @commands.command(name='update')
    async def update_role(self, ctx):
        """更新貢獻者角色"""
        if ctx.author.id not in self.user_mapping:
            await ctx.send("❌ 請先使用 `!link <github_username>` 連結你的 GitHub 帳號！")
            return
        
        github_username = self.user_mapping[ctx.author.id]
        contributor_level = await self.github.get_contributor_level(github_username)
        
        if contributor_level is None:
            await ctx.send("❌ 無法獲取你的貢獻數據！")
            return
        
        success = await self.role_manager.assign_role(ctx.guild, ctx.author, contributor_level)
        
        if success:
            embed = discord.Embed(
                title="🔄 角色更新成功！",
                description=f"GitHub 帳號: `{github_username}`\n"
                           f"新的貢獻者等級: **{contributor_level}**\n"
                           f"角色: {self.role_manager.role_config[contributor_level]['name']}",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ 更新角色時發生錯誤！")
    
    @commands.command(name='stats')
    async def show_stats(self, ctx):
        """顯示貢獻統計"""
        if ctx.author.id not in self.user_mapping:
            await ctx.send("❌ 請先連結你的 GitHub 帳號！")
            return
        
        github_username = self.user_mapping[ctx.author.id]
        
        # 獲取詳細統計
        prs = await self.github._get_user_prs(github_username)
        issues = await self.github._get_user_issues(github_username)
        contributor_level = await self.github.get_contributor_level(github_username)
        
        embed = discord.Embed(
            title=f"📊 {github_username} 的貢獻統計",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="📈 總體數據",
            value=f"**Pull Requests**: {len(prs)}\n"
                  f"**Issues**: {len(issues)}\n"
                  f"**總貢獻分數**: {len(prs) * 3 + len(issues)}",
            inline=True
        )
        
        embed.add_field(
            name="🏆 貢獻者等級",
            value=f"**等級**: {contributor_level}\n"
                  f"**角色**: {self.role_manager.role_config[contributor_level]['name']}",
            inline=True
        )
        
        embed.add_field(
            name="📅 最近活動",
            value=f"**最後更新**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            inline=True
        )
        
        embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.set_footer(text="Tsext Adventure Community")
        
        await ctx.send(embed=embed)
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        """顯示幫助資訊"""
        embed = discord.Embed(
            title="🤖 Tsext Adventure Bot 命令",
            description="以下是可用的命令：",
            color=discord.Color.blue()
        )
        
        commands_info = [
            ("!link <github_username>", "連結你的 GitHub 帳號"),
            ("!update", "更新你的貢獻者角色"),
            ("!stats", "查看你的貢獻統計"),
            ("!help", "顯示此幫助資訊")
        ]
        
        for cmd, desc in commands_info:
            embed.add_field(name=cmd, value=desc, inline=False)
        
        embed.add_field(
            name="📚 更多資訊",
            value="• [GitHub 專案](https://github.com/BabyGrootCICD/Sext-Adventure)\n"
                  "• [貢獻指南](https://github.com/BabyGrootCICD/Sext-Adventure/blob/main/CONTRIBUTING.md)\n"
                  "• [線上遊戲](https://babygrootcicd.github.io/Sext-Adventure/)",
            inline=False
        )
        
        embed.set_footer(text="Tsext Adventure Community")
        await ctx.send(embed=embed)
    
    @tasks.loop(hours=24)
    async def update_contributor_roles(self):
        """定期更新所有貢獻者角色"""
        logger.info("開始定期更新貢獻者角色...")
        
        for guild in self.guilds:
            for user_id, github_username in self.user_mapping.items():
                try:
                    member = guild.get_member(user_id)
                    if not member:
                        continue
                    
                    contributor_level = await self.github.get_contributor_level(github_username)
                    if contributor_level:
                        await self.role_manager.assign_role(guild, member, contributor_level)
                        logger.info(f"更新 {member.display_name} 的角色為 {contributor_level}")
                    
                except Exception as e:
                    logger.error(f"更新 {github_username} 角色時發生錯誤: {e}")
        
        logger.info("定期更新完成")


def main():
    """主函數"""
    # 從環境變數獲取 Discord Bot Token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        logger.error("請設定 DISCORD_BOT_TOKEN 環境變數！")
        return
    
    # 創建並運行 Bot
    bot = TsextAdventureBot()
    bot.run(token)


if __name__ == "__main__":
    main()
