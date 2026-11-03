# 上游審查紀錄

最後審查：2026-11-03（commit 水位 `41cee09`，PR 水位 #332、issue 水位 #320；PR #323 以 head／state 追蹤）

本檔只記可執行結論。機器水位與 open PR head SHA 放在 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。相同 SHA、狀態與庫存不重審；任一項變動才重新評估。

## 2026-11-03 整樹採納（`79d962e..41cee09`）

已將 fetch 確認的 main `41cee09f70518fdcacdc307dcba58d635505bb41` 差量以逐檔三方合併採納：48 個 commit、230 個路徑、+5242／-1813，無文字衝突。下方 2026-11-02 的 40 筆 commit 裁決是歷史快照；其中 defer 均已隨本次整樹採納，三筆依賴 skip 已由上游安全版本涵蓋。PR #263 的 revision-checked 全文譯文入口與 #291 的分享圖補充字體一併採納。

- 分岔依 `DIVERGENCE.md` 保留：限流表全站計數、Markdown 跳脫、prefix 替換、手機導航、目錄捲動、測試 cleanup 與 `timelineAt`。`http-policy.ts` 的舊 `/sources` 規則已移除，prefix 回歸改用測試模組宣告的規則。
- 上游 `zod` 4.6.6 已符合原登記的 ≥4.6.6 收斂條件；`fast-uri`、`undici` 也已有安全修補，兩個 manifest 與 lock 改採上游，移除三列依賴分岔。
- 依保留既有檔案的限制，`day-header-year.test.ts`、`report-year.test.ts`、`sign-in-paths.standalone.test.ts` 留存；上游已把同類斷言併入既有測試，這三個路徑在新基準下屬 fork 自有測試。
- 新增 7 個遷移：0090、0091、0092、0105 是新增欄位；0121、0122、0123 是 `CONCURRENTLY IF NOT EXISTS` 索引。均為新檔、每檔一條語句，沒有修改已發布遷移。環境無可用本機 `_test`／`_ci` 資料庫設定、PostgreSQL 工具或服務；遷移與資料庫整合測試未驗證，沒有建立或連線其他庫。
- 隱藏內容掃描涵蓋 48 個 commit 各自的新增行及 PR #323：行內 ≥40 空白、>400 字元行、eval／new Function／globalThis.require、長 base64／hex、零寬與雙向字元。命中僅四條已判讀的長行（Picture sizes、部署說明、測試 SVG）與 HMAC `digest("base64url")`，均為正常內容，無隱藏載荷。
- Co-authored-by 致謝：Claude Opus 5.5 <noreply@anthropic.com>、cunyikang <cunyikang@qq.com>、FelixFtch <143968032+FelixFtch@users.noreply.github.com>、granary17 <98481815+granary17@users.noreply.github.com>。

| 新增 commit | 裁決與理由 |
|---|---|
| `f88621f` | adopt：微信文章身分與存量查找、兩個並行索引、管理內容路徑與模組管理邊界。 |
| `9059707` | adopt：第三個微信 externalId 查找索引，補足短網址先入庫的去重。 |
| `e6e3c68` | adopt：回饋來源與信箱封禁、通知接收者設定及其回歸。 |
| `2c71b68` | adopt：一致正文抽取、aside／layout 類別處理、純文字替代正文入口與日期解析回歸。 |
| `ce97b4d` | adopt：依讀者卡片比較同新聞、事實合併、回聲來源與交易內發布。付費判斷仍走既有模型與回執。 |
| `29aa1ab` | adopt：事實合併補正與事件／新聞價值回歸。 |
| `e05f58a` | adopt：帶明確錨點的 Markdown changelog 解析及回歸。 |
| `41cee09` | adopt：架構測試將共用測試支援檔明確排除出產品模組邊界檢查。 |

| 新增 PR | 裁決與重新審查條件 |
|---|---|
| #323（open，head `50ec992`） | 不併入 main 整樹採納：獨立的 Menu 鍵盤導航／焦點修復，觸及 Menu 與 item-copy 測試，不覆蓋 fork 分岔；已讀完整 diff 並掃描，未合併的修復超出本項 main 範圍。以 `monitored` 追蹤 head／state，變動即重審。 |
| #324、#325、#326、#327、#329、#330、#331、#332 | merged，分別對應以上八個 commit，全部採納。 |

issue #320 之後無新增，issue 水位不變。


### 本機驗證（2026-11-03，整合來源 `41cee09`）

- Node.js 24.22.1：`tools/dev_check.ps1` exit 0（typecheck、SSR build、網頁 65/65、分岔契約 9/9、freshness 契約 2/2）；`npm run test:standalone` 249/249，`npm audit --package-lock-only` 0 vulnerabilities，`check_upstream_updates.py --strict` exit 0。
- HTTP cookie 回歸在舊實作為 `true !== false`，採納後 5/5 fork 安全回歸通過。分岔檢查器新增回歸：基準新增檔存在但未追蹤時，舊檢查器誤報刪除；改依 Git filtered blob 比對後，相同內容與不同內容兩個案例皆通過，實際 15 列登記吻合。
- 公開樣本只下載一次後由 localhost fake server 重播：Google Research RSS 100 筆、Hugging Face RSS 895 筆，以及各自最新一篇原文；以 load hook 載入起點 `92d91d7` 原始碼，與採納後比對。995 筆的 URL、標題、日期、摘要、正文與狀態完全相同；兩篇正文分別 9424、9686 字元，SHA-256 與日期也完全相同。這項比對未呼叫模型或連線資料庫。
- 預設 Node.js 26.12.1 的 standalone 為 248/249：既有 secure-proxy fixture 把 IP 設為 SNI，Node 26 拋 `ERR_INVALID_ARG_VALUE`；同一程式與測試在專案指定的 Node 24.22.1 通過。沒有修改 TLS 驗證或放寬斷言。
- `git diff --check` 唯一提示為上游原有的 `tests/collection-body-preservation.test.ts:73` 檔尾空行；保留上游內容，沒有為格式建立額外分岔。

## Main commits

- `cc66cce` 以前：2026-10-03 已整批採納（#89–#91，另有安全修補 `e4478cb`、`879afa3`、`14fe1da`、`31fa181`）。
- `cc66cce..ce83484`（124 個 commit，PR #92–#269）：2026-10-25 **整樹採納**。做法是把上游 `cc66cce..ce83484` 的差量以 3-way 套到 fork 樹，再重做分岔檔。上游此段包含 4.0.0 引擎／站點分層（`site/`、`modules/`，#92、#95）、模型榜與 Codex 重置監控移出框架、資料庫遷移約定、安全邊界（#197、#223 的內網放行與雲端中繼位址拒絕）、`sanitize-html` 2.18.x／`fastify`／`undici` 安全版本（`b3998dc`）、日期解析與採集修正。
- `ce83484..79d962e`（3 個 commit，PR #273–#275，10 檔 +179／−16）：2026-10-28 **整批採納**，3-way 套用無衝突（這 10 檔都不在分岔表內）。
  - `aa8e5b1`（#273）：告警可改走群組自訂機器人 Webhook（`FEISHU_ALERT_WEBHOOK_URL`），600 ms 間隔、18 000 位元組分段；只在 `FEISHU_INTERNAL_ENABLED=true` 且設了該變數時生效，本 fork 預設關，行為不變。回應了 #271。
  - `04427b9`（#274）：日報切換 chip、前後日連結與跟進徽章跨年時帶年份（`format.ts`、`ReportPaper.tsx`＋`report-year.test.ts`）。
  - `79d962e`（#275）：`extract.ts` 的登入頁路徑正則補 `sign_in`、`log_in`、`sign_up`、`wp-login.php` 與 `.php/.aspx/.html/.jsp` 副檔名（＋`sign-in-paths.standalone.test.ts`）。
  - 判準八：對 `ce83484..79d962e` 差量掃「空白夾程式」（`\S\s{40,}\S`）、`eval(`／`new Function(`／`globalThis`、120 字以上 base64，0 命中。
- 判準八（隱藏內容）：對整份 `cc66cce..ce83484` 差量掃描「空白夾程式」「超長單行」「`eval`／`new Function(`」「掛 `require`」「長 base64／hex」，0 筆命中。

## 本 fork 先前移植、已由上游自行解決（分岔列已刪）

| 原移植 | 上游現況 |
|---|---|
| PR #79 `tests/architecture.test.ts` 路徑正規化 | 上游測試已用 posix 路徑（`path.posix.relative`），Windows 缺陷不存在；採上游版。 |
| PR #83 `summaryIsBody` | 上游 `rss.ts` 已有 `source.config.summaryIsBody === true`，並寫入 `docs/sources.md`；採上游版。本 fork 的 `tests/rss-summary-body.test.ts` 保留。 |
| PR #85 `_aihot.initialBackfillOnly` | 上游以 `50b562b`（#105）內建等效行為：首次匯入後只收首次匯入前 48 小時內與之後的條目，不需 opt-in 開關；`collect.ts`／`config-keys.ts`／`docs/sources.md` 採上游版，移除 fork 的開關。 |

## 本 fork 保留的分岔

以 [`DIVERGENCE.md`](DIVERGENCE.md) 的逐檔登記與收斂判準為準。目前除 README／AGENTS 繁中化、`CLAUDE.md` 刪除，也保留產品碼與測試分岔；依賴補丁已於 2026-11-03 隨上游安全版本收斂：

- 導航與瀏覽器測試：文章目錄邊界鍵盤捲動、phone card 停用 view transition，以及瀏覽器啟動失敗時的測試清理與 router／DOM 一致性回歸。
- 安全修正：Agent Markdown 連結文字跳脫反斜線、prefix 轉址將路徑當資料替換、登入嘗試表修剪時保留全站計數。逐筆判讀與理由見 [`DECISIONS.md`](DECISIONS.md) 第 9 條。

上游修改對應檔案時，依分岔表比對行為與回歸證據；只有包含等價修正才移除 fork 補丁與登記列，不以產品碼零分岔為前提。

## 2026-11-02 上游積壓審查（commit `79d962e..6e0cfaf`；PR #279–#322；issue #276–#320）

換上游檢查器正本後 `--strict` 回 exit 1，本節逐筆審完 40 個 commit、34 筆 PR、10 筆 issue。**commit 水位刻意不推進**：`tools/check_divergence.py` 以 `reviewed_through` 為基準，要求工作樹與該基準的差異恰等於 `DIVERGENCE.md` 的登記；基準推到 `6e0cfaf` 而樹沒有同步，就會有約 200 個檔案被當成未登記分岔。因此 commit 軸只能是「整樹採納」或「不推進」，不能只挑幾筆。本輪沒有採納，理由與工作量如下。

### 為什麼這輪不做整樹採納

- 規模：`git diff --stat 79d962e upstream/main` 為 212 個檔、+4107／-1728；其中 `packages/backend` 65 檔、`apps/web` 59 檔、`apps/api` 10 檔，另有 4 個資料庫遷移（`0090_source_selection_class`、`0091_feedback_kind`、`0092_feedback_idea`、`0105_source_uses`）。
- 動到產品主流程：告警交給自動處理服務（`operations/alerts.ts` +240 行）、信源類別門槛與採集（`sources/collect.ts`）、通知（`notify/agent.ts`、`notify/feishu.ts`）、事件歸組（`events/group.ts`）、全部動態只列 40 分以上、新增回饋類型與信源用途資料表。這些是行為變更，需要 PostgreSQL 完整驗收（`DATABASE_URL` 整合測試）與遷移演練，不是一個小時的工作。
- 與分岔檔重疊：上游差量碰到 DIVERGENCE 已登記的 `apps/api/src/routes/admin-auth.ts`（-48／+，與 fork 的全站 `all` 計數補丁同檔）、`apps/web/app/routes/item.tsx`（68 行，與目錄邊界鍵盤補丁同檔）、`apps/web/app/features/feed/FeedItem.tsx`、`packages/contracts/src/http-policy.ts`（上游刪掉了 `/sources` 的 prefix 規則那一行，但第 83 行的 `location.replace("*", …)` 程式仍在，fork 的 `replaceAll` 補丁修的是程式而非規則，分岔列不能因此刪），另有 `package.json`／`package-lock.json`／`README.md`／`AGENTS.md`。每一個都要判讀後重做補丁。
- 上一輪（124 個 commit）的做法是整樹 3-way 套用後重做分岔檔；本批同樣適用，但需要排一個完整工作段，已列入 [`ROADMAP.md`](../ROADMAP.md) 近期表。

掃描（判準八）：對每個 commit 的完整 diff 新增行掃 `eval(`／`new Function(`／`globalThis.require`、零寬／雙向控制字元、120 字元以上 base64／hex、行內 40 空白以上夾內容，另加 400 字元以上單行。只有 `c9e68c3`（`apps/web/app/routes/hot.tsx`、`docs/deploy.md`、`tests/media-performance.test.ts`）與 `a846c43`（`ReportPaper.tsx`）有超長單行，已讀過：是 Picture 的 srcSet／sizes 字串、Nginx 與備份說明文件，以及 sharp 測試的內嵌 SVG，非隱藏內容；其餘 0 命中。PR #263 原追蹤的 head `656564f` 已被作者改成 `7dd34dc` 後合併為 `823db74`，該 commit 同樣掃描 0 命中。

### 相關既有追蹤項的狀態變更

- PR #263（全文譯文導入入口）：**2026-11-01 已合併**（head `656564f` → `7dd34dc`，合併 commit `823db74`，`translate.ts`＋測試共 +34／-3）。先前「暫不移植」的理由（上游未收下）不再成立；改為隨整樹採納一併帶入，ROADMAP 中期列「重評全文譯文入口」的觸發條件已成立。
- issue #261：上游 closed（completed），隨 #263 處理。issue #267：上游 closed，由 #291（`7265071`、`ef2aaa6`、`0b52749`）實作站點補充字體；ROADMAP「處理分享圖缺字」的觸發條件之一（上游出現實作）已成立，隨整樹採納。

### Commit 軸（40 筆：37 defer、3 skip）

| Commit | 檔數 | 裁決與理由 |
| --- | ---: | --- |
| `d86c120` | 2 | **defer**：獨立小修（admin-auth.ts +cookie Secure 按請求協議判斷，回應 issue #278）；該檔是 DIVERGENCE 分岔檔，需與 fork 的「保留全站 all 計數」補丁合併 |
| `846e6f3` | 1 | **defer**：文件，隨 d86c120 |
| `c535666` | 2 | **defer**：隨 d86c120 |
| `0c75802` | 1 | **defer**：獨立小修（`http-fetch.ts` 單檔，P-256 重試，回應 issue #282）；不在分岔檔內 |
| `fd54d04` | 1 | **defer**：隨 0c75802（只對 GET／HEAD 重放） |
| `5b2aaaa` | 1 | **defer**：隨 0c75802（只認 refused key share） |
| `a9ab0c8` | 2 | **defer**：獨立小修（`jina.ts` 與測試，列表頁收費記錄不再以時鐘當編號） |
| `c9e68c3` | 129 | **defer**：整樹採納時一併帶入；掃描命中新增行超過 400 字元（apps/web/app/routes/hot.tsx, docs/deploy.md, tests/media-performance.test.ts），已讀過新增的長行：JSX srcSet／sizes 字串、Nginx 設定範例、備份說明與 sharp 測試用內嵌 SVG，皆為正常內容，非隱藏內容，不拒收 |
| `4d50183` | 1 | **skip**：已具備：fork lock 的 `fast-uri` 為 4.2.3／3.1.9，與上游相同 |
| `7432095` | 4 | **defer**：「同步引擎」引擎同步包（4 檔，主要在 packages/backend、tests/agent-wake.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `598289e` | 16 | **defer**：「同步引擎」引擎同步包（16 檔，主要在 packages/backend、apps/web），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `c3a83e0` | 26 | **defer**：「同步引擎」引擎同步包（26 檔，主要在 apps/web、packages/backend），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `85a1632` | 3 | **skip**：已具備且更新：fork 的 `zod` 為 4.6.7（安全修補 GHSA-mrhx-c7xc-m3w5），高於上游 4.6.6；DIVERGENCE 列待上游追上 4.6.7 再刪 |
| `0659e91` | 8 | **defer**：「同步引擎」引擎同步包（8 檔，主要在 packages/backend、tests/source-uses.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `eada774` | 2 | **defer**：「同步引擎」引擎同步包（2 檔，主要在 packages/backend、tests/source-uses.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `77cdb36` | 2 | **defer**：「同步引擎」引擎同步包（2 檔，主要在 packages/backend、tests/jina-listing.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `37318e0` | 10 | **defer**：「同步引擎」引擎同步包（10 檔，主要在 packages/backend、apps/api），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `9460570` | 1 | **defer**：「同步引擎」引擎同步包（1 檔，主要在 packages/backend），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `a846c43` | 12 | **defer**：整樹採納時一併帶入；掃描命中新增行超過 400 字元（apps/web/app/features/report/ReportPaper.tsx），已讀過新增的長行：JSX srcSet／sizes 字串、Nginx 設定範例、備份說明與 sharp 測試用內嵌 SVG，皆為正常內容，非隱藏內容，不拒收 |
| `877813d` | 3 | **defer**：「同步引擎」引擎同步包（3 檔，主要在 packages/backend、tests/agent-wake.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `65fe2f1` | 5 | **defer**：「同步引擎」引擎同步包（5 檔，主要在 packages/backend、apps/api），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `edfa18f` | 21 | **defer**：「同步引擎」引擎同步包（21 檔，主要在 packages/backend、apps/web），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `ce9a504` | 12 | **defer**：「同步引擎」引擎同步包（12 檔，主要在 packages/backend、apps/web），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `4be9cc0` | 1 | **defer**：「同步引擎」引擎同步包（1 檔，主要在 site/site.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `823db74` | 2 | **defer**：「同步引擎」引擎同步包（2 檔，主要在 packages/backend、tests/translate.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `7265071` | 3 | **defer**：「同步引擎」引擎同步包（3 檔，主要在 docs/customize.md、packages/backend），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `ef2aaa6` | 3 | **defer**：「同步引擎」引擎同步包（3 檔，主要在 packages/backend、tests/media-performance.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `0b52749` | 1 | **defer**：「同步引擎」引擎同步包（1 檔，主要在 tests/media-performance.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `fe530c0` | 1 | **skip**：已具備：fork lock 的 `undici` 為 7.30.1，與上游相同 |
| `05d700d` | 2 | **defer**：「同步引擎」引擎同步包（2 檔，主要在 README.md/、docs/deploy.md），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `ed628d9` | 7 | **defer**：「同步引擎」引擎同步包（7 檔，主要在 apps/web、apps/api），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `77cdcbf` | 6 | **defer**：「同步引擎」引擎同步包（6 檔，主要在 .github/workflows、AGENTS.md/），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `f6b9dd2` | 2 | **defer**：「同步引擎」引擎同步包（2 檔，主要在 packages/backend、tests/owner-alerts.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `9d7b6a6` | 4 | **defer**：「同步引擎」引擎同步包（4 檔，主要在 packages/backend、apps/web），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `d4e0374` | 7 | **defer**：「同步引擎」引擎同步包（7 檔，主要在 packages/backend、tests/agent-wake.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `027d50a` | 7 | **defer**：「同步引擎」引擎同步包（7 檔，主要在 apps/api、apps/web），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `38d130f` | 7 | **defer**：「同步引擎」引擎同步包（7 檔，主要在 apps/web、packages/backend），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `46a9334` | 3 | **defer**：「同步引擎」引擎同步包（3 檔，主要在 packages/backend、tests/source-health.test.ts），與其他同步包相依，不能單挑；整樹採納時一併帶入 |
| `5c10a6e` | 2 | **defer**：獨立小修（`content/materials.ts`，列表源末尾實時計數不觸發內容修訂，回應 issue #314） |
| `6e0cfaf` | 4 | **defer**：小修但跨 `admin/models.tsx`、`contracts/admin.ts`（回應 issue #319） |

### PR 軸（34 筆：30 defer、4 skip）

| PR | 狀態 | head | 標題 | 裁決與理由 |
| ---: | --- | --- | --- | --- |
| #279 | MERGED | `12e6973` | fix(auth): 后台 cookie 的 Secure 按请求协议判断，明文入口不再丢会话 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #281 | MERGED | `07471ae` | fix(http): TLS 握手被拒时改用 P-256 重试一次，救回一批 Node 打不开的政府站 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #285 | MERGED | `7951291` | fix(http): P-256 重试只认 ERR_SSL_BAD_ECPOINT | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #287 | MERGED | `2c4e9d7` | fix(sources): 列表页按次读取的收费记录不再拿时钟当编号 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #288 | MERGED | `782fa8d` | 同步引擎：告警可先交给自动处理服务、信源类别门槛、全部动态只列 40 分以上 | **defer**：已合併；掃描命中的長行已讀過為正常內容（見上）；隨整樹採納 |
| #289 | MERGED | `553e2c7` | chore(deps): bump fast-uri | **skip**：已合併；fork lock 已有相同版本 |
| #290 | MERGED | `c1e457f` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #291 | MERGED | `cb41887` | feat(og): 站点可另加补充字体，补上 Noto Sans SC 子集缺的字 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #292 | MERGED | `07fb377` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #293 | MERGED | `6531976` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #294 | MERGED | `fd15fea` | fix(deps): zod 升到 4.6.6 | **skip**：已合併；fork 的 zod 4.6.7 高於其 4.6.6 |
| #295 | MERGED | `71b64d1` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #296 | MERGED | `a3b0847` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #297 | MERGED | `12f00fb` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #298 | MERGED | `6d200ca` | chore(deps): bump undici from 7.30.0 to 7.30.1 | **skip**：已合併；fork lock 已有相同版本 |
| #299 | MERGED | `4d4aeab` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #300 | MERGED | `45f7cb6` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #301 | MERGED | `15c8310` | 同步引擎 | **defer**：已合併；掃描命中的長行已讀過為正常內容（見上）；隨整樹採納 |
| #302 | MERGED | `1b1c4e6` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #303 | MERGED | `2e52fd1` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #304 | MERGED | `fa1d5ec` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #305 | MERGED | `dea9bd7` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #307 | MERGED | `26e97ff` | 文档：补上怎么省模型费用，说明 Agent Skill 只在线上 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #308 | MERGED | `f9c9b22` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #309 | MERGED | `df3757e` | 文档与配置：customize.md 不重抄字段注释，补齐 OpenAPI retryAfter 与 test:web | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #310 | MERGED | `5b1b102` | 把通知注释里的 Webhook hub 改成 Agent 自动化中台 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #311 | CLOSED | `b322466` | 同步引擎 | **skip**：closed 未合併；改 `notify/feishu.ts` 與 `tests/owner-alerts.test.ts`（告警產品行為），上游未收，fork 預設關閉飛書通知，不採用 |
| #312 | MERGED | `24d626d` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #313 | MERGED | `ff5c66f` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #316 | MERGED | `ba9ba27` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #317 | MERGED | `b7702d3` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #318 | MERGED | `b015cd6` | 同步引擎 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #321 | MERGED | `88ca762` | 修复：列表源末尾的实时计数不再触发内容修订 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |
| #322 | MERGED | `9312ba2` | 修复：模型配置写了不存在的名字时，后台页面给出提示 | **defer**：已合併，內容就是上表同名 commit；隨整樹採納 |

### Issue 軸（10 筆：4 defer、6 skip；全部在上游已 closed）

| Issue | 標題 | 裁決與理由 |
| ---: | --- | --- |
| #276 | codex-resets：announced 事件预估窗口过期后永不收口，确认帖只新增独立事件，旧预告永久滞留「待确认」 | **skip**：上游 not_planned 關閉（維護者逐條對過，接口行為符合約定）；codex-resets 模組已移出框架，fork 不含 |
| #277 | 正文兜底：可选用 Keenable 读取，代替 Jina（BODY_READER=keenable） | **skip**：上游 not_planned 關閉（Keenable 讀取方不收）；功能請求 |
| #278 | 后台登录在非 HTTPS 入口永远失败：cookie 的 Secure 只看 SITE_URL | **defer**：上游已由 #279（`d86c120`）修；fork 同樣有此缺陷（`apps/api/src/routes/admin-auth.ts:26` 的 `secure()` 只看 `config.siteUrl.startsWith("https://")`），隨整樹採納 |
| #280 | feat(sources): 新增网页搜索型信源（search kind），用查询词覆盖没有稳定列表页的长尾 | **skip**：上游 not_planned 關閉（搜索型信源不放進開源版）；功能請求 |
| #282 | 部分政务站 Node 握手报 ERR_SSL_BAD_ECPOINT，curl 与浏览器却正常 | **defer**：上游已由 #281／#285（`0c75802` 等三個 commit）修；缺陷在 Node 對部分政務站的 TLS 握手，fork 未加此重試，隨整樹採納 |
| #286 | 官方 /api/v1/hot-topics 返回 567 blocked，反馈页同时返回 520 | **skip**：上游 not_planned 關閉（共用 Cloudflare 出口被站點限流，上游託管服務的問題） |
| #314 | 列表源的实时计数（Stars/Forks）进入内容哈希，热门条目每天被重分析上百次 | **defer**：上游已由 #321（`5c10a6e`）修；隨整樹採納 |
| #315 | 崩溃残留的 'received' 回执/attempts 永不回收，永久闸住对应请求与文章 | **skip**：上游 not_planned 關閉，維護者以真實資料反駁：`received` 不是崩溃殘留，不該回收 |
| #319 | 模型配置指向不存在的预设名时静默落回默认，后台无任何提示 | **defer**：上游已由 #322（`6e0cfaf`）修；隨整樹採納 |
| #320 | 提议：模型路由插口——每步的候选链/暂停可由模块动态提供，适配多免费档并用 | **skip**：上游 not_planned 關閉（模型路由插口框架先不加）；功能提案 |

PR 水位推到 #322、issue 水位推到 #320：這兩軸已逐筆分流。commit 水位維持 `79d962e`，所以 `--strict` 仍回 exit 1，直到整樹採納完成。

## Open pull requests

| PR | Head | 決定 | 重新審查條件 |
|---:|---|---|---|
| [#263](https://github.com/KKKKhazix/AIHOT/pull/263) | `656564f`（2026-10-27 重取 `refs/pull/263/head` 仍是同一 SHA，無 force-push） | **2026-11-01 已合併**（head 已由 `656564f` 變為 `7dd34dc`，合併 commit `823db74`，`translate.ts`＋測試 +34／-3）；不再是 open，隨整樹採納，見 2026-11-02 一節。舊判讀：暫不移植。新增「全文譯文導入入口」，動 `editorial/translate.ts`＋測試共 35 行；屬新的寫入入口（對應 open issue #261），產品行為尚未被上游收下，本 fork 沒有需要它的模組。判準八掃描 0 命中（2026-10-27 對 `b3998dc..656564f` 差量重掃：2 檔 35 行，無「空白夾程式」、無超長單行、無 `eval`／`new Function(`／`globalThis`、無長 base64）。 | head SHA 或狀態改變。 |

## Closed, unmerged pull requests

判準六：本 fork 已有產品碼與測試分岔，不能因 PR 未被上游採納就排除其修復本 fork 缺陷的可能。審查時對照 [`DIVERGENCE.md`](DIVERGENCE.md) 的現行差異，檢查缺陷是否仍存在、是否涉及 fork 的安全與導航修正或額外承擔的情境（Windows、繁中），並以回歸測試證明是否需要移植；安全告警的逐筆理由沿用 [`DECISIONS.md`](DECISIONS.md) 第 9 條，不在本檔複製。以下保留既有逐筆結論；若本 fork 的相關分岔、source/sink 或防護邊界改變，即重新評估受影響項目，不必等上游重開。

#93、#94、#101 的主題已由上游整合的 #105／#116 吸收；#255（Dockerfile 釘 `node:24.22.1`）不收：基底映像 `node:24-trixie-slim` 是浮動標籤，重建時就會取得最新 24.x，釘死反而不會自動跟進安全版；#158／#159（`dev.sh`）依賴 POSIX shell，本 fork 的本機驗證走 `tools/dev_check.*`。其餘（#99、#100、#113–#115、#118、#129、#194、#207、#211、#240、#245、#247、#248、#258、#262、#264，加上先前 #24–#72 系列）皆為新功能、資料提案或已被合併 PR 取代；除上述 fork 變動外，上游重開或以新 PR 重提時也重新評估。判準八對全部 66 個未合併 PR 的現行 head 掃描：命中的只有 PR 內的測試素材（`tests/fixtures/game-sources/*`）、品牌圖檔（`site/brand/nameplates/*.svg`）與一行測試用 `new Function(SIDEBAR_BOOT_SCRIPT)`，皆非隱藏載荷，且都不移植。

`#56`、`#100`、`#194`、`#258` 觸及本 fork 分岔檔（`publication/agent.ts`、`http-policy.ts`、`FeedItem.tsx`、`routes/item.tsx`、`navigation-performance.test.ts`），2026-11-02 已依判準六逐筆讀 `gh pr diff` 與現行檔案重審，整體不採用（#194 整包不採用，但其中一個 `agent.ts` hunk 經判準六判定為本 fork 也有的缺陷，已於 fork 另行實作，見 [`DIVERGENCE.md`](DIVERGENCE.md) 的 agent／items／publish／v1／openapi 列）：

- #56（週報公開 API）：不移植。其 `agent.ts` 只改 `agentGuide()` 的一行週報說明，`http-policy.ts` 只在 `V1_CACHE_CONTROL` 加 `weeklies`／`latestWeekly`／`weeklyByWeek`；現行 fork 已無該常數，週報 v1 端點改由 `apps/api/src/routes/v1.ts` 的 `weeklies` 路徑與 `V1_OPERATIONS` 提供，`agentGuide()` 也已改由模組組裝。該 PR 動的行不含 fork 補丁（`linkText` 反斜線跳脫在 `agent.ts:42`、`replaceAll("*", () => …)` 在 `http-policy.ts:85`），無衝突，也不涉及連結跳脫或轉址替換缺陷。
- #100（把「推薦理由」「AI 評分」改讀 `ITEM_COPY`）：不移植，現行 fork 已有等效。`site/site.ts` 已有 `ITEM_COPY.reasonLabel`／`showScore`，`FeedItem.tsx:118`、`item.tsx:238,413,511`、`agent.ts:71,79` 已經使用；該 PR 的 `agent.ts`／`item.tsx`／`FeedItem.tsx` 改動只是文案常數化，不碰 `linkText`、`isPhone()` 或目錄邊界鍵盤攔截。
- #194（大型介面改版，另含 ask 模組、遷移、部署 workflow，`gh pr view 194` 回報 338 檔）：不採用。其 `FeedItem.tsx`／`item.tsx` 改動是 spotlight 卡片、標題 `viewTransitionName`、Toast 重構、入選說明面板；`FeedItem.tsx` 的 `IntentLink viewTransition` 在 PR 側仍無條件啟用，且再替標題加共享 view-transition 名稱，與本 fork 的 phone 停用（`viewTransition={!isPhone()}`，WebKit 回歸）方向相反，採用會重新暴露那個缺陷。`navigation-performance.test.ts` 的改動只是把 fixture 分類換成 `new-games`／`esports` 遊戲行業分類，沒有 router／DOM 一致性斷言，無法取代 fork 的回歸。也不涉及 `item.tsx` 的目錄邊界鍵盤攔截（hunk 止於 ReadingProgress 與 Toast 一帶）。
  - 另有兩個後端檔：`apps/api/src/routes/agent.ts`（+11／−3）讓模組 ability 接受可選查詢參數並把業務錯誤轉成 problem 回應，屬新功能，不採用。`packages/backend/src/publication/agent.ts`（+29／−3）新增 `itemTimeBits`，在 agent 輸出加「站內時間 `timelineAt`」，來源與站內時間差 1 分鐘以上才另列「原文發布於」，並在 `BRIEF_HINTS` 提示「最近 N 小時」要按站內時間過濾。**本 fork 當時有同樣缺陷**：`v1.ts` 的 `latest`／`search` 以 `p.sort_at`／`p.timeline_at` 判視窗與排序（agent 走 `by: "timeline"`），但 `V1ItemPayload` 沒有 `timelineAt`，`itemLines` 只印 `發布於 publishedAt`。條目 `publishedAt` 早於進站時間時，agent 依畫面上的時間做「最近 N 小時」過濾會誤刪視窗內的條目；這與服務端視窗語意不一致，不是 fork 獨有但 fork 同樣中招。**值得移植，但不能整段套用**：該 hunk 的上下文是舊的未跳脫 `linkText` 正則（`/([[\]])/g`），而 fork 是 `/([\\[\]])/g`（`agent.ts:42`，反斜線跳脫安全修正），整段套用會把補丁蓋掉；且 `V1ItemPayload` 與帳本 payload 沒有 `timelineAt`，要先擴充公開契約。2026-11-02 已於 fork 另行實作（保留反斜線跳脫；`V1ItemPayload`、帳本 payload 與 v1 OpenAPI 加可選 `timelineAt`；舊帳本缺欄位時退回原輸出；回歸測試在 `tests/fork-security-fixes.standalone.test.ts`），分岔列見 [`DIVERGENCE.md`](DIVERGENCE.md)。舊 `selected_ledger` payload 不回填：缺欄位時維持原輸出，個別條目重新 sync 時自然帶上。
- #258（分享卡片按鈕）：不採用。`item.tsx` 改動是把「分享卡片」做成原文連結旁的按鈕、手機工具列 `onShare` 改開海報、並在手機動作表新增分享列；這是版面偏好，現行 fork 已可從選單與手機動作表使用「生成分享海報」（`item.tsx:346,362`）。不涉及目錄邊界鍵盤攔截，與 fork 補丁無衝突，也未修任何本 fork 的缺陷。

查證範圍：四筆 diff 皆以 `gh pr diff` 或 `gh api pulls/<n>/files`（#194 的整份 diff 過大，改取檔案 patch）唯讀取得；未在本機執行這些 PR 的測試，結論來自 diff 與現行程式碼比對。

## Open issues

| Issue | 決定 | 重新審查條件 |
|---:|---|---|
| [#261](https://github.com/KKKKhazix/AIHOT/issues/261) | **2026-11-01 上游 closed（completed）**，隨 #263 處理。舊判讀：模組恢復全文譯文的寫入入口提案；與 PR #263 同一件事，本 fork 暫不跟。 | #263 合併或 issue 有結論。 |
| [#267](https://github.com/KKKKhazix/AIHOT/issues/267) | **上游已 closed**，由 #291 實作站點補充字體（`7265071`），隨整樹採納。舊判讀：分享圖允許站點補充字體（補 Noto Sans SC 子集缺字）。本 fork 沒有自訂分享圖字體的需求；缺字只影響罕用字。 | 上游提出實作，或本 fork 站點出現分享圖缺字。 |
| [#270](https://github.com/KKKKhazix/AIHOT/issues/270) | 使用者詢問公眾號與社媒信源為何常被阻擋；純提問、無缺陷、無 PR，不需動作。2026-10-26 上游維護者回覆並**關閉**（狀態由 open 變 closed）：公眾號走 `mp_account`（`DAJIALA_KEY`）、X 走 `x_search`，其他走 RSSHub／外部推送，設定見 `docs/sources.md`；仍無程式變更。 | 上游重開，或出現缺陷結論或關聯 PR。 |
| [#271](https://github.com/KKKKhazix/AIHOT/issues/271) | **2026-10-26 上游關閉**：由 `aa8e5b1`（PR #273，告警 Webhook）實作，本 fork 已隨 commit 軸採納。以下為原判讀：詢問飛書系統告警為何走應用機器人而非 Webhook，建議告警可選 Webhook。**不是缺陷、無 PR**：維護者 2026-10-26 回覆原因（內部群同時轉發帶截圖的反饋，圖片上傳只有應用機器人能做），「告警單獨走 Webhook 要先在產品上定」，尚無結論。本 fork 實況：`packages/backend/src/notify/feishu.ts:111-121` 的 `sendAlert` 只走 `FEISHU_ALERT_CHAT_ID`／`FEISHU_INTERNAL_CHAT_ID` 應用機器人，且 `FEISHU_INTERNAL_ENABLED` 預設關（`.env.example:73`）；本 fork 未啟用飛書，上游額度痛點不適用（判準七：理由的主詞是飛書個人免費企業的使用者，不是本 fork）。不移植、無需動作。 | 上游出現告警 Webhook 的 PR／commit，或本 fork 開啟 `FEISHU_INTERNAL_ENABLED`。 |

已關閉的舊追蹤項（#67、#77、#86、#88）全部在上游關閉，結論見上節。#88（推理模型 `max_tokens`）已由 #105 的「推理模型額度」處理，workaround `LLM_EXTRA_JSON` 不再需要；README 已記載 `LLM_REASONING_TOKENS`。

## Branches, tags, releases

- 上游分支：只有 `main`（2026-10-28 `git ls-remote` 為 `79d962e`）；無 tag、無 GitHub Release。issue 編號 #272 查詢回 404（已刪除或移轉），沒有可審內容。
- 本 fork 分支：只有 `main`（`ci/job-names-20261024`、`security/alerts-20261024`、`tmp-probe-delete` 已於 2026-10-25 清除）；無 tag、無 Release。
