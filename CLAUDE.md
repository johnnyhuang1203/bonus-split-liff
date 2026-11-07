# 獎金分潤 LIFF — Claude Code 專案邊界

狀態: NOT_ENABLED

本檔是給 Claude Code 閱讀的專案邊界，不是已啟用的 GitHub 整合。
它不會啟動 GitHub Actions、不會呼叫 Claude、也不代表已接上任何人的本機會話或即時團隊同步。

GitHub 上的 Claude Code Action 仍待審核。啟用前的範本放在 `docs/claude-code/templates/claude.yml.example`，不在 `.github/workflows/`。審查說明見 `docs/claude-code/REVIEW.md`。

## 這個儲存庫

- 業務程式只有根目錄的 `index.html`：LINE LIFF 靜態頁，頁面內含試算、資料讀寫與畫面。
- 正式環境是 GitHub Pages。發布來源只有 `main` 分支的根目錄。`github-pages` 環境的部署分支政策也只有 `main`。
- 沒有分支預覽環境。正式 GitHub Pages 不是測試版，也不是其他分支的預覽。
- 沒有自訂 CI。唯一既有的 Actions 工作流是 GitHub Pages 內建的 `pages-build-deployment`，只隨 `main` 的正式發布運行。
- 沒有獨立測試套件。離線檢查只能用明標虛構資料，而且不得寫回既有雲端資料。

## 不可變更

- 不得修改獎金分潤規則、級距、稅務與折扣處理、分潤模型、撥付與責任額公式。
- 不得修改 `bracket`、`calc`，以及 `calc` 所使用的模型選擇與結果。
- 不得修改既有部署、Pages 來源、LIFF 初始化，或 `refresh` / `writeBlob` 的資料讀寫行為。
- 不得把 `SEED`、`BLOB_URL`、`LIFF_ID`、雲端回傳或畫面資料抄進文件、提交、日誌、PR 或留言。
- 不得讀取、列出、匯出或寫入真實客戶、人員、薪資或獎金資料。頁面內嵌種子與既有雲端路徑都算正式資料。
- 不得安裝 GitHub App、建立或讀取 secret、token、登入檔，不得寄信或發送其他外部訊息。
- 不得把 Cursor、Grok 或其他工具說成 Claude Code 引擎的替代品。本檔不新增機器人。

## 若將來獲准修改

只處理與業務公式無關、且經人工 diff 審查的文件或靜態檢查。
任何會讓 Claude 在 GitHub 上執行的工作流，都必須先有另行核准的啟用變更。
啟用前不得把範本移入 `.github/workflows/`，不得移除範本裡的停用條件，也不得填入認證。
