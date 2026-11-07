# Claude Code GitHub 整合審查包

狀態：待審核。尚未啟用，尚未上線，串接沒有完成。

日期以培華 2026-11-07 台北時間的確認為準：在 GitHub 專案存取授權開通後，重試準備本儲存庫的 Claude Code 串接設定，供審核，不直接上線。

範圍只有 `johnnyhuang1203/bonus-split-liff`。沒有改其他系統、其他儲存庫或團隊權限。

這份文件準備給庫克所統籌的開發工具與協作流程審核。培華已經在使用 Claude Code。這裡要審的是日後如何讓指定的人在 GitHub 上看見進度、變更、測試結果與受控成果。引擎仍是 Claude Code。這不是新機器人，也不是用 Cursor 取代 Claude Code。

## 三層要分開看

### GitHub 開發紀錄可見

這是本 PR 目前做得到的一層。

有權限打開這個儲存庫的人，可以在分支、commit 與 PR 看見這次的文件 diff。儲存庫目前是 public，所以 PR 文字會是公開的。文件沒有秘密值，也沒有複製客戶或個人獎金資料。

這一層只代表「看得到準備中的設定與說明」。它不代表 Claude 已在 GitHub 上運行，也不代表有人能在網頁上操作一個新的測試版。

### 受控可操作測試版

目前沒有這一層。

調查時沒有預覽環境、沒有 GitHub Environment 除了正式用的 `github-pages`、沒有可對分支單獨開啟的測試站。正式 GitHub Pages 不是分支預覽，不能拿來當測試版。

既有頁面會讀寫正式雲端資料。在另案做成與正式 Pages、正式雲端資料隔離的環境之前，不存在受控可操作測試版。本 PR 沒有建立這個環境。

### 正式上線

正式站仍是既有 GitHub Pages：

- 網址：`https://johnnyhuang1203.github.io/bonus-split-liff/`
- 來源：`main` 分支根目錄
- 建置型別：legacy
- 部署環境 `github-pages` 的分支政策只有 `main`

本 PR 不合併、不部署、不改 `index.html`。正式站在這次審查期間維持原樣。

## 調查結果

調查日是 2026-11-07。官方依據是當日讀取的 [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)。

| 項目 | 結果 |
| --- | --- |
| 預設分支 | `main`。調查當下遠端只有這個分支；沒有分支保護，rulesets 為空。本審查分支是其後另開的，不在 Pages 發布來源內 |
| 程式與測試 | 只有 `README.md` 與 `index.html`。沒有測試套件，沒有既有 Claude 設定、`CLAUDE.md` 或 `.github/workflows` |
| 既有 Actions | 只有 GitHub 內建 `pages-build-deployment`。當時全部 35 筆執行的 ref 都是 `main` |
| 推分支會不會正式部署 | 不會。Pages 來源與部署分支政策都限定 `main`。本分支沒有放進 `.github/workflows` 的工作流 |
| 開 PR 會不會跑 Claude 或正式部署 | 不會。`main` 上沒有 `pull_request` 工作流，也沒有 Claude 工作流 |
| 合併會不會碰到正式發布 | 會，所以這次不合併。合併到 `main` 會觸發既有 Pages 再建置。即使 `index.html` 不變，新文件也會跟著正式站公開，並多一次正式建置 |
| 協作者 API | 只列出 `johnnyhuang1203`，角色 admin |
| Secrets / Actions variables | API 回 403，無法列出名稱。沒有讀取或寫入任何值 |
| Claude GitHub App | 沒有安裝。這次的權限也不足以替儲存庫安裝 |
| 本機 Claude 會話與 Grok Bot | 沒有連接，也沒有即時同步可驗證 |

官方手動安裝要三件事：安裝 Claude GitHub App、在 Actions secrets 放入一種認證、把可執行工作流放進 `.github/workflows/`。這三件事這次都沒做。官方也允許用既有 API key 或訂閱方案的 OAuth token，不要求一定新增 API key。Quick setup 的 `/install-github-app` 會直接安裝 App 並寫入 secret，因此沒有執行。

## 這次變更

- `CLAUDE.md`：日後 Claude Code 讀取的邊界。現在不會觸發雲端 Claude。
- `docs/claude-code/REVIEW.md`：本審查說明。
- `docs/claude-code/templates/claude.yml.example`：停用範本。副檔名不是 `.yml` 或 `.yaml`，目錄也不是 `.github/workflows/`。
- `docs/claude-code/verify_review_package.py`：離線靜態檢查。只用腳本內明標的虛構資料，不讀業務資料。
- `README.md`：加上指向本說明的兩句話。

沒有修改 `index.html`，沒有修改分潤規則或業務功能，沒有新增可執行工作流。

## 停用方式

GitHub Actions 只執行 `.github/workflows/` 底下、副檔名為 `.yml` 或 `.yaml` 的檔案。範本放在其他目錄，推分支與開 PR 都不會啟動它。

範本內部還有第二道停用條件：工作步驟的 `if` 固定為不成立。即使將來有人把檔案抄進 workflows，在拿掉該條件、並補上恰好一種認證之前，Claude 步驟也不會執行。

範本沒有 `push`、`pull_request`、`pull_request_target` 或 `schedule`。沒有自動化 `prompt`。認證兩行都維持註解。因此審核期間不會呼叫 Claude、不會消耗 Claude 用量，也不會因為這份新設定去部署。

## 團隊現在看得到什麼

- 這個 PR 的 diff、commit 與審查說明。
- 既有正式站。它仍是合併前的 `main`，不是這個分支的預覽。
- 既有 GitHub 提交歷史。

## 團隊現在還看不到什麼

- Claude 在 GitHub 上的執行、留言、進度或測試結果。整合沒有啟用。
- 這個分支的可操作測試版。沒有預覽環境。
- 培華本機 Claude Code 的會話。本 PR 沒有接上那些會話。
- Grok Bot 或其他即時團隊同步。沒有建立這條通道。
- 秘密值。文件只寫將來可能用到的名稱與設定位置。

## 最小權限

這份 PR 本身不授予任何新權限。

將來若核准啟用，官方互動模式工作流需要的 job token 權限是：

| 權限 | 原因 |
| --- | --- |
| Contents: write | Claude 才能在獲准後修改檔案並推 commit |
| Pull requests: write | 才能開 PR、寫審查留言 |
| Issues: write | 才能回覆 issue |
| id-token: write | 官方 Action 預設用它向 Claude GitHub App 換短效憑證 |
| Actions: read | 讓 Claude 讀取既有 CI 結果 |

官方 Claude GitHub App 一旦安裝，權限是整包的，不能只勾其中幾項。官方文件列出的安裝權限包含 Actions、Administration、Checks、Contents、Discussions、Issues、Members、Merge queues、Metadata、Pull requests、Repository hooks、Statuses、Workflows。其中有多項不是這個 Action 本身需要的。

若只要 Action 所用的最小集合，官方允許改用自訂 GitHub App，只給 Contents、Issues、Pull requests。自訂 App 不能順便涵蓋 Claude Code Review 或雲端自動修復。這次兩種 App 都沒有安裝，留待核准時二選一，而且只能選這個儲存庫，不對組織全部儲存庫安裝。

將來觸發者預設必須是有寫入權限的真人。不開放 `allowed_non_write_users`，也不把機器人列入 `allowed_bots`。

## 手動驗收

請審核者只做閱讀與 diff 檢查，不要留言 `@claude`，不要按合併。

1. `index.html` 與 `main` 相比沒有 diff。
2. `.github/workflows/` 仍不存在，PR 沒有新增 `.yml` 或 `.yaml` 工作流。
3. 範本仍在 `docs/claude-code/templates/claude.yml.example`。
4. 範本的執行條件仍是固定不成立，兩種認證仍是註解。
5. 全文搜尋不應出現 secret 的值、token、登入檔或雲端資料內容。
6. 在儲存庫根目錄執行 `python3 docs/claude-code/verify_review_package.py`，結果應為通過。這個檢查不連網、不讀業務資料。
7. 確認本 PR 的 Actions 沒有新的 Claude 工作，Pages 也沒有對這個分支部署。

## 費用控制

這次沒有新增付費服務，沒有啟動會產生費用的工作。

將來啟用後才可能產生兩類用量：GitHub 托管 runner 的 Actions 分鐘數，以及 Claude 用量。用訂閱 OAuth token 時，用量走該訂閱；用 API key 時才走 API 計費。兩者擇一，不為了這次審查另外申請 API key。公開儲存庫的 Actions 分鐘數是否計費，以核准當下的 GitHub 方案為準。

範本裡預留、但尚未生效的上限：

- 只回應明確提及，不在 push、PR 同步或排程時自動跑。
- `--max-turns 4`。
- job `timeout-minutes: 8`。
- concurrency 限制同一討論串同時只有一個執行，新的執行會取消尚未完成的舊執行。
- 不指定特定高價模型，避免在未核准前鎖定計費產品。
- 不加入每日報告、自動 code review 或對每個 PR 自動執行的工作流。

## 回復方案

現在的回復就是不合併並關閉本 PR。`main` 與正式 Pages 不會因為本分支存在而改變。

若將來誤合併本審查包：revert 該合併 commit。這會再觸發一次正式 Pages 建置。`index.html` 未改時，網站試算行為不變，但新增的說明檔會從正式站撤下。合併本身就會讓說明檔隨 Pages 公開，所以核准前不應合併。

若將來已把工作流放進 `.github/workflows/`：刪除該工作流後，Claude Code Action 就不再運行。不需為了回復去改業務程式。

若將來已寫入 secret：在下方設定位置刪除對應名稱。刪除 GitHub secret 不會自動作廢憑證本身。若用的是 API key，還要在 Claude Console 停用該 key。OAuth token 則由建立它的訂閱帳號作廢。這次沒有任何 secret 可刪。

若將來已安裝 GitHub App：只有在確認沒有其他 Claude 功能使用時才卸載。這次沒有安裝，沒有需要卸載的 App。

## 安全授權清單

核准啟用前，請逐項決定。未勾選的項目維持不做。

1. 是否同意本審查包的文字留在分支上供人閱讀。同意與否都不等於啟用。
2. 是否同意將來把說明檔合併進 `main`。合併會觸發正式 Pages 再建置，說明檔會變成公開靜態檔。
3. 認證方式：沿用訂閱 OAuth token，或使用 API key。不強制新開 API key。
4. 認證只存放在本儲存庫 Actions secrets。不要放到檔案、Pages、聊天或信件。
5. GitHub App：暫不安裝、安裝官方 App，或建立只含 Contents / Issues / Pull requests 的自訂 App。範圍只能是這個儲存庫。
6. 啟用 PR 必須另開。該 PR 才能移動範本、移除停用條件、取消註解恰好一種認證。
7. 指定哪些寫入權限的人可以在啟用後提及 Claude。沒有寫入權限的人預設不能觸發。
8. 受控可操作測試版若要做，必須與正式 Pages 和正式雲端資料隔離。這不是本 PR 的範圍。
9. Claude 將讀到的公開程式已含內嵌種子資料。禁止把該內容貼到日誌、PR 或留言。本審查包沒有複製該內容。
10. 不授權讀取或寫入真實客戶與個人獎金資料。靜態驗證只允許明標虛構資料。

## 秘密：只有名稱與設定位置

沒有收集、列印或寫入任何值。現有權限無法確認這兩個名稱是否已經存在。

| 名稱 | 何時才需要 | 公司核准的設定位置 |
| --- | --- | --- |
| `CLAUDE_CODE_OAUTH_TOKEN` | 選擇沿用 Claude 訂閱時 | 儲存庫 `johnnyhuang1203/bonus-split-liff` 的 Settings、Secrets and variables、Actions、Repository secrets |
| `ANTHROPIC_API_KEY` | 選擇 Claude API 計費時 | 同上，同一個 Repository secrets 清單 |

OAuth token 由已有訂閱的人在自己的電腦執行官方 `claude setup-token` 產生，再只把值貼進上述 GitHub secret。這次沒有執行該指令。API key 若採用，來自 Claude Console，同樣只進上述位置。兩個名稱擇一，不要兩個都當成必要項。

不要把值寫進工作流。將來啟用時，工作流只能引用 GitHub Actions 的 secrets 上下文。組織層 secret、其他儲存庫、雲端供應商金鑰與 workload identity 都不在這次範圍。

## 啟用前步驟

以下全部留待另一次書面核准。這次不執行。

1. 確認本 PR 的驗收清單通過，且仍然不合併啟用。
2. 選定 OAuth token 或 API key。
3. 由儲存庫管理員把所選名稱的值寫入上面的 Actions secret。值不經過 PR。
4. 選定並安裝官方 App 或自訂 App，只勾這個儲存庫。
5. 另開 PR，把範本複製成 `.github/workflows/claude.yml`，移除停用條件，取消註解恰好一種認證。
6. 該啟用 PR 仍不得加入 push、排程、自動 PR 審查，也不得把 Pages 改成預覽環境。
7. 啟用後的第一次手動驗收，使用與正式資料隔離的場合。不要在正式站或正式資料上試。
8. 若要停止，依回復方案刪除工作流；必要時再刪 secret 與卸載 App。

## 測試邊界

做過的與沒做的測試寫在 PR 說明。驗證腳本的通過只代表「審查包維持停用，且業務檔未被這次變更改動」。它不代表串接完成，也不代表業務公式已被重新驗證。
