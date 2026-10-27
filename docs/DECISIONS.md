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

9. **依賴警示在 fork 內修；CodeQL 警示逐筆判讀，真缺陷修最小補丁，誤報附 source/sink 理由關閉**
   - **現行決定**（2026-10-28 重判，取代 2026-10-24 的「上游程式只記錄不改」）：41 筆 open CodeQL 全部落在上游持有的檔案。逐筆讀原始碼後，能說出「什麼輸入會錯、錯成什麼」的就修，加分岔列與 `tests/fork-security-fixes.standalone.test.ts` 回歸測試；其餘在 GitHub 逐筆 dismiss，理由寫在該筆告警上，摘要如下。
   - **修掉（3 項）**：
     - #13 `js/incomplete-sanitization`（`publication/agent.ts` `linkText`）：先前判為「Markdown 跳脫風格」是錯的。標題 `x\](https://evil.example)` 會在給 AI 的 Markdown 造出外部連結；`6668f48` 連 `\` 一起跳脫。
     - #15 `js/incomplete-sanitization`（`contracts/http-policy.ts`）：路徑尾段當成 `replace` 的替換字串，``/sources/a$`b`` 轉成 `/admin/sources/a/admin/sourcesb`；`634f90d` 改成函式替換。
     - 判讀 #42／#43 時發現：`admin-auth.ts` 嘗試表滿 5000 筆時連全站計數一起清掉，偽造 `X-Forwarded-For` 可重置「50 次／15 分鐘」上限；`37b043e` 只清各 IP 的筆數。
   - **誤報（false positive）**：
     - `js/missing-rate-limiting` #17、#19、#20、#42、#43（admin-auth.ts）：#42／#43 密碼登入有行程內限流 `tooManyAttempts`（每 IP 10 次、全站 50 次／15 分鐘，`37b043e` 後全站上限不會被重置），CodeQL 不認得自寫限流；#17 `/api/auth/options` 只回兩個設定布林值；#19 `/api/auth/feishu`、#20 `/api/auth/callback` 是 OAuth 轉向與一次性 code 交換，要先過 state cookie 比對。
     - `js/missing-rate-limiting` #22（admin.ts 截圖）：在 `adminHandler` 內，要有效管理員 session。#21（ingest.ts）：先比對至少 16 字的 `INGEST_TOKEN`（常數時間），且有 `INGEST_RATE_LIMIT`（docker compose 預設 10／分）。#23（media.ts）：先驗 HMAC 簽章與期限，未簽的請求不讀檔不抓圖。#44（mcp.ts）：公開唯讀端點，有 `bodyLimit`。#24（static.ts）：只讀站方自有檔案並有 ETag 快取；這幾類流量限制交給前置代理。
     - `js/path-injection` #4、#6、#38（static.ts）：唯一的外部檔名來源是 `/contact/:file`，先過 `^[\w.-]+\.(png|jpg|jpeg|webp)$`，不含 `/` 或 `\`，`path.join` 不會離開 `uploads`／`brand/contact`；其他 `sendFile` 呼叫的路徑都是程式內寫死的。
     - `js/file-system-race` #46（static.ts）：stat 與 readFile 之間檔案變了，只會讓快取存一份新內容配舊 mtime，下次 stat 就重讀；只讀、無寫入。
     - `js/xss-through-dom` #2（feedback.tsx）：`src` 是 `URL.createObjectURL(file)` 的 `blob:` 位址，不是文字輸入。
     - `js/insufficient-password-hash` #27、#28、#29（admin/auth.ts）：沒有儲存任何密碼雜湊。#28／#29 的 HMAC 只把兩邊變成等長再 `timingSafeEqual`；#27 是把 session 綁在目前密碼上的 HMAC。密碼本身在環境變數。
     - `js/incomplete-sanitization` #12（markdown.ts）：表格儲存格先經 turndown，turndown 已把 `\` 跳脫成 `\\`，這裡只補 `|`；實測儲存格 `a\|b` 輸出 `a\\\|b`，欄數不變。
     - `js/incomplete-sanitization` #14、`js/bad-tag-filter` #7（json-list.ts）：前者用管理員設定的變數名組 RegExp，後者是從抓回的頁面找 JSON script 區塊；都不是輸出過濾，漏抓只會讓該信源回 `FetchError`。
     - `js/file-access-to-http` #47（llm.ts）：送出的是提示詞與設定的 API 金鑰，目的地是維護者設定的 `LLM_BASE_URL`，這就是功能本身。
     - `js/clear-text-logging` #26（init-env.ts）：一次性把剛產生的管理員密碼印給操作者，檔頭與文件都寫明。
   - **真實但不修（won't fix）**：
     - `js/polynomial-redos` #1（ingest.ts `/^Bearer\s+(.+)$/i`）：要讓 `$` 失敗需要換行字元，Node 的 HTTP 解析器對 CR／LF 回 400；標頭上限 16 KB。
     - `js/double-escaping` #41（writing.ts）：`&amp;lt;` 會還原成 `<`；結果只進 LLM 提示純文字，不當 HTML 輸出。
     - `js/file-system-race` #32（init-env.ts）：`existsSync` 後 `writeFileSync`；單人本機一次性腳本，攻擊者要先能寫工作目錄。
   - **測試碼（used in tests）**：#35、#36、#37 `js/reflected-xss` 是測試裡綁 `127.0.0.1` 的假伺服器；#45 `js/server-side-unvalidated-url-redirection` 是故意做轉址的測試假伺服器；#39、#40 是對固定 HTML 的斷言；#48–#54 `js/regex/missing-regexp-anchor` 是對已知輸出做 `assert.match`。都不處理外部輸入。
   - **重審條件**：新告警逐筆判讀；上游改了上述檔案時，對照分岔列決定刪列或保留。
   - **理由**：「上游程式不改」會把真缺陷（#13、#15、限流重置）一起放著；每項修正都小且附回歸測試，分岔表寫明上游修好就刪。
