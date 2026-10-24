# 架構與維護決策記錄（DECISIONS.md）

本文件遵循精簡原則，僅記錄現行決定與一行理由。

---

## 決策清單

1. **以繁體中文作為主入口文件語言（`README.md`、`AGENTS.md`、`docs/*.md`）**
   - **現行決定**：核心文件全面採用繁體中文，上游原版英文/簡中鏡像完整保留在 `README.en.md`。
   - **理由**：符合本機主要維護者溝通習慣，並便於台灣業界與個人熱點站落地。

2. **追蹤上游最新進展，分岔處嚴格登記於 `docs/DIVERGENCE.md`**
   - **現行決定**：接受隨維護深入必然產生的分岔，所有對上游持有檔之變更均登載於分岔表，並由 `tools/check_divergence.py` 機器強制比對。
   - **理由**：避免每次同步上游時遺失判斷脈絡，以機器檢查杜絕文件腐爛。

3. **協作流程採「做完就 push 到 main、不開分支、不開 PR」**
   - **現行決定**：個人維護線全部在 `origin/main` 進行，驗證通過直接 push，不留常駐分支。
   - **理由**：個人專案無需多餘分支審查摩擦，push 即為可靠備份。

4. **對外只打 `SanHsien/AIHOT`，禁止未經授權對上游開 PR**
   - **現行決定**：`gh repo set-default SanHsien/AIHOT`，所有 GitHub 操作限定在本 Fork 內。
   - **理由**：防範維護骨架與客製變更誤提至上游公共倉庫。

5. **全庫設定 `.gitattributes` 強制 `eol=lf`**
   - **現行決定**：根目錄設定 `* text=auto eol=lf`。
   - **理由**：避免 Windows 原生環境因 CRLF 導致 lint、diff 或 shell 解析誤報。

6. **開發與測試預設關閉模型與采集安全閥**
   - **現行決定**：單元測試與一般本機建置強制 `COLLECT_ENABLED=false` 與 `MODEL_CALLS_ENABLED=false`。
   - **理由**：防止本機測試非預期消耗外部付費 API 額度。

7. **分支只留 `main`；release 與 tag 只留最新一份**
   - **現行決定**：合併或結案後刪除工作分支；發布新版本並驗證成功後，移除較舊 release 與 tag。
   - **理由**：維持個人維護線簡潔，避免過期分支與重複發布物造成誤用。

8. **上游審查採六軸紀錄，不重做相同判斷**
   - **現行決定**：commit、PR、issue、branch、tag、release 的決策寫在 `docs/UPSTREAM.md`，SHA／狀態水位寫在 `tools/upstream_baseline.json`。
   - **理由**：相同 head 與狀態不應每次巡檢重新閱讀；只有內容或狀態改變才重審。

9. **依賴警示在 fork 內修；CodeQL 警示分流，上游持有的程式碼只記錄不改**
   - **現行決定**：2026-10-24 清掉全部 20 項 Dependabot 與 `npm audit` 的 4 項（見 `docs/DIVERGENCE.md` 的 manifest 列）；Dependabot PR #4–#10 由同一個 bump 涵蓋。34 項 CodeQL 警示逐項看過原始碼：沒有一項落在 fork 自有程式碼，因此不在 fork 內改上游持有的檔案（會新增分岔列），結論如下，待下次對齊上游後重掃。
   - **誤報（28 項）**：
     - `js/missing-rate-limiting` #16–#20、#22、#23、#25：登入有行程內限流（`tooManyAttempts`，每 IP 10 次／全站 50 次），後台路由要簽章 session，圖片代理要簽章，MCP 為公開唯讀；限流交給前置代理。#21、#24 見下方「真實但不修」。
     - `js/insufficient-password-hash` #27–#29：HMAC-SHA256 只用來把兩邊補成等長再做 `timingSafeEqual`（#28、#29）與把 session 綁在密碼上（#27）；管理員密碼本來就在環境變數，沒有儲存的密碼雜湊可被離線爆破。
     - `js/path-injection` #4–#6、`js/file-system-race` #31（static.ts）：檔名先過 `^[a-z0-9-]+\.(svg|png)$` 與 `^[\w.-]+\.(png|jpg|jpeg|webp)$`，不含路徑分隔字元；stat／readFile 之間的競態只會讓快取放一份稍舊的伺服器自有檔案。
     - `js/xss-through-dom` #2（feedback.tsx）：`src` 是 `URL.createObjectURL(file)` 產生的 `blob:` 位址。
     - `js/bad-tag-filter` #7、`js/incomplete-sanitization` #14（json-list.ts）：是從抓回的頁面取 JSON 與用管理員設定的變數名組 RegExp，不是輸出過濾。
     - `js/incomplete-multi-character-sanitization` #9（detail.ts）：只為大綱取純文字，輸出仍由 React 跳脫。
     - `js/incomplete-sanitization` #12（markdown.ts）、#13（agent.ts）、#15（http-policy.ts）：Markdown 輸出的跳脫風格、靜態規則表裡只有一個 `*`；非 HTML 邊界。
     - `js/clear-text-logging` #26（init-env.ts）：一次性把產生的管理員密碼印給操作者，是文件寫明的行為。
     - `js/file-access-to-http` #33（llm.ts）：API 金鑰本來就是設定，送往設定的 `LLM_BASE_URL`。
     - 測試碼 #3、#8、#30、#34：只在測試裡對固定字串或本機暫時伺服器做斷言，不處理外部輸入。
   - **真實但不修（6 項，影響低）**：
     - `js/polynomial-redos` #1（ingest.ts `/^Bearer\s+(.+)$/i`）：正則確為二次方（16 KB 約 82 ms），但要讓 `$` 失敗必須有換行字元，Node 的 HTTP 解析器對 CR／LF 回 400、UTF-8 的 U+2028 會被拆成 latin1 位元組，實測從網路送不進來。
     - `js/double-escaping` #10、#11（writing.ts、text.ts）：`&amp;` 先於 `&lt;` 還原，`&amp;lt;` 會變成 `<`；結果只進純文字欄位與 LLM 提示，不當 HTML 用。
     - `js/file-system-race` #32（init-env.ts）：`existsSync` 後 `writeFileSync` 可被搶先建立的 `.env` 覆蓋；單人本機一次性腳本，修法是寫入加 `flag: "wx"`。
     - `js/missing-rate-limiting` #21（ingest.ts）：令牌比對在限流之前，可無限次猜測；令牌至少 16 字且常數時間比較。上游較新版本已加入 `INGEST_RATE_LIMIT`。
     - `js/missing-rate-limiting` #24（static.ts）：靜態檔案無應用層限流，交給前置代理。
   - **重審條件**：下次合併上游後重跑 CodeQL；上述 6 項若上游已改就隨之消失，未改且仍在 fork 內被觸及時，修成最小補丁並加分岔列。fork 自有程式碼出現的警示一律在 fork 內修。
   - **理由**：核心程式碼跟隨上游，逐項寫下判斷才不會每次重看；不為了讓警示變零而新增分岔。
