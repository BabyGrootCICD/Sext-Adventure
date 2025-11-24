#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community Pulse Reporter - GitHub Action Entry Point
GitHub Action 入口程式

作者: Tsext Adventure Team
授權: MIT License
"""

import os
import sys
import logging
from datetime import datetime

# 添加腳本路徑
sys.path.insert(0, '/action/scripts')

from community_reporter import GitHubClient, ContributionAnalyzer, ReportGenerator

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_env_variable(name: str, default: str = None, required: bool = False) -> str:
    """
    獲取環境變數
    
    Args:
        name: 變數名稱
        default: 預設值
        required: 是否必需
        
    Returns:
        變數值
    """
    value = os.getenv(name, default)
    
    if required and not value:
        logger.error(f"缺少必需的環境變數: {name}")
        sys.exit(1)
    
    return value


def set_output(name: str, value: str):
    """
    設定 GitHub Actions 輸出
    
    Args:
        name: 輸出名稱
        value: 輸出值
    """
    github_output = os.getenv('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a', encoding='utf-8') as f:
            f.write(f"{name}={value}\n")
    else:
        # 回退到舊版語法（適用於舊版 GitHub Actions）
        print(f"::set-output name={name}::{value}")


def write_summary(summary: str):
    """
    寫入 GitHub Actions 摘要
    
    Args:
        summary: 摘要內容
    """
    github_step_summary = os.getenv('GITHUB_STEP_SUMMARY')
    if github_step_summary:
        with open(github_step_summary, 'a', encoding='utf-8') as f:
            f.write(summary)
            f.write('\n')


def parse_interval(interval: str) -> int:
    """
    解析時間間隔
    
    Args:
        interval: 時間間隔字符串
        
    Returns:
        天數
    """
    interval = interval.lower().strip()
    
    # 直接是數字
    if interval.isdigit():
        return int(interval)
    
    # 特殊關鍵字
    if interval in ['last_month', 'lastmonth', 'month']:
        return 30
    elif interval in ['last_week', 'lastweek', 'week']:
        return 7
    elif interval in ['last_year', 'lastyear', 'year']:
        return 365
    
    # 嘗試解析 "30days", "2weeks" 等格式
    if 'day' in interval:
        return int(''.join(filter(str.isdigit, interval)) or '30')
    elif 'week' in interval:
        weeks = int(''.join(filter(str.isdigit, interval)) or '1')
        return weeks * 7
    elif 'month' in interval:
        months = int(''.join(filter(str.isdigit, interval)) or '1')
        return months * 30
    
    # 預設 30 天
    logger.warning(f"無法解析時間間隔 '{interval}'，使用預設值 30 天")
    return 30


def main():
    """主函數"""
    logger.info("🚀 Community Pulse Reporter 開始執行...")
    
    try:
        # 獲取配置
        github_token = get_env_variable('GITHUB_TOKEN', required=True)
        repo_owner = get_env_variable('REPO_OWNER', required=True)
        repo_name = get_env_variable('REPO_NAME', required=True)
        interval_str = get_env_variable('INTERVAL', default='30')
        output_file = get_env_variable('OUTPUT_FILE', default='COMMUNITY_REPORT.md')
        include_stats_str = get_env_variable('INCLUDE_STATS', default='true')
        
        # 解析配置
        interval_days = parse_interval(interval_str)
        include_stats = include_stats_str.lower() in ['true', '1', 'yes']
        
        logger.info(f"📊 倉庫: {repo_owner}/{repo_name}")
        logger.info(f"📅 分析期間: 過去 {interval_days} 天")
        logger.info(f"📄 輸出文件: {output_file}")
        
        # 初始化組件
        logger.info("🔧 初始化 GitHub 客戶端...")
        github_client = GitHubClient(token=github_token)
        
        logger.info("📈 初始化分析器...")
        analyzer = ContributionAnalyzer(github_client, repo_owner, repo_name)
        
        logger.info("📝 初始化報告生成器...")
        reporter = ReportGenerator(repo_owner, repo_name)
        
        # 執行分析
        logger.info("🔍 開始分析貢獻數據...")
        analysis = analyzer.analyze_period(days=interval_days)
        
        # 生成報告
        logger.info("📄 生成報告...")
        report = reporter.generate_report(analysis, include_stats=include_stats)
        
        # 保存報告
        logger.info(f"💾 保存報告到 {output_file}...")
        reporter.save_report(report, output_file)
        
        # 生成摘要
        summary = reporter.generate_summary(analysis)
        write_summary(summary)
        
        # 設定輸出
        stats = analysis['overall_stats']
        set_output('report_file', output_file)
        set_output('total_contributors', str(stats['active_contributors']))
        set_output('total_prs', str(stats['total_prs']))
        set_output('total_issues', str(stats['total_issues']))
        
        # 成功訊息
        logger.info("✅ Community Pulse Reporter 執行完成！")
        logger.info(f"📊 活躍貢獻者: {stats['active_contributors']}")
        logger.info(f"🔀 總 PRs: {stats['total_prs']} (已合併: {stats['merged_prs']})")
        logger.info(f"📝 總 Issues: {stats['total_issues']}")
        logger.info(f"💾 總 Commits: {stats['total_commits']}")
        
        # 顯示前三名貢獻者
        top_3 = analysis['leaderboard'][:3]
        if top_3:
            logger.info("🏆 Top 3 貢獻者:")
            medals = {0: '🥇', 1: '🥈', 2: '🥉'}
            for i, contributor in enumerate(top_3):
                logger.info(f"  {medals[i]} @{contributor['username']} - {contributor['total_score']} 分")
        
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"❌ 執行過程中發生錯誤: {e}", exc_info=True)
        
        # 寫入錯誤摘要
        error_summary = f"""## ❌ Community Pulse Reporter 執行失敗

**錯誤訊息**: {str(e)}

請檢查：
1. GitHub Token 是否有效
2. 倉庫名稱是否正確
3. API 請求是否超過限制

詳細錯誤請查看 Action 日誌。
"""
        write_summary(error_summary)
        
        sys.exit(1)


if __name__ == '__main__':
    main()

