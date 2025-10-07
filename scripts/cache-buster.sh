#!/bin/bash
# GitHub Pages 快取清除工具
# 解決 GitHub Pages 部署快取問題

set -e

echo "🧹 GitHub Pages 快取清除工具"
echo "================================"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 檢查參數
ACTION=${1:-"help"}
REPO_NAME=${2:-"dennislee928/tsext-adventure"}

show_help() {
    echo "用法: $0 [動作] [儲存庫名稱]"
    echo ""
    echo "動作:"
    echo "  help     顯示此說明"
    echo "  purge    清除所有快取"
    echo "  check    檢查版本"
    echo "  force    強制重新部署"
    echo "  status   顯示部署狀態"
    echo ""
    echo "範例:"
    echo "  $0 purge"
    echo "  $0 check dennislee928/tsext-adventure"
    echo ""
}

check_version() {
    echo -e "${BLUE}🔍 檢查當前版本...${NC}"
    
    # 檢查本地版本
    if [ -f "version.json" ]; then
        echo -e "${GREEN}本地版本:${NC}"
        cat version.json | grep -E '"version"|"build_number"|"last_updated"' | sed 's/^/  /'
    else
        echo -e "${YELLOW}⚠️  本地版本檔案不存在${NC}"
    fi
    
    # 檢查線上版本
    REPO_OWNER=$(echo $REPO_NAME | cut -d'/' -f1)
    REPO_REPO=$(echo $REPO_NAME | cut -d'/' -f2)
    PAGES_URL="https://${REPO_OWNER}.github.io/${REPO_REPO}"
    
    echo -e "${BLUE}線上版本檢查:${NC}"
    echo "  URL: $PAGES_URL"
    
    # 檢查主頁面
    if curl -s -I "$PAGES_URL" | grep -q "200 OK"; then
        echo -e "  ${GREEN}✅ 主頁面可訪問${NC}"
    else
        echo -e "  ${RED}❌ 主頁面無法訪問${NC}"
    fi
    
    # 檢查版本頁面
    if curl -s -I "$PAGES_URL/version-check.html" | grep -q "200 OK"; then
        echo -e "  ${GREEN}✅ 版本檢查頁面可訪問${NC}"
        echo "  ${BLUE}🔗 版本檢查: $PAGES_URL/version-check.html${NC}"
    else
        echo -e "  ${YELLOW}⚠️  版本檢查頁面不存在${NC}"
    fi
    
    # 檢查 GitHub Actions 狀態
    echo -e "${BLUE}GitHub Actions 狀態:${NC}"
    if command -v gh &> /dev/null; then
        gh run list --repo $REPO_NAME --limit 5 --json status,conclusion,createdAt,displayTitle | \
        jq -r '.[] | "  \(.displayTitle): \(.status) (\(.createdAt | strptime("%Y-%m-%dT%H:%M:%SZ") | strftime("%m-%d %H:%M")))"' || \
        echo "  無法取得 Actions 狀態"
    else
        echo "  請安裝 GitHub CLI (gh) 以查看 Actions 狀態"
    fi
}

purge_cache() {
    echo -e "${BLUE}🧹 清除快取...${NC}"
    
    # 1. 清除本地快取
    echo "1. 清除本地快取..."
    if [ -d "deploy" ]; then
        rm -rf deploy/*
        echo -e "  ${GREEN}✅ 本地部署目錄已清除${NC}"
    fi
    
    # 2. 強制更新版本
    echo "2. 強制更新版本..."
    if [ -f "scripts/version-manager.py" ]; then
        python3 scripts/version-manager.py
        echo -e "  ${GREEN}✅ 版本已更新${NC}"
    else
        echo -e "  ${YELLOW}⚠️  版本管理腳本不存在${NC}"
    fi
    
    # 3. 重新執行部署腳本
    echo "3. 重新執行部署腳本..."
    if [ -f "deploy.sh" ]; then
        chmod +x deploy.sh
        ./deploy.sh
        echo -e "  ${GREEN}✅ 部署腳本執行完成${NC}"
    else
        echo -e "  ${YELLOW}⚠️  部署腳本不存在${NC}"
    fi
    
    # 4. 推送變更到 GitHub
    echo "4. 推送變更到 GitHub..."
    if git status --porcelain | grep -q .; then
        git add .
        git commit -m "🧹 快取清除 - $(date)"
        git push origin main
        echo -e "  ${GREEN}✅ 變更已推送${NC}"
    else
        echo -e "  ${BLUE}ℹ️  沒有變更需要推送${NC}"
    fi
    
    echo -e "${GREEN}✅ 快取清除完成${NC}"
    echo ""
    echo -e "${BLUE}📋 後續步驟:${NC}"
    echo "1. 等待 5-10 分鐘讓 GitHub Pages CDN 更新"
    echo "2. 訪問版本檢查頁面確認更新"
    echo "3. 如果仍有問題，請使用者按 Ctrl+F5 強制重新整理"
}

force_redeploy() {
    echo -e "${BLUE}🚀 強制重新部署...${NC}"
    
    # 觸發 GitHub Actions 重新部署
    if command -v gh &> /dev/null; then
        echo "觸發 GitHub Actions 部署..."
        gh workflow run cache-management.yml --repo $REPO_NAME || \
        gh workflow run deploy.yml --repo $REPO_NAME
        echo -e "  ${GREEN}✅ GitHub Actions 已觸發${NC}"
    else
        echo -e "  ${YELLOW}⚠️  請手動觸發 GitHub Actions${NC}"
    fi
    
    # 等待並檢查狀態
    echo "等待部署完成..."
    sleep 60
    
    check_version
}

show_status() {
    echo -e "${BLUE}📊 部署狀態摘要${NC}"
    echo "===================="
    
    # 本地狀態
    echo -e "${BLUE}本地狀態:${NC}"
    if [ -f "version.json" ]; then
        VERSION=$(cat version.json | grep '"version"' | cut -d'"' -f4)
        BUILD=$(cat version.json | grep '"build_number"' | cut -d':' -f2 | tr -d ' ,')
        echo "  版本: $VERSION"
        echo "  建置: #$BUILD"
    fi
    
    echo "  Git 狀態: $(git status --porcelain | wc -l) 個變更"
    echo "  當前分支: $(git branch --show-current)"
    
    # 遠端狀態
    echo -e "${BLUE}遠端狀態:${NC}"
    REPO_OWNER=$(echo $REPO_NAME | cut -d'/' -f1)
    REPO_REPO=$(echo $REPO_NAME | cut -d'/' -f2)
    echo "  儲存庫: $REPO_NAME"
    echo "  GitHub Pages: https://${REPO_OWNER}.github.io/${REPO_REPO}"
    echo "  版本檢查: https://${REPO_OWNER}.github.io/${REPO_REPO}/version-check.html"
    
    # 檢查線上狀態
    PAGES_URL="https://${REPO_OWNER}.github.io/${REPO_REPO}"
    if curl -s -I "$PAGES_URL" | grep -q "200 OK"; then
        echo -e "  狀態: ${GREEN}✅ 線上${NC}"
    else
        echo -e "  狀態: ${RED}❌ 離線${NC}"
    fi
}

# 主程式
case $ACTION in
    "help"|"--help"|"-h")
        show_help
        ;;
    "check")
        check_version
        ;;
    "purge")
        purge_cache
        ;;
    "force")
        force_redeploy
        ;;
    "status")
        show_status
        ;;
    *)
        echo -e "${RED}❌ 未知動作: $ACTION${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎃 快取管理工具執行完成！${NC}"
