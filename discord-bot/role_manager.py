#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord 角色管理腳本
用於批量管理貢獻者角色和權限

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import json
import asyncio
import logging
from typing import Dict, List, Optional
import discord
from discord.ext import commands

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RoleManager:
    """角色管理器"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.role_config = self.load_role_config()
    
    def load_role_config(self) -> Dict:
        """載入角色配置"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"找不到配置檔案: {config_path}")
            return {}
    
    async def sync_roles(self, guild: discord.Guild):
        """同步角色到伺服器"""
        logger.info(f"開始同步角色到伺服器: {guild.name}")
        
        for role_id, config in self.role_config.get('roles', {}).items():
            await self.create_or_update_role(guild, role_id, config)
        
        logger.info("角色同步完成")
    
    async def create_or_update_role(self, guild: discord.Guild, role_id: str, config: Dict):
        """創建或更新角色"""
        role_name = config['name']
        existing_role = discord.utils.get(guild.roles, name=role_name)
        
        if existing_role:
            logger.info(f"角色 {role_name} 已存在，跳過創建")
            return existing_role
        
        try:
            # 設定權限
            permissions = discord.Permissions()
            for perm in config.get('permissions', []):
                setattr(permissions, perm, True)
            
            # 設定顏色
            color_map = {
                'gold': discord.Color.gold(),
                'blue': discord.Color.blue(),
                'green': discord.Color.green(),
                'orange': discord.Color.orange()
            }
            color = color_map.get(config.get('color', 'blue'), discord.Color.blue())
            
            # 創建角色
            role = await guild.create_role(
                name=role_name,
                color=color,
                permissions=permissions,
                mentionable=True,
                reason=f"Tsext Adventure 貢獻者角色: {role_id}"
            )
            
            logger.info(f"成功創建角色: {role.name}")
            return role
            
        except discord.Forbidden:
            logger.error(f"沒有權限創建角色: {role_name}")
        except Exception as e:
            logger.error(f"創建角色時發生錯誤: {e}")
        
        return None
    
    async def assign_role_to_user(self, guild: discord.Guild, user: discord.Member, role_id: str):
        """為用戶分配角色"""
        if role_id not in self.role_config.get('roles', {}):
            logger.error(f"未知的角色 ID: {role_id}")
            return False
        
        role_name = self.role_config['roles'][role_id]['name']
        role = discord.utils.get(guild.roles, name=role_name)
        
        if not role:
            logger.error(f"找不到角色: {role_name}")
            return False
        
        try:
            # 移除其他貢獻者角色
            await self.remove_contributor_roles(user)
            
            # 分配新角色
            await user.add_roles(role, reason=f"分配貢獻者角色: {role_id}")
            logger.info(f"成功為 {user.display_name} 分配角色: {role.name}")
            return True
            
        except discord.Forbidden:
            logger.error(f"沒有權限為 {user.display_name} 分配角色")
        except Exception as e:
            logger.error(f"分配角色時發生錯誤: {e}")
        
        return False
    
    async def remove_contributor_roles(self, user: discord.Member):
        """移除所有貢獻者角色"""
        for role_config in self.role_config.get('roles', {}).values():
            role = discord.utils.get(user.roles, name=role_config['name'])
            if role:
                try:
                    await user.remove_roles(role, reason="移除貢獻者角色")
                    logger.info(f"移除 {user.display_name} 的角色: {role.name}")
                except Exception as e:
                    logger.error(f"移除角色時發生錯誤: {e}")
    
    async def get_user_role_level(self, user: discord.Member) -> Optional[str]:
        """獲取用戶的貢獻者等級"""
        for role_id, role_config in self.role_config.get('roles', {}).items():
            role = discord.utils.get(user.roles, name=role_config['name'])
            if role:
                return role_id
        return None
    
    async def list_contributors(self, guild: discord.Guild) -> Dict[str, List[discord.Member]]:
        """列出所有貢獻者"""
        contributors = {
            'maintainer': [],
            'core': [],
            'active': [],
            'novice': []
        }
        
        for member in guild.members:
            role_level = await self.get_user_role_level(member)
            if role_level:
                contributors[role_level].append(member)
        
        return contributors
    
    async def generate_contributor_report(self, guild: discord.Guild) -> str:
        """生成貢獻者報告"""
        contributors = await self.list_contributors(guild)
        
        report = f"# 📊 {guild.name} 貢獻者報告\n\n"
        
        for role_id, members in contributors.items():
            if members:
                role_config = self.role_config['roles'][role_id]
                report += f"## {role_config['name']}\n"
                report += f"*{role_config['description']}*\n\n"
                
                for member in members:
                    report += f"- {member.mention} ({member.display_name})\n"
                
                report += "\n"
        
        total_contributors = sum(len(members) for members in contributors.values())
        report += f"**總貢獻者**: {total_contributors} 人\n"
        
        return report


class PermissionManager:
    """權限管理器"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def update_channel_permissions(self, guild: discord.Guild):
        """更新頻道權限"""
        logger.info(f"開始更新 {guild.name} 的頻道權限")
        
        # 獲取貢獻者角色
        role_config = {
            'maintainer': {'permissions': ['manage_messages', 'manage_channels', 'kick_members']},
            'core': {'permissions': ['manage_messages']},
            'active': {'permissions': []},
            'novice': {'permissions': []}
        }
        
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                await self.update_channel_permission_overwrites(channel, role_config)
        
        logger.info("頻道權限更新完成")
    
    async def update_channel_permission_overwrites(self, channel: discord.TextChannel, role_config: Dict):
        """更新頻道的權限覆蓋"""
        try:
            for role_id, config in role_config.items():
                role = discord.utils.get(channel.guild.roles, name=config['name'])
                if not role:
                    continue
                
                # 設定權限覆蓋
                overwrite = discord.PermissionOverwrite()
                
                # 基本權限
                overwrite.read_messages = True
                overwrite.send_messages = True
                overwrite.read_message_history = True
                
                # 特殊權限
                for perm in config.get('permissions', []):
                    setattr(overwrite, perm, True)
                
                await channel.set_permissions(role, overwrite=overwrite)
                logger.info(f"更新頻道 {channel.name} 的角色 {role.name} 權限")
                
        except Exception as e:
            logger.error(f"更新頻道權限時發生錯誤: {e}")


class NotificationManager:
    """通知管理器"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    async def send_welcome_message(self, guild: discord.Guild, member: discord.Member):
        """發送歡迎訊息"""
        welcome_channel = discord.utils.get(guild.channels, name='welcome')
        if not welcome_channel:
            welcome_channel = guild.system_channel
        
        if not welcome_channel:
            return
        
        embed = discord.Embed(
            title="🎉 歡迎加入 Tsext Adventure 社區！",
            description=f"歡迎 {member.mention}！\n\n"
                       "我們是一個開源的萬聖節文字冒險遊戲專案。\n"
                       "你可以：\n"
                       "• 貢獻故事內容\n"
                       "• 報告 Bug\n"
                       "• 提出新功能建議\n"
                       "• 參與討論\n\n"
                       "使用 `!link <github_username>` 連結你的 GitHub 帳號來獲得貢獻者角色！",
            color=discord.Color.orange()
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Tsext Adventure Community")
        
        await welcome_channel.send(embed=embed)
    
    async def send_role_update_notification(self, guild: discord.Guild, member: discord.Member, old_role: str, new_role: str):
        """發送角色更新通知"""
        update_channel = discord.utils.get(guild.channels, name='contributor-updates')
        if not update_channel:
            update_channel = guild.system_channel
        
        if not update_channel:
            return
        
        embed = discord.Embed(
            title="🔄 貢獻者角色更新",
            description=f"{member.mention} 的貢獻者等級已更新！\n\n"
                       f"**舊等級**: {old_role}\n"
                       f"**新等級**: {new_role}\n\n"
                       "感謝你的持續貢獻！🎉",
            color=discord.Color.green()
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Tsext Adventure Community")
        
        await update_channel.send(embed=embed)
    
    async def send_monthly_report(self, guild: discord.Guild, report: str):
        """發送月度報告"""
        announcement_channel = discord.utils.get(guild.channels, name='announcements')
        if not announcement_channel:
            announcement_channel = guild.system_channel
        
        if not announcement_channel:
            return
        
        # 分割長訊息
        if len(report) > 2000:
            chunks = [report[i:i+2000] for i in range(0, len(report), 2000)]
            for chunk in chunks:
                await announcement_channel.send(chunk)
        else:
            await announcement_channel.send(report)


def main():
    """主函數 - 用於測試"""
    print("Discord 角色管理腳本")
    print("此腳本需要與 Discord Bot 一起使用")
    print("請參考 bot.py 中的使用範例")


if __name__ == "__main__":
    main()
