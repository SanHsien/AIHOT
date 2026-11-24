# 架構與維護決策記錄（DECISIONS.md）

本文件遵循精簡原則，僅記錄現行決定與一行理由。

---

## 決策清單

- **2026-11-25 前次阻礙已解除**：`67116b6` 因文件範圍不足保留水位；本輪已允許分岔及上游紀錄，逐筆結論以下表為準。

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

10. **GitHub 以 Actions 用量過大停用本 fork 的 Actions（2026-11-23）；push 觸發改為只跑會影響結果的變更**
   - **量測**：近 30 天（10-27..11-22）`gh run list` 前 100 筆：Check 25 次 push、Fork Quality & Divergence Check 25 次 push、CodeQL 26 次 push（每次 2 個語言 job）；排程本來就是每週／每月（CodeQL、Upstream check 週一，Dependency freshness 每月 1 日），不是主要來源。用量全在每次 push 都跑三個 workflow。
   - **現行決定**：`check.yml`、`fork-check.yml` 的 push 觸發對只改維護紀錄的提交（`ROADMAP.md`、`REVIEW.md`、`FORK.md`、`NOTICE.md`、兩份報告、`docs/UPSTREAM.md`、`docs/DECISIONS.md`、`tools/upstream_baseline.json`）略過；`codeql.yml` 的 push 只在 JS/TS/Python 原始碼或該 workflow 改動時跑。三者的 pull_request 與 CodeQL 每週排程不加篩選，所有改動仍至少每週掃一次。`docs/DIVERGENCE.md` 刻意不略過（`check_divergence.py` 讀它）。
   - **預估**：push 觸發的 run 數約減少一半以上（多數提交是紀錄類）；沒有刪任何檢查。
   - **還原**：移除上述 `paths-ignore`／`paths` 區塊即回到每次 push 全跑。
   - **重審條件**：Actions 重新啟用後再用 `gh run list` 量一次，仍被限制再降頻。


## 2026-11-25：上游 103 筆逐項裁決

固定範圍 `7140b6f..bc57d79`，依 Git 拓撲順序共 103 筆；採納 6、延後 85、拒絕 12。每一列對應一個 commit，不把一個 PR 與它的 commit 重複計數。PR #375 的合併產物就是第 1 列；其餘以可追溯 commit URL 作本輪單位。未另行刷新範圍外的 PR／issue 庫存，相關水位保持不變。

延後列的 G1–G10 是分類代號，完整觸發條件只維護於 [ROADMAP.md](../ROADMAP.md)；不是因為水位推進就算採納。拒絕中間版本不代表拒絕其最終修正；表內明列替代關係。

| # | 上游 commit | 裁決 | 理由／觸發分類 |
|---:|---|---|---|
| 1 | [bb9a507](https://github.com/KKKKhazix/AIHOT/commit/bb9a507b9fca8009c9e3cd6bdc366401b0df622a) | defer | #375：合併與重新發布改成同一交易，遞迴解析長合併鏈，向量查詢改 ANY 陣列；需驗證回滾、長鏈及 65536 筆召回。 觸發：G1（見 ROADMAP）。 |
| 2 | [ba3e9b8](https://github.com/KKKKhazix/AIHOT/commit/ba3e9b87c8ad78f516e39aa2aa3e69d94f240ea7) | defer | 未匹配討論只撤銷仍在 RECALL_DAYS 視窗的事件熱度，避免重判刪掉已過期召回的證據。 觸發：G1（見 ROADMAP）。 |
| 3 | [863bc1a](https://github.com/KKKKhazix/AIHOT/commit/863bc1a584e9a80841045398f088d74ed7660264) | reject | 交易內重發前鎖全部文章的中間方案，已被 45ebf34 及 69a9d5f 的完整鎖序取代，不單獨套用。 |
| 4 | [be59ff3](https://github.com/KKKKhazix/AIHOT/commit/be59ff360e718df0d7f165613f7580e264785433) | reject | 撤回 bb9a507 在無向量時清除證據的行為；目前 fork 原本就直接返回 signal-unmatched，已具備此行為。 |
| 5 | [7781f01](https://github.com/KKKKhazix/AIHOT/commit/7781f01d9441e9dc1c47bc524c1113bbc34f6cf9) | defer | 未附著討論依最新 grouping_decisions 而非任何歷史判決決定可否重新匹配，須驗證撤下後再附著。 觸發：G1（見 ROADMAP）。 |
| 6 | [eed37da](https://github.com/KKKKhazix/AIHOT/commit/eed37dac26f00d63ca252fd4ca8eb4b8dfac9dd7) | defer | 熱度夾具前移一分鐘，配合新增 signals 回歸，避免測試建立時間邊界。 觸發：G1（見 ROADMAP）。 |
| 7 | [45ebf34](https://github.com/KKKKhazix/AIHOT/commit/45ebf34711490243b58d19170bd0f2db97503adb) | reject | 先文章後事件的中間鎖序已被 69a9d5f 補為事實、文章、事件；不採用過渡版本。 |
| 8 | [d4f1f7f](https://github.com/KKKKhazix/AIHOT/commit/d4f1f7fb6ac67e529305f7a49421254f529deb76) | defer | 目前附著事件的事實排除於 answered 集合，須重新判斷，避免舊否決撤銷後來的附著。 觸發：G1（見 ROADMAP）。 |
| 9 | [cce8025](https://github.com/KKKKhazix/AIHOT/commit/cce802596a14b847af1f13a43da6315c462e43e7) | defer | 判斷舊事件能否召回時也要求 groupingEvidenceCondition，與實際候選的證據範圍一致。 觸發：G1（見 ROADMAP）。 |
| 10 | [69a9d5f](https://github.com/KKKKhazix/AIHOT/commit/69a9d5f9c8ca535fe46fc9431ed972a7b825447a) | defer | 最終合併鎖序是 facts NO KEY UPDATE、articles FOR UPDATE、stories；不可只採中間兩版，需交易併發驗證。 觸發：G1（見 ROADMAP）。 |
| 11 | [a500884](https://github.com/KKKKhazix/AIHOT/commit/a500884ca391aa0d47b2e576a90067d2436ba9a1) | defer | SignalRiver 與 Halftone 共用 seededRandom，屬前端繪圖去重，沒有獨立產品缺陷需要本輪移植。 觸發：G4（見 ROADMAP）。 |
| 12 | [2f9df7e](https://github.com/KKKKhazix/AIHOT/commit/2f9df7e54e01c939bf6b2232cc18819b7705f042) | defer | 以 host、PID、birth 辨識中斷工作；翻譯綁 revision、投遞放棄改 skipped、採集狀態交易化；Windows 無 processBirth 證據時不回收。 觸發：G2（見 ROADMAP）。 |
| 13 | [2697657](https://github.com/KKKKhazix/AIHOT/commit/269765738daf6b15316fa69e504087a73f54738b) | defer | 翻譯上限依 shield 後送模型的字元數計算，避免長媒體網址耗掉正文額度；應與 revision 回歸一起驗收。 觸發：G2（見 ROADMAP）。 |
| 14 | [83b32d3](https://github.com/KKKKhazix/AIHOT/commit/83b32d3f168940c8e796d1be2468197900292db1) | defer | #390：補釘釘安全閥與英文 Agent 入口說明；需人工合併繁中 AGENTS 及 fork 英文入口，不用上游原檔覆蓋。 觸發：G3（見 ROADMAP）。 |
| 15 | [26e9e24](https://github.com/KKKKhazix/AIHOT/commit/26e9e24a17bf5894d5c64612643bbb64446e4b01) | defer | Finding 型別要求 agentOnly 同時給 agentType，移除 alert.review 的隱含類型；與告警呼叫端一起驗型別及事件內容。 觸發：G2（見 ROADMAP）。 |
| 16 | [408d112](https://github.com/KKKKhazix/AIHOT/commit/408d1127a1bda8ab4aa026a2d403b48941d78528) | reject | fast-xml-parser 5.12.0 已由 fork 先行採納；目前鎖檔的 parser、entities、is-unsafe、strnum 版本均與 d342846 相同，不重複升級。 |
| 17 | [d342846](https://github.com/KKKKhazix/AIHOT/commit/d342846e785db3a9a713a869efbc78b9a2dca67c) | reject | 5.12.0 鎖檔對齊已具備；本輪實際核對四個解析套件版本一致，不把重複修改列為新採納。 |
| 18 | [e385794](https://github.com/KKKKhazix/AIHOT/commit/e3857943ddb53b1d2ea13d346be2e06709b2be19) | defer | Score 標籤及數字的視覺位移微調，留待同批前端版型驗收，沒有行為修正可獨立證明。 觸發：G4（見 ROADMAP）。 |
| 19 | [11da55c](https://github.com/KKKKhazix/AIHOT/commit/11da55cca2ee7b21d37ed432efe9362cce3b7b05) | defer | 新增 sendPageMarkdown 的 noindex、canonical 及模組 agent.pages、SEO alternate，屬模組 Markdown 出口擴充。 觸發：G3（見 ROADMAP）。 |
| 20 | [70d1349](https://github.com/KKKKhazix/AIHOT/commit/70d134925fd7ca038184d19d7d80b2856a066f43) | defer | 新增帳號掛載、收藏訂閱與寫入、同步契約和模組 provider 定義；目前沒有啟用帳號模組的需求，需整合同步邊界測試。 觸發：G3（見 ROADMAP）。 |
| 21 | [af712e5](https://github.com/KKKKhazix/AIHOT/commit/af712e5119a1594a5908213ef6c74463a2737b0d) | defer | 側欄 GitHub 與外觀切換改為同行排列，配合新帳號區，需要桌面及手機版型驗收。 觸發：G4（見 ROADMAP）。 |
| 22 | [860ee12](https://github.com/KKKKhazix/AIHOT/commit/860ee12060f2dfb940a4a2ca92a440c8779d5d84) | defer | Presence 在首個 render 就套 enter 動畫以消除閃爍；需可重現首幀問題及 reduced-motion、退出動畫回歸。 觸發：G4（見 ROADMAP）。 |
| 23 | [ad5472c](https://github.com/KKKKhazix/AIHOT/commit/ad5472c00dc527e762894061cab5d234fd3987e2) | reject | 收藏頁首次掛載 Account 的版本已被 e3bd0ad 原樣撤回，最終方案在 cb5d4e5／4468bb5，不單獨採納。 |
| 24 | [e3bd0ad](https://github.com/KKKKhazix/AIHOT/commit/e3bd0adc637da20c0d0740a8de85a431ed3397cd) | reject | 只撤回 ad5472c；目前 fork 未加入該中間版本，現行收藏頁已是本機儲存提示，無需重做。 |
| 25 | [02c4843](https://github.com/KKKKhazix/AIHOT/commit/02c484357d4daf82655b19af2985abec30b2e7d2) | defer | 同步去掉刪除記錄的 90 天清除、驗證安全時間戳與原型鍵；收藏可保留超過 500 筆的帳號快照，須連同同步契約驗收。 觸發：G3（見 ROADMAP）。 |
| 26 | [7be84c2](https://github.com/KKKKhazix/AIHOT/commit/7be84c2dc3684dfd11a928e96dbb7d2a8d218c31) | defer | modal 焦點候選加入 iframe；需 iframe Tab 循環與返回焦點的瀏覽器回歸，不能只斷言 selector 字串。 觸發：G4（見 ROADMAP）。 |
| 27 | [cb5d4e5](https://github.com/KKKKhazix/AIHOT/commit/cb5d4e533f85f07e9a417ac169d5225c5a69d2b8) | defer | 收藏頁再次掛載 Account 並允許子元素作本機提示，與 account 模組契約一起處理。 觸發：G3（見 ROADMAP）。 |
| 28 | [a9f7faa](https://github.com/KKKKhazix/AIHOT/commit/a9f7faa2ad966257421a2066e4d8253d127adfdc) | defer | 摘要與下架提示移除未經證實的來源方要求，屬跨 reader、report、starred 的文案調整，待版型更新一併驗收。 觸發：G4（見 ROADMAP）。 |
| 29 | [4468bb5](https://github.com/KKKKhazix/AIHOT/commit/4468bb56c29e90ac8c85206ef02074cb068e7823) | defer | Account 移除 children 介面，保留沒有帳號模組時的 localNote；是收藏帳號插口的最終介面。 觸發：G3（見 ROADMAP）。 |
| 30 | [1596c52](https://github.com/KKKKhazix/AIHOT/commit/1596c5248511b4b8f5252a228c6703040c37e515) | defer | recordRun 的預算熔斷以 failureKind=budget 記 skipped、保留錯誤並重拋；需驗 DB 狀態及一般錯誤仍 failed。 觸發：G2（見 ROADMAP）。 |
| 31 | [76e3b6e](https://github.com/KKKKhazix/AIHOT/commit/76e3b6ea52ac45ed3e2f30272514c83f1845b989) | reject | 只補工作失敗不加跨小時重試、桶生命週期負責備份清理的註解；現行 fork 沒有該額外排程，無行為變更可採納。 |
| 32 | [a22aba8](https://github.com/KKKKhazix/AIHOT/commit/a22aba8b4e76f720bf7c21545c984b586e74ae2a) | defer | 向量以 text_hash 共用、回執移除已另存的 data，新增並行索引 0140；需驗冷啟動、尺寸切換與同時購買只付一次。 觸發：G2（見 ROADMAP）。 |
| 33 | [991a36a](https://github.com/KKKKhazix/AIHOT/commit/991a36ad01e6c6a1eb668d34ea51110cce1fed0a) | defer | 移除飛書登入、改密碼唯一登入並擴充 previewPrincipal；會改授權與舊會話語義，不能與刪欄遷移拆開部署。 觸發：G3（見 ROADMAP）。 |
| 34 | [e01104c](https://github.com/KKKKhazix/AIHOT/commit/e01104cd61b61b356feeaf76a6c6e525232249d3) | defer | 移除飛書登入環境範例並補密碼升級說明；在 fork 尚支援飛書時不能先套，否則文件會說錯。 觸發：G3（見 ROADMAP）。 |
| 35 | [18d147c](https://github.com/KKKKhazix/AIHOT/commit/18d147cfe57bfb7de250712e985a3f362051b184) | defer | 0146／0147 刪 admin_sessions.auth_claims 與 admin_users.feishu_union_id；現行程式仍讀取，延後直到停用登入及資料升級驗收。 觸發：G3（見 ROADMAP）。 |
| 36 | [6c6c9ea](https://github.com/KKKKhazix/AIHOT/commit/6c6c9ea0aafa19438c8ce62b6e513f7e5b5c0324) | defer | 更正停用飛書的升級說明，列明 setup 會刪兩欄；依附登入移除，不能先改現行文件。 觸發：G3（見 ROADMAP）。 |
| 37 | [df278f6](https://github.com/KKKKhazix/AIHOT/commit/df278f6fa643d788a0358ed3a235cbfc1bfb33a5) | defer | 告警依 ADMIN 是否存在連到 runs 或 health，需連同無管理頁站點的登入與模組行為驗收。 觸發：G3（見 ROADMAP）。 |
| 38 | [84ed3a2](https://github.com/KKKKhazix/AIHOT/commit/84ed3a2c93db7a07f09b2ece9f25b19682a75b1b) | defer | preview 與 admin 都禁止共用快取，分開 devPrincipal，無管理頁時不承認舊管理員 session；依附灰頁授權新機制。 觸發：G3（見 ROADMAP）。 |
| 39 | [f8fe46e](https://github.com/KKKKhazix/AIHOT/commit/f8fe46e2ce52d0321a016d11d618ff3e19238dd1) | defer | 0149／0150 把 auth_method 約束限成 password NOT VALID；現行 fork 仍產生飛書會話，不能先裝約束。 觸發：G3（見 ROADMAP）。 |
| 40 | [594c7ce](https://github.com/KKKKhazix/AIHOT/commit/594c7ce876e9fe22bc6efe4f58e3d4583923e341) | reject | #420 只精簡上游 AGENTS 的歷史敘述與範例；fork 已用繁中單一指引與不同治理結構，不覆蓋本機政策。 |
| 41 | [a600101](https://github.com/KKKKhazix/AIHOT/commit/a60010148a4d41ace783a249926488ccf01148c2) | defer | S3 備份改為大檔 multipart，重試同一 part、失敗 abort、檢查 Complete 的 200 Error；需本機 multipart 假服務與備份恢復驗收。 觸發：G5（見 ROADMAP）。 |
| 42 | [2184557](https://github.com/KKKKhazix/AIHOT/commit/21845572fdad281b863458a19b9b8d9a61166233) | defer | 0151 suppress_original、EditorialPolicy 及圖片審核、翻譯／事件清理與舊帳本遮蔽跨公開出口；需整套 publication 及回執測試，不能零散採用。 觸發：G6（見 ROADMAP）。 |
| 43 | [a3e4349](https://github.com/KKKKhazix/AIHOT/commit/a3e43495d139dd6704e9039b9dabc360d3cd442d) | adopt | 代理 DNS 支援依序備援，預設仍釘住已驗公網 IP；明確 EGRESS_PIN_DNS=false 才把主機名交給代理，與警示及安全回歸成套採納。 |
| 44 | [fe9be05](https://github.com/KKKKhazix/AIHOT/commit/fe9be059a1d9f0d5daca6e5ea88f75918c18c4e1) | adopt | 採納本機代理與 DNS 假服務的備援、未釘 IP 及拒絕內網答案測試；對舊產品執行會失敗，修正後全過。 |
| 45 | [23d3882](https://github.com/KKKKhazix/AIHOT/commit/23d38826acd70fe9a40dabd1e116f840322b8cbf) | adopt | 與 a3e4349 同套採納：明載代理再次解析可能連入內網，只有代理自身不能連內網／本機時才可停用 pinning；預設不變。 |
| 46 | [700f7c7](https://github.com/KKKKhazix/AIHOT/commit/700f7c7006a27507da462b6f83b56b1389efaa57) | adopt | A／AAAA 用 allSettled 收齊，任何已回答的內網位址直接拒絕，不能被另一個查詢失敗帶去備援；獨立反向還原測試修前失敗。 |
| 47 | [209417b](https://github.com/KKKKhazix/AIHOT/commit/209417b0dd614460926ba7d96760794d07d83711) | defer | 新增模組管理頁唯讀授權、後台 layout、同事實卡片召回；備份排除原始分析事件、測試自建 PG 輔助器僅 Linux，需分邊界驗收。 觸發：G3（見 ROADMAP）。 |
| 48 | [6e4c692](https://github.com/KKKKhazix/AIHOT/commit/6e4c69246e810c354cced954dd97a59edf5444c0) | defer | 抽 adminPageAccess、後台導覽微調、統一北京日期及 avatar 尺寸；跨前後端並依附模組後台，隨同批驗收。 觸發：G3（見 ROADMAP）。 |
| 49 | [148d227](https://github.com/KKKKhazix/AIHOT/commit/148d227c9724fbc9cefd6d3010c30d0416fc1ef6) | defer | 新增公開網頁離線抽取比對腳本及三個 standalone 測試改名；待建立公開語料重播流程再採，避免只搬入口而無樣本證據。 觸發：G7（見 ROADMAP）。 |
| 50 | [909d8cb](https://github.com/KKKKhazix/AIHOT/commit/909d8cb2cf8c772837696f395f6ae7a6ba127048) | defer | 移除信源 first_party 讀寫與欄位契約，改依 tier／owner 身分；需與 seed 及 0153 一起驗舊庫升級。 觸發：G6（見 ROADMAP）。 |
| 51 | [ecc3cca](https://github.com/KKKKhazix/AIHOT/commit/ecc3ccab114c1f04fffb443ac6a979d360e9c300) | defer | 移除模組 agent 額外文字插口，回收超過一月且已送達的 hub 事件、保留未送達；需回收資料庫及出口回歸。 觸發：G2（見 ROADMAP）。 |
| 52 | [a977870](https://github.com/KKKKhazix/AIHOT/commit/a9778705efda8bd777b3dd566a7f5b1ece091c36) | defer | 私人告警經 hub 確認接管才消音、分開 privateNotice／privateOwner 狀態與恢復通知；需投遞去重、失敗及恢復測試。 觸發：G2（見 ROADMAP）。 |
| 53 | [541c0fa](https://github.com/KKKKhazix/AIHOT/commit/541c0fa63852f90234c9d276cdc181a1ba2dfb8c) | defer | 合併採集、分析、回饋與翻譯測試，保留 SIGTERM 子程序案例，抽取腳本逐頁記例外；測試搬移依附尚未採納的產品功能。 觸發：G8（見 ROADMAP）。 |
| 54 | [7b23e31](https://github.com/KKKKhazix/AIHOT/commit/7b23e312875384c5cb3a19b787c88e6b23b68645) | defer | seed 停止寫 sources.first_party；現行 fork 的來源規則及資料表仍有該欄，須與 909d8cb、0153 一起更換。 觸發：G6（見 ROADMAP）。 |
| 55 | [cee2dbb](https://github.com/KKKKhazix/AIHOT/commit/cee2dbb2ae5283bae2c562366c755ec9f29443bf) | defer | 0153 刪 first_party、移除管理原因提示預設值及 SIGN_IN_HOME 調整；不能先刪仍讀寫的欄位。 觸發：G6（見 ROADMAP）。 |
| 56 | [adf92d1](https://github.com/KKKKhazix/AIHOT/commit/adf92d1eacd050454bdd4a396cec92d448cbb6d0) | defer | 0154–0158 刪故事、事實與回執／投遞舊欄，事件證據清空也清綜述、存報告回傳是否寫入；需有資料升級與對應業務測試。 觸發：G6（見 ROADMAP）。 |
| 57 | [eff4ce9](https://github.com/KKKKhazix/AIHOT/commit/eff4ce93ccd3d0ed185cbeee55d2809914bc31d7) | defer | 圖片代理簽章移除 Accept 格式後綴，驗證僅剩已簽 mode／期限；需舊網址相容及竄改拒絕測試，不能只移植測試標題。 觸發：G5（見 ROADMAP）。 |
| 58 | [7c3d557](https://github.com/KKKKhazix/AIHOT/commit/7c3d55746da566609a168f4ad8274d7ba339a81b) | defer | 0162–0165 刪 stories.latest、story_digests.latest、reports.model／origin 並修測試；需先確認現行讀寫全部移除及升級資料一致。 觸發：G6（見 ROADMAP）。 |
| 59 | [816159b](https://github.com/KKKKhazix/AIHOT/commit/816159bffb906fc6b3bf0f4e0881062936793718) | defer | 移除 motion、改 Presence 動畫，抽靜態 ETag 比對、啟用 noUnusedLocals 並刪過期插口；要連鎖檔與全站動畫一起驗。 觸發：G4（見 ROADMAP）。 |
| 60 | [3c44d42](https://github.com/KKKKhazix/AIHOT/commit/3c44d42a974b10fc5660bf1d9905ecd551dac33a) | defer | 整併多個產品測試到既有功能檔，新增本機字型備份行為案例；搬移前須先完成相關產品更新並核對測試數與行為覆蓋。 觸發：G8（見 ROADMAP）。 |
| 61 | [ed4a838](https://github.com/KKKKhazix/AIHOT/commit/ed4a83840778b8f1f2ace929461d7fc4ad7f751a) | defer | RSS／Atom 的媒體從清理後 HTML 抽取，排除輪播促銷圖片；需公開真實訂閱樣本前後對照，保留 enclosure 與正常媒體。 觸發：G7（見 ROADMAP）。 |
| 62 | [6777de9](https://github.com/KKKKhazix/AIHOT/commit/6777de9719da0183346f9fea64287f40ba71f02f) | defer | 網頁 manifest 移除 motion，另測歸組可見 6000 字以後證據；前者依附動畫移除，後者依附歸組文字更新，不單套 manifest。 觸發：G4（見 ROADMAP）。 |
| 63 | [7fa763d](https://github.com/KKKKhazix/AIHOT/commit/7fa763dfd959eb5bafff24c594d3c0884c6923ab) | defer | 移除 motion／framer-motion 鎖檔；目前網頁還引用 motion，先移鎖檔會破壞 npm ci，待動畫移除一起更新。 觸發：G4（見 ROADMAP）。 |
| 64 | [fe46be3](https://github.com/KKKKhazix/AIHOT/commit/fe46be3e4e4be72845f610bd0640eeb546315d58) | defer | 帳本停止讀寫 visible_at、移除 rawDropKeys 設定入口；須確認上下游呼叫與既有設定清理後再執行刪欄。 觸發：G6（見 ROADMAP）。 |
| 65 | [04a3d42](https://github.com/KKKKhazix/AIHOT/commit/04a3d427371b8e0373dea6a19e58f5e15bdb4e43) | defer | 0169 刪 selected_ledger.visible_at 及相依索引；現行 appendLedger、adminChain 仍使用，禁止只先套遷移。 觸發：G6（見 ROADMAP）。 |
| 66 | [0c6f287](https://github.com/KKKKhazix/AIHOT/commit/0c6f287fc753504213332c137fa597e3bd94b40f) | reject | SocialData 暫時改成全部走代理，已被 88b114d 的 direct-first 取代；不採用過渡路由，避免新增代理失敗面。 |
| 67 | [7b446b1](https://github.com/KKKKhazix/AIHOT/commit/7b446b1008d832ee25084f8e7baf62ce493f40c3) | defer | 模型圖片輸入把任一邊小於等於 10px 的圖片補白到 11px，保留證據而不改讀者快取；依附 2184557 的完整圖片審核入口。 觸發：G6（見 ROADMAP）。 |
| 68 | [4c6e9e1](https://github.com/KKKKhazix/AIHOT/commit/4c6e9e17068d16ef883124f51acd0e5aeb265ec2) | defer | sanitizeBody 移除 section 下的 Related Stories 卡片，保留 Related work；須真實頁面及 RSS 媒體前後比較再採。 觸發：G7（見 ROADMAP）。 |
| 69 | [88b114d](https://github.com/KKKKhazix/AIHOT/commit/88b114d7efbcdee17c3fc4d2e29c27672178e10a) | defer | SocialData direct-first 只在首個連線逾時且 request 尚未開始時切代理；需驗 421 後失敗不重放付費請求及路由回歸。 觸發：G5（見 ROADMAP）。 |
| 70 | [5bd2965](https://github.com/KKKKhazix/AIHOT/commit/5bd2965508252e66d663118f0fecc9dd9c3185be) | defer | 事件可索引條件、文章事件連結、主題標籤與 phone 導覽一起調整；涉及 fork 的 Phone view transition 與 outline 分岔，需保留後驗收。 觸發：G9（見 ROADMAP）。 |
| 71 | [e0554b6](https://github.com/KKKKhazix/AIHOT/commit/e0554b64aa3a75dcc29e2b4dac570241ae532b35) | defer | 事件主頁取代多來源文章作索引、Google News 與 topic archive SEO／推送更新；Baidu 路徑需保留 fork HTTPS 及次數上限防線。 觸發：G9（見 ROADMAP）。 |
| 72 | [529d3e3](https://github.com/KKKKhazix/AIHOT/commit/529d3e363bd6382d881e37eef6f7480dd0467b2e) | defer | stableJson 移到同步契約、canonicalIp、管理內容審計與退役模型計價修正；需同步契約及資料庫價目／來源回歸成套驗。 觸發：G3（見 ROADMAP）。 |
| 73 | [9cffdf6](https://github.com/KKKKhazix/AIHOT/commit/9cffdf6daf893c3182ca8fade616dcb52783c118) | defer | 0170–0174 新增報告期號、綜述版本、自動釋放與 feedback surface；報告穩定 section key、UI 與通知共 69 檔，需新舊庫及所有報告出口驗收。 觸發：G9（見 ROADMAP）。 |
| 74 | [eebe155](https://github.com/KKKKhazix/AIHOT/commit/eebe1559c3f4611dd541487e96ca1cd6c36dd0e2) | defer | CI PostgreSQL 公鑰與 apt 下載加有限重試；目前 Actions 被停用，恢復後再檢查 Linux job，保留 713caec push 篩選。 觸發：G8（見 ROADMAP）。 |
| 75 | [4c0de98](https://github.com/KKKKhazix/AIHOT/commit/4c0de98f6c134c667518ceb67324c3b72b612f62) | defer | 模型主請求逾時測試增加 timeout 並讓備援完成；屬測試時序調整，待本工作樹重現該測試逾時再改，避免無證據放寬時間。 觸發：G8（見 ROADMAP）。 |
| 76 | [1f746d6](https://github.com/KKKKhazix/AIHOT/commit/1f746d61b7edafedca91f13df5b4e30c40494bcc) | defer | 分類改正清來源欄導讀但保留目標欄原本有效導讀；需資料庫回歸確認日／週／月報及 fork 現行欄位契約。 觸發：G9（見 ROADMAP）。 |
| 77 | [6fa2845](https://github.com/KKKKhazix/AIHOT/commit/6fa28457689abe26115d5c2677f43e8de946422a) | defer | 區分服務商 HTTP 5xx 與出網故障，只有服務商問題降成 daily 通知；需驗 4xx、混合故障及門檻計數。 觸發：G2（見 ROADMAP）。 |
| 78 | [6f96144](https://github.com/KKKKhazix/AIHOT/commit/6f96144c909109622f9c226bf9ae8fd4905f27ec) | defer | 集中微信 URL 識別、物料身分解析與公開 article list predicate；改 agent／items／v1 時須保留 timelineAt 及 Markdown 跳脫分岔。 觸發：G9（見 ROADMAP）。 |
| 79 | [13f8602](https://github.com/KKKKhazix/AIHOT/commit/13f8602450a065b697ed90372b64d25707e85d2a) | defer | 事實合併回歸加驗連續兩次 consolidate，依附交易與合併行為，不單搬測試造假綠燈。 觸發：G1（見 ROADMAP）。 |
| 80 | [cf0b73e](https://github.com/KKKKhazix/AIHOT/commit/cf0b73e8effc97093a81858fd08ca27a10808f0c) | defer | 抽取評測只把公開列表頁誤當文章計為問題，避免期望標題影響判準；與 148d227 的樣本工具一起驗。 觸發：G7（見 ROADMAP）。 |
| 81 | [6aa93e9](https://github.com/KKKKhazix/AIHOT/commit/6aa93e992678b895e676e88dccf37f2bc41c7841) | defer | 新增測試時鐘債務清冊與靜態檢查，依賴 repo 內 SourceDebt／clock helper；待既有時鐘夾具清理及完整測試後採。 觸發：G8（見 ROADMAP）。 |
| 82 | [24a8147](https://github.com/KKKKhazix/AIHOT/commit/24a81472f0fae7c87f703aeec1f215ca92fc9d37) | defer | 設計字級、pagePathname 的 document／data 同義、phone/sidebar 導覽集中及架構檢查共 79 檔；需多配置與 WebKit 回歸。 觸發：G4（見 ROADMAP）。 |
| 83 | [9139ad3](https://github.com/KKKKhazix/AIHOT/commit/9139ad33873a2acc81ebdaec66cf1371d408f57a) | defer | 44 檔測試改為可觀察行為及 pollFor，包含 fork 加強的 navigation／outline；需確認沒有削弱 router／DOM 與捲動防線再整合。 觸發：G8（見 ROADMAP）。 |
| 84 | [1e7cc02](https://github.com/KKKKhazix/AIHOT/commit/1e7cc022fd8bef3bded929dcf9d1f919e08c11de) | defer | 43 檔字級改用共用設計尺度，不能只改少數 class 造成視覺不一致；待完整前端版型比較。 觸發：G4（見 ROADMAP）。 |
| 85 | [dd81a99](https://github.com/KKKKhazix/AIHOT/commit/dd81a99eb7842a5f830b6797cd4925208b7bbd2e) | defer | 導航回歸改驗可見 token 色彩與閱讀位置卡片、清理 presentation assertion 債務；保留 fork URL/router／DOM 及 pageerror 斷言再驗 WebKit。 觸發：G8（見 ROADMAP）。 |
| 86 | [f3d7c29](https://github.com/KKKKhazix/AIHOT/commit/f3d7c2964f7febc270813f9577593708d32aabab) | defer | 0184 用資料庫約束強制 suppress_original 只能 summary 且不 syndicate，簡化公開查詢並補 source tier；需 0151 及遮蔽全部出口一起驗。 觸發：G6（見 ROADMAP）。 |
| 87 | [b6bb047](https://github.com/KKKKhazix/AIHOT/commit/b6bb047a43b8c273464510fac233e89257baae80) | defer | 只改媒體 HTTP 測試名稱以反映 eff4ce9 不再依 Accept 分流，依附簽章遷移而非獨立缺陷。 觸發：G5（見 ROADMAP）。 |
| 88 | [2776be6](https://github.com/KKKKhazix/AIHOT/commit/2776be6f202ba085308108e1c8badf01389d242c) | defer | 只有服務商自身錯誤達門檻才降噪，少量 5xx 不能掩蓋大批出網錯誤；依附 6fa2845 的告警分類。 觸發：G2（見 ROADMAP）。 |
| 89 | [34646eb](https://github.com/KKKKhazix/AIHOT/commit/34646ebfd213c9b95ceeda4cf50e0bb625d6e564) | defer | 繼續刪除字級／斷言 debt 及改 cache、private route 測試，應與新架構規則和前端版型一起驗。 觸發：G8（見 ROADMAP）。 |
| 90 | [aec61a4](https://github.com/KKKKhazix/AIHOT/commit/aec61a4cca18ff1521f4d32040ba5ee1750d9017) | reject | 新增日文 README 與語言切換入口；本 fork 主入口為繁中且 README 已改 fork 部署說明，上游日文原文不能直接作本 fork 文件。 |
| 91 | [6f01a81](https://github.com/KKKKhazix/AIHOT/commit/6f01a81223f590742163914e5ec9188cf4d15449) | defer | 讀者文案、topic blurb、標籤 displayTag 與 RSS／Agent 說明跨出口更新，包含 industry 自訂分類；須先確認站點文案需求並保留 timelineAt 分岔。 觸發：G9（見 ROADMAP）。 |
| 92 | [a1fbcb4](https://github.com/KKKKhazix/AIHOT/commit/a1fbcb431fa1573b930447fddb0e19c8819a7132) | defer | 告警先收集 coverage 再濾被大故障涵蓋的 source failures，避免重複告警；需驗混合服務商故障、恢復與未涵蓋來源仍通報。 觸發：G2（見 ROADMAP）。 |
| 93 | [42e990f](https://github.com/KKKKhazix/AIHOT/commit/42e990fad199f640fcf5d457acb6f2b6ba711b01) | reject | 長文新增 isSubstantiallyChinese 但只改翻譯入口的過渡方案，會讓翻譯與閱讀出口判斷不同；由 8261fc2 統一方案取代。 |
| 94 | [8261fc2](https://github.com/KKKKhazix/AIHOT/commit/8261fc24e9aa0c1d446f1c97d92ec72ab0c4d5e5) | defer | 把長文 Han 比例規則併回 isChineseText，統一翻譯與所有閱讀出口；需含英中日韓的真實語料及既有短字串回歸。 觸發：G7（見 ROADMAP）。 |
| 95 | [645e4db](https://github.com/KKKKhazix/AIHOT/commit/645e4db718bb128facc157a47ccc6a0b410e1763) | defer | 長文 Han 比例由 30% 改 10%，避免含大量產品英文名的中文被誤翻；必須與 8261fc2 及混語語料一起校驗。 觸發：G7（見 ROADMAP）。 |
| 96 | [005bd78](https://github.com/KKKKhazix/AIHOT/commit/005bd78650bd3a6b20cac2b584aca6ab3b7f38e1) | defer | 取消事實／事件標題硬截斷、統一空白、只在證據改動時 dirty digest；依附 EditorialPolicy 與事件重寫入口，需長標題及綜述失效回歸。 觸發：G6（見 ROADMAP）。 |
| 97 | [4e03f81](https://github.com/KKKKhazix/AIHOT/commit/4e03f818ebe5ee816a3bb52a0d2c42ceab0fef97) | defer | 新增側欄 MoreMenu 收納外觀與字型並調整 module 插口；須鍵盤、焦點、手機版與目前側欄相容驗收。 觸發：G4（見 ROADMAP）。 |
| 98 | [9bad98b](https://github.com/KKKKhazix/AIHOT/commit/9bad98bab7d2e7db34560a5373915a5a6a39539e) | defer | FontSelect 共用選項、MoreMenu 精簡及「我的」字型入口更新；與 4e03f81 一起驗儲存／無權寫入及切換。 觸發：G4（見 ROADMAP）。 |
| 99 | [65c6550](https://github.com/KKKKhazix/AIHOT/commit/65c6550e7f5ac571207e1699051fe3a517f301d8) | defer | 新增 ENGLISH=null 與 Babel parser，為英文版準備設定；尚未要求雙語站，需連同後續 104 檔路由與翻譯契約驗。 觸發：G10（見 ROADMAP）。 |
| 100 | [16c433f](https://github.com/KKKKhazix/AIHOT/commit/16c433f8d853740a66ef050e11a08f9ad2474f78) | adopt | JSON itemsPath 失敗時顯示停住層級、最多八個鍵與截短上游 message／msg／error；本機錯誤包體測試修前失敗、修後通過。 |
| 101 | [1dcf1db](https://github.com/KKKKhazix/AIHOT/commit/1dcf1db770029c0282f39ca08cf4afc86d224176) | adopt | 修正新診斷在 null／純量層呼叫 Object.keys 的錯誤；先在 16c433f 版本重現 null 包體 TypeError，再套修正通過。 |
| 102 | [59c3d52](https://github.com/KKKKhazix/AIHOT/commit/59c3d526b79329eafd6e01159b38427543f15ddb) | defer | 104 檔加 /en 文案、連結、SEO、industry English 與 taxonomy 語言契約；需英文內容需求確認、導覽及全出口語言測試，保留 fork 導覽補丁。 觸發：G10（見 ROADMAP）。 |
| 103 | [bc57d79](https://github.com/KKKKhazix/AIHOT/commit/bc57d793fb4d3e35fbe908d59514664b3539b0e7) | defer | 修英文版側欄／TabBar、分欄與 sectionLabelIn 優先穩定 key；沒有 59c3d52 的雙語介面不可單獨套用。 觸發：G10（見 ROADMAP）。 |
