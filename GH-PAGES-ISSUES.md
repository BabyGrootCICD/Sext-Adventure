GitHub Pages 部署快取問題及解決方案
快取問題的存在
是的，GitHub Pages 部署確實容易遇到前次殘存快取問題。這是一個普遍且常見的問題，主要涉及多層快取機制：

多層快取結構：

瀏覽器本地快取

GitHub Pages CDN 快取（預設 max-age=600，即10分鐘）

DNS 快取

代理伺服器快取

問題產生原因
1. GitHub Pages 快取設定
GitHub Pages 預設設定 Cache-Control: max-age=600，意味著快取時效為10分鐘。雖然時間不長，但在開發測試階段仍可能造成困擾。

2. 瀏覽器快取機制
瀏覽器會根據 HTTP 快取標頭決定是否使用本地快取，即使伺服器內容已更新，瀏覽器可能仍顯示舊版本。

3. CDN 快取
GitHub Pages 使用 CDN 服務，不同地理位置的使用者可能看到不同版本的內容。

解決方案
即時解決方法
1. 強制重新整理

Windows/Linux：Ctrl + F5 或 Ctrl + Shift + R

Mac：Cmd + Shift + R
這會跳過瀏覽器快取強制重新載入

2. 使用無痕模式
開啟瀏覽器的無痕/隱私模式瀏覽網站，避免使用快取

3. 清除瀏覽器快取
手動清除瀏覽器的快取資料，特別是過去一小時的資料通常最有效

開發端解決方案
1. 在 HTML 中加入防快取標頭

xml
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />
2. 檔案版本化
為靜態資源（CSS、JS）加入版本號：

xml
<link rel="stylesheet" href="css/style.css?v=1.0.3">
<script src="js/main.js?v=1.0.3"></script>
每次更新時修改版本號，強制瀏覽器重新載入

3. 使用 gh-pages 套件部署
對於 Node.js 專案，使用 gh-pages 套件可以更好地控制部署過程：

json
{
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
部署完成後等待 2-5 分鐘讓更新生效

系統性解決方案
1. GitHub Actions 快取管理
可以透過 GitHub CLI 或 Actions 清除快取：

bash
gh cache delete --all
或使用 GitHub Actions 工作流程自動清除
