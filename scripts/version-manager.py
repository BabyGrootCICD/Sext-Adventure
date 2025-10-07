#!/usr/bin/env python3
"""
GitHub Pages 快取問題解決方案 - 版本管理系統
自動管理檔案版本號，解決快取問題
"""

import json
import os
import re
import datetime
from pathlib import Path


class VersionManager:
    def __init__(self, version_file="version.json"):
        self.version_file = version_file
        self.version_data = self.load_version()
    
    def load_version(self):
        """載入版本資訊"""
        if os.path.exists(self.version_file):
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "version": "1.0.0",
                "build_number": 1,
                "last_updated": datetime.datetime.now().isoformat(),
                "files": {}
            }
    
    def save_version(self):
        """儲存版本資訊"""
        self.version_data["last_updated"] = datetime.datetime.now().isoformat()
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(self.version_data, f, indent=2, ensure_ascii=False)
    
    def increment_version(self, version_type="patch"):
        """增加版本號"""
        version = self.version_data["version"]
        major, minor, patch = map(int, version.split('.'))
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        self.version_data["version"] = f"{major}.{minor}.{patch}"
        self.version_data["build_number"] += 1
        
        print(f"版本更新: {version} -> {self.version_data['version']}")
        return self.version_data["version"]
    
    def get_file_version(self, file_path):
        """取得檔案版本號"""
        if file_path in self.version_data["files"]:
            return self.version_data["files"][file_path]
        else:
            # 新檔案，從 1 開始
            self.version_data["files"][file_path] = 1
            return 1
    
    def increment_file_version(self, file_path):
        """增加檔案版本號"""
        if file_path in self.version_data["files"]:
            self.version_data["files"][file_path] += 1
        else:
            self.version_data["files"][file_path] = 1
        return self.version_data["files"][file_path]
    
    def update_html_version(self, html_file="web/index.html"):
        """更新 HTML 檔案中的版本資訊"""
        if not os.path.exists(html_file):
            print(f"警告: {html_file} 不存在")
            return
        
        # 讀取 HTML 檔案
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新版本號
        new_version = self.increment_version("patch")
        content = re.sub(
            r'<meta name="version" content="[^"]*" />',
            f'<meta name="version" content="{new_version}" />',
            content
        )
        
        # 更新建置時間
        build_time = datetime.datetime.now().isoformat() + "Z"
        content = re.sub(
            r'<meta name="build-time" content="[^"]*" />',
            f'<meta name="build-time" content="{build_time}" />',
            content
        )
        
        # 寫回檔案
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已更新 {html_file} 版本為 {new_version}")
        return new_version
    
    def generate_versioned_html(self, input_file="web/index.html", output_dir="deploy/github-pages"):
        """產生版本化的 HTML 檔案"""
        if not os.path.exists(input_file):
            print(f"錯誤: {input_file} 不存在")
            return None
        
        # 確保輸出目錄存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 讀取原始 HTML
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新版本資訊
        version = self.increment_version("patch")
        build_time = datetime.datetime.now().isoformat() + "Z"
        
        # 替換版本資訊
        content = re.sub(
            r'<meta name="version" content="[^"]*" />',
            f'<meta name="version" content="{version}" />',
            content
        )
        content = re.sub(
            r'<meta name="build-time" content="[^"]*" />',
            f'<meta name="build-time" content="{build_time}" />',
            content
        )
        
        # 為 CSS 和 JS 加入版本參數
        content = re.sub(
            r'<style>',
            f'<style><!-- Version: {version} -->',
            content
        )
        
        # 寫入版本化檔案
        output_file = os.path.join(output_dir, "index.html")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"已產生版本化檔案: {output_file} (版本: {version})")
        return output_file
    
    def create_cache_buster_script(self, output_dir="deploy/github-pages"):
        """建立快取清除腳本"""
        os.makedirs(output_dir, exist_ok=True)
        
        script_content = f'''#!/bin/bash
# GitHub Pages 快取清除腳本
# 版本: {self.version_data["version"]}
# 建置時間: {self.version_data["last_updated"]}

echo "🧹 GitHub Pages 快取清除工具"
echo "版本: {self.version_data["version"]}"
echo "=================================="

# 方法 1: 強制重新整理提示
echo "📱 使用者端解決方案:"
echo "1. 按 Ctrl+F5 (Windows/Linux) 或 Cmd+Shift+R (Mac) 強制重新整理"
echo "2. 開啟無痕模式瀏覽網站"
echo "3. 清除瀏覽器快取"

# 方法 2: 等待 CDN 更新
echo ""
echo "⏰ 伺服器端解決方案:"
echo "1. 等待 5-10 分鐘讓 CDN 更新"
echo "2. 使用不同網路環境測試"
echo "3. 檢查版本號是否更新"

# 檢查版本
echo ""
echo "🔍 版本檢查:"
echo "當前版本: {self.version_data["version"]}"
echo "建置時間: {self.version_data["last_updated"]}"

# 建立版本檢查頁面
cat > {output_dir}/version-check.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>版本檢查 - Tsext Adventure</title>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />
</head>
<body>
    <h1>版本檢查</h1>
    <p>當前版本: {self.version_data["version"]}</p>
    <p>建置時間: {self.version_data["last_updated"]}</p>
    <p>如果看到舊版本，請按 Ctrl+F5 強制重新整理</p>
    <script>
        console.log('版本檢查頁面載入時間:', new Date().toISOString());
    </script>
</body>
</html>
EOF

echo "✅ 快取清除腳本建立完成"
echo "📁 檔案位置: {output_dir}/cache-buster.sh"
echo "🌐 版本檢查: {output_dir}/version-check.html"
'''
        
        script_file = os.path.join(output_dir, "cache-buster.sh")
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 設定執行權限
        os.chmod(script_file, 0o755)
        
        print(f"快取清除腳本已建立: {script_file}")
        return script_file


def main():
    """主程式"""
    print("Tsext Adventure - 版本管理系統")
    print("=====================================")
    
    vm = VersionManager()
    
    # 顯示當前版本
    print(f"當前版本: {vm.version_data['version']}")
    print(f"建置編號: {vm.version_data['build_number']}")
    print(f"最後更新: {vm.version_data['last_updated']}")
    
    # 更新 HTML 版本
    if os.path.exists("web/index.html"):
        print("\n更新 HTML 版本...")
        new_version = vm.update_html_version()
        print(f"新版本: {new_version}")
    
    # 產生部署檔案
    print("\n產生部署檔案...")
    deploy_file = vm.generate_versioned_html()
    
    # 建立快取清除腳本
    print("\n建立快取清除腳本...")
    cache_script = vm.create_cache_buster_script()
    
    # 儲存版本資訊
    vm.save_version()
    
    print("\n版本管理完成！")
    print(f"部署檔案: {deploy_file}")
    print(f"快取腳本: {cache_script}")
    print(f"版本檔案: {vm.version_file}")


if __name__ == "__main__":
    main()
