@echo off
REM Tsext Adventure: Halloween Haunt 部署腳本 (Windows)

echo 🎃 Tsext Adventure: Halloween Haunt 部署腳本 🎃
echo ==================================================

REM 檢查是否在正確的目錄
if not exist "main.py" (
    echo ❌ 錯誤: 請在專案根目錄運行此腳本
    pause
    exit /b 1
)

REM 創建部署目錄
echo 📁 創建部署目錄...
if not exist "deploy" mkdir deploy
if not exist "deploy\github-pages" mkdir deploy\github-pages
if not exist "deploy\itch-io" mkdir deploy\itch-io

REM 複製 GitHub Pages 檔案
echo 🌐 準備 GitHub Pages 部署...
copy "web\index.html" "deploy\github-pages\"
copy "web\DEPLOYMENT.md" "deploy\github-pages\"

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
echo 🚀 部署步驟:
echo.
echo GitHub Pages:
echo   1. 將 deploy\github-pages\ 的內容推送到 gh-pages 分支
echo   2. 或在 GitHub 設定中啟用 Pages
echo.
echo itch.io:
echo   1. 上傳 deploy\tsext-adventure-itch-io.zip
echo   2. 設置專案資訊
echo   3. 發布遊戲
echo.
echo 🎃 Happy Deploying! 🎃
pause
