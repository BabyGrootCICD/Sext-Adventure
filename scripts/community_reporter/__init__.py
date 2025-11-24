#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Community Pulse Reporter
社群貢獻分析與報告生成模組

這個模組提供了 GitHub 倉庫貢獻分析的核心功能，可以：
- 獲取並分析貢獻者數據
- 生成月度/週期性報告
- 產生排行榜和統計數據

作者: Tsext Adventure Team
授權: MIT License
"""

__version__ = '1.0.0'
__author__ = 'Tsext Adventure Team'

from .github_client import GitHubClient
from .analyzer import ContributionAnalyzer
from .reporter import ReportGenerator

__all__ = ['GitHubClient', 'ContributionAnalyzer', 'ReportGenerator']

