#!/bin/bash
# 本地測試 Community Pulse Reporter Action
# 此腳本用於在本地環境測試 Docker 構建和執行

set -e

echo "🚀 開始測試 Community Pulse Reporter..."
echo ""

# 檢查 Docker 是否安裝
if ! command -v docker &> /dev/null; then
    echo "❌ 錯誤: Docker 未安裝"
    echo "請先安裝 Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker 已安裝"
echo ""

# 檢查必需文件
echo "🔍 檢查必需文件..."
required_files=(
    "action.yml"
    "action.Dockerfile"
    "action_entrypoint.py"
    "requirements.txt"
    "scripts/community_reporter/__init__.py"
    "scripts/community_reporter/github_client.py"
    "scripts/community_reporter/analyzer.py"
    "scripts/community_reporter/reporter.py"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 錯誤: 找不到文件 $file"
        exit 1
    fi
    echo "  ✓ $file"
done

echo ""
echo "✅ 所有必需文件都存在"
echo ""

# 構建 Docker 映像
echo "🐳 構建 Docker 映像..."
docker build -f action.Dockerfile -t community-pulse-reporter:test .

if [ $? -eq 0 ]; then
    echo "✅ Docker 映像構建成功"
else
    echo "❌ Docker 映像構建失敗"
    exit 1
fi

echo ""
echo "🧪 測試執行 Action..."
echo ""

# 設定測試環境變數
export GITHUB_TOKEN="${GITHUB_TOKEN:-your_token_here}"
export REPO_OWNER="${REPO_OWNER:-dennislee928}"
export REPO_NAME="${REPO_NAME:-Sext-Adventure}"
export INTERVAL="${INTERVAL:-30}"
export OUTPUT_FILE="${OUTPUT_FILE:-COMMUNITY_REPORT_TEST.md}"
export INCLUDE_STATS="${INCLUDE_STATS:-true}"

# 顯示配置
echo "📋 測試配置："
echo "  - REPO_OWNER: $REPO_OWNER"
echo "  - REPO_NAME: $REPO_NAME"
echo "  - INTERVAL: $INTERVAL 天"
echo "  - OUTPUT_FILE: $OUTPUT_FILE"
echo ""

# 執行 Docker 容器
echo "🚀 執行測試..."
docker run --rm \
    -e GITHUB_TOKEN="$GITHUB_TOKEN" \
    -e REPO_OWNER="$REPO_OWNER" \
    -e REPO_NAME="$REPO_NAME" \
    -e INTERVAL="$INTERVAL" \
    -e OUTPUT_FILE="$OUTPUT_FILE" \
    -e INCLUDE_STATS="$INCLUDE_STATS" \
    -v "$(pwd):/workspace" \
    -w /workspace \
    community-pulse-reporter:test

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Action 執行成功！"
    echo ""
    
    # 檢查輸出文件
    if [ -f "$OUTPUT_FILE" ]; then
        echo "📄 報告已生成: $OUTPUT_FILE"
        echo ""
        echo "📊 報告預覽（前 30 行）："
        echo "----------------------------------------"
        head -n 30 "$OUTPUT_FILE"
        echo "----------------------------------------"
        echo ""
        echo "💡 完整報告請查看: $OUTPUT_FILE"
    else
        echo "⚠️  警告: 未找到輸出文件 $OUTPUT_FILE"
    fi
else
    echo ""
    echo "❌ Action 執行失敗"
    exit 1
fi

echo ""
echo "🎉 測試完成！"
echo ""
echo "下一步："
echo "  1. 查看生成的報告: $OUTPUT_FILE"
echo "  2. 檢查日誌輸出是否正確"
echo "  3. 如果一切正常，可以推送到 GitHub 並測試 Action"
echo ""

