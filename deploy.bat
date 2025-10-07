@echo off
REM Tsext Adventure: Halloween Haunt 部署腳本 (Windows - 含快取管理)

echo 🎃 Tsext Adventure: Halloween Haunt 部署腳本 🎃
echo ==================================================

REM 檢查是否在正確的目錄
if not exist "main.py" (
    echo ❌ 錯誤: 請在專案根目錄運行此腳本
    pause
    exit /b 1
)

REM 快取管理功能
set CACHE_MANAGEMENT=true
set VERSION_FILE=version.json
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set DEPLOY_TIMESTAMP=%dt:~0,8%_%dt:~8,6%

echo 🚀 開始部署流程 (含快取管理)
echo 部署時間戳: %DEPLOY_TIMESTAMP%

REM 版本管理和快取清除
if "%CACHE_MANAGEMENT%"=="true" (
    echo 🔧 執行版本管理和快取清除...
    
    REM 執行版本管理腳本
    if exist "scripts\version-manager.py" (
        echo 📝 更新版本號...
        python scripts\version-manager.py
    ) else (
        echo ⚠️  警告: 版本管理腳本不存在，跳過版本更新
    )
    
    REM 建立快取清除檔案
    echo 🧹 建立快取清除檔案...
    (
        echo # GitHub Pages 快取清除指南
        echo.
        echo ## 🚀 部署資訊
        echo - **部署時間**: %DEPLOY_TIMESTAMP%
        echo - **版本檔案**: %VERSION_FILE%
        echo - **快取管理**: 已啟用
        echo.
        echo ## 🧹 即時解決方法
        echo.
        echo ### 1. 強制重新整理
        echo - **Windows/Linux**: Ctrl + F5 或 Ctrl + Shift + R
        echo - **Mac**: Cmd + Shift + R
        echo - **手機**: 長按重新整理按鈕選擇「重新載入」
        echo.
        echo ### 2. 無痕模式
        echo 開啟瀏覽器的無痕/隱私模式瀏覽網站
        echo.
        echo ### 3. 清除瀏覽器快取
        echo 手動清除瀏覽器的快取資料
        echo.
        echo ## ⏰ 等待 CDN 更新
        echo GitHub Pages CDN 通常需要 5-10 分鐘更新
        echo.
        echo ## 🔍 版本檢查
        echo 訪問 `/version-check.html` 檢查當前版本
        echo.
        echo ---
        echo *自動生成於 %DEPLOY_TIMESTAMP%*
    ) > deploy\cache-info.md
)

REM 創建部署目錄
echo 📁 創建部署目錄...
if not exist "deploy" mkdir deploy
if not exist "deploy\github-pages" mkdir deploy\github-pages
if not exist "deploy\itch-io" mkdir deploy\itch-io

REM 複製 GitHub Pages 檔案 (含快取管理)
echo 🌐 準備 GitHub Pages 部署...
copy "web\index.html" "deploy\github-pages\"
copy "web\DEPLOYMENT.md" "deploy\github-pages\"

REM 加入快取管理檔案
if "%CACHE_MANAGEMENT%"=="true" (
    copy "deploy\cache-info.md" "deploy\github-pages\"
    if exist "%VERSION_FILE%" (
        copy "%VERSION_FILE%" "deploy\github-pages\"
    ) else (
        echo ⚠️  版本檔案不存在
    )
    
    REM 建立版本檢查頁面 (簡化版)
    (
        echo ^<!DOCTYPE html^>
        echo ^<html lang="zh-TW"^>
        echo ^<head^>
        echo     ^<meta charset="UTF-8"^>
        echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>
        echo     ^<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" /^>
        echo     ^<meta http-equiv="Pragma" content="no-cache" /^>
        echo     ^<meta http-equiv="Expires" content="0" /^>
        echo     ^<title^>版本檢查 - Tsext Adventure^</title^>
        echo ^</head^>
        echo ^<body^>
        echo     ^<h1^>🎃 Tsext Adventure - 版本檢查^</h1^>
        echo     ^<p^>部署時間戳: %DEPLOY_TIMESTAMP%^</p^>
        echo     ^<p^>如果看到舊版本，請按 Ctrl+F5 強制重新整理^</p^>
        echo     ^<a href="index.html"^>🎮 回到遊戲^</a^>
        echo ^</body^>
        echo ^</html^>
    ) > deploy\github-pages\version-check.html
)

REM 複製 itch.io 檔案
echo 🎮 準備 itch.io 部署...
copy "web\index.html" "deploy\itch-io\"
copy "itch-deploy\README.md" "deploy\itch-io\"

REM 創建 ZIP 檔案 (需要 PowerShell)
echo 📦 創建部署包...
powershell -command "Compress-Archive -Path 'deploy\itch-io\*' -DestinationPath 'deploy\tsext-adventure-itch-io.zip' -Force"

REM 顯示部署資訊
echo.
echo ✅ 部署準備完成！
echo.
echo 📁 部署檔案位置:
echo   • GitHub Pages: deploy\github-pages\
echo   • itch.io: deploy\itch-io\
echo   • itch.io ZIP: deploy\tsext-adventure-itch-io.zip
echo.

REM 快取管理資訊
if "%CACHE_MANAGEMENT%"=="true" (
    echo 🧹 快取管理功能:
    echo   • 版本檢查頁面: deploy\github-pages\version-check.html
    echo   • 快取清除指南: deploy\github-pages\cache-info.md
    echo   • 版本檔案: deploy\github-pages\version.json
    echo.
    echo 🔍 版本資訊:
    echo   • 部署時間戳: %DEPLOY_TIMESTAMP%
    echo.
)

echo 🚀 部署步驟:
echo.
echo GitHub Pages:
echo   1. 將 deploy\github-pages\ 的內容推送到 gh-pages 分支
echo   2. 或在 GitHub 設定中啟用 Pages
echo   3. 等待 5-10 分鐘讓 CDN 更新
echo   4. 訪問 /version-check.html 檢查版本
echo.
echo itch.io:
echo   1. 上傳 deploy\tsext-adventure-itch-io.zip
echo   2. 設置專案資訊
echo   3. 發布遊戲
echo.

REM 快取問題解決提示
if "%CACHE_MANAGEMENT%"=="true" (
    echo ⚠️  快取問題解決提示:
    echo   • 如果使用者看到舊版本，請他們按 Ctrl+F5 強制重新整理
    echo   • 或提供 /version-check.html 連結讓他們檢查版本
    echo   • 等待 5-10 分鐘讓 GitHub Pages CDN 更新
    echo.
)

echo 🎃 Happy Deploying! 🎃
pause
