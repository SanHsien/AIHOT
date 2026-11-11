# 上游審查紀錄

最後審查：2026-11-10（commit 水位 `7140b6f`，PR 水位 #383、issue 水位 #340；追蹤中的 open PR：#375）

本檔只記可執行結論。機器水位與 open PR head SHA 放在 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。相同 SHA、狀態與庫存不重審；任一項變動才重新評估。

## 2026-11-10 整樹採納（`cd424b0..7140b6f`）

fetch 確認的 main `8e02c95`（commit 水位已再推到 `7140b6f`，見下）：51 個 commit、118 個路徑、+4514／-483。做法同 2026-11-03：把 `git diff cd424b0 upstream/main` 以 `git apply --3way` 套到 fork 樹。審查過程中上游又前進一個 commit（`9a7f5bd` → `8e02c95`，即 #382 合併），該增量另行套用，無衝突。其後 #383 合併為 `7140b6f`（2 檔、+2／-2），同日追加採納，總計 52 個 commit。

- 衝突兩處，已人工合併：`AGENTS.md`（上游在簡中安全閥句加入 `BAIDU_PUSH_ENABLED`，fork 是繁中改寫，只把該變數加進繁中句，上游其餘簡中規則不蓋回）與 `apps/web/app/features/feed/FeedItem.tsx`（上游在 X 貼文摘要包 `shortAddresses(...)`，fork 保留 `viewTransition={!isPhone()}`，兩者並存）。其他與分岔登記重疊的 `apps/web/app/routes/item.tsx`、`publication/agent.ts`、`publication/items.ts`、`contracts/src/http-policy.ts`、`apps/web/tests/navigation-performance.test.ts` 三方合併無衝突；`http-policy.ts` 的 `replaceAll("*", () => …)` 仍在，上游新增 `canonical` 規則與貼文尾巴（`pastedPage`）轉址不觸及它。分岔登記列數由檢查器實算為 16 列，與實際變更吻合，無需新增或刪列。
- 分岔收斂條件逐條對照（上游本次有改動的分岔登記檔，以 `git show upstream/main:<檔案>` 讀取）：`http-policy.ts` 上游 `prefix` 規則仍是 `rule.location.replace("*", pathname.slice(...))`（字串替換值，`$` 序列仍會被解讀），保留 `replaceAll` 補丁；`agent.ts` 上游 `linkText` 仍只跳脫 `[`、`]`，且沒有 `timelineAt` 輸出，保留；`items.ts` 上游 `ApiItemRow` 與 `API_ITEM_COLUMNS` 的取捨與 fork 差異未變，保留；`item.tsx` 上游目錄邊界攔截仍只呼叫 `preventDefault`、`FeedItem.tsx` 仍無 phone 判斷（本次只多 `shortAddresses`），保留。16 列分岔登記全部維持。
- 新增 4 個遷移：0124、0125、0126 是 `notify_targets_kind_check` 的三段式（DROP IF EXISTS → ADD … NOT VALID → VALIDATE），0127 是 `articles ADD COLUMN cover jsonb`（可 NULL、無預設值）。均為新檔、每檔一條語句，未修改已發布遷移。本機沒有 PostgreSQL，**尚未在有資料的庫上驗證升級**，見 ROADMAP；CI 空庫全新安裝在推送後才有結果。
- 隱藏內容掃描：對 `cd424b0..8e02c95` 的 4632 條新增行掃描「行內 ≥40 空白」「>400 字元行」「eval／new Function／globalThis.require／child_process／exec／atob／fromCharCode」「≥120 字 base64」「≥64 位 hex」「零寬與雙向字元」，0 命中。另對標題含 fix 或牽涉媒體、轉址、輸入處理的 commit 讀 diff：`f925285`（X 影片簽章代理，`isXVideoUrl` 只放 `https://video.twimg.com` 的 `amplify_video|ext_tw_video|tweet_video` MP4，HMAC 簽章與期限仍必過）、`http-policy.ts`（貼文尾巴轉址只改相對路徑、API 路徑不動、不跨站）、百度推送（預設 `BAIDU_PUSH_ENABLED=false`）、釘釘推送（預設 `DINGTALK_CONTENT_PUSH_ENABLED=false`）。
- 測試時間炸彈檢查：新增測試內寫死日期共 2021–2026 年份的夾具；`baidu-push.test.ts` 的 `DAY1`／`DAY2` 以參數注入時鐘（`submitBaiduPush(DAY1)`），`mentions.test.ts` 的 `at` 與頁面測試的日期只作為夾具資料，沒有「相對現在的視窗」比較，未發現會隨日期過期的斷言。
- 百度推送的 token（`4edbe4b` 起）以純 HTTP 的 query string 送出，上游 `baidu-push.ts` 的 `ENDPOINT` 為 `http://data.zz.baidu.com/urls`，且 `reply.remain` 只驗 `typeof === "number"`（負數會造成空批次無限 POST）。2026-11-11 Codex 覆核（F1／F2）後 fork 加分岔（見 `docs/DIVERGENCE.md`）：端點改讀 `BAIDU_PUSH_ENDPOINT`，非 https 就在啟用時拒絕並寫明原因、請求不跟隨轉址；`remain` 必須是非負安全整數（含持久化舊值），單輪最多 50 次請求與 5 分鐘。百度推送文件頁（ziyuan.baidu.com）為前端渲染，無法唯讀確認有 HTTPS 端點，故預設值保持文件上的 http 位址、等於 fork 維持停用，待確認 https 端點後才在 `BAIDU_PUSH_ENDPOINT` 填入。`config.baiduPushToken` 仍直接讀環境變數、不走 `credential()`。預設 `BAIDU_PUSH_ENABLED=false`，本 fork 不啟用（中國服務）。跟進上游時若其改 https 並驗 `remain`，刪除對應分岔列與 guard 檔。
- 站點預設：`4e45b6b` 使 `SITE.poweredBy` 預設為 `{ name: "AIHOT", url: "https://aihot.news" }`，側欄與「我的」頁顯示「由 AIHOT 驅動」；`4106602` 加 `SEO_TITLES`，`53e534b` 加 `SITE.siteVerification`。三者都是 `site/site.ts` 的選填設定，原樣採納；本 fork 沒有自己的部署，若日後部署自建站，依 `AGENTS.md`「自建站不得使用 AIHOT 名稱與 Logo」把 `poweredBy` 設為 `null` 或自己的名稱。

| 上游 commit | 裁決與理由 |
|---|---|
| `a3d0263`、`15f7b2d`（#336） | adopt：X 歷史 backlog 只留一份、超過 3 天放棄；分片重組後已移走帳號的積壓貼文仍入庫。直接回應 issue #335 的花費事故。 |
| `1e839a7`（#337） | adopt：側欄只點亮最具體的一項（`Sidebar.tsx`、`nav.ts`）。不在導航分岔登記檔內。 |
| `6aafd93`、`22e3105`、`0ce2d00`（#342） | adopt：釘釘群機器人內容推送，遷移 0124–0126；預設關。 |
| `4106602`、`4e45b6b`、`53e534b`（#343–#345） | adopt：`SEO_TITLES`、`poweredBy`、`siteVerification`（見上）。 |
| `df70f8f`、`4edbe4b`、`61ef3bb` | adopt：百度主動推送（`baidu-push.ts`、排程、`.env.example`、`AGENTS.md` 安全閥句），預設關。 |
| `92e4a15`、`ad3e934`、`5e17c25`、`61f72c5`、`377e6c9`、`6fe293d`、`d92d42f` 等 | adopt：錯誤頁與 Cookie 同意、導航、頁腳不進正文（issue #338）及相關正文抽取回歸。 |
| `265ddc2`（#364） | adopt：文章封面 `cover.ts` 與遷移 0127。 |
| `c605442`、`ee2ba20`、`5f42520` 等 | adopt：提及（mentions）、短位址、版面與 SEO（`seo.ts`、`item.tsx`、`report-latest.tsx` 等）。 |
| `f925285`、`2d8410f`（#373、#377） | adopt：X 影片代理與 Range 回應、socialdata 與 sanitize 補強（讀 diff 見上）。 |
| `cf4a9d9`、`b5297e8`（#368、#378） | adopt：`http-policy.ts` 的 canonical 轉址與貼文尾巴轉址；與 fork 的 `replaceAll` 修正並存。 |
| `623c629`、`a6641fa`、`a040b22`、`f71cf5c`、`fb7ed2c`（#371、#376、#379、#380、#382） | adopt：回饋與 X 改名處理（`feedback.ts`、`x-renames.ts`、`clicks.ts`）。 |
| 其餘「同步引擎」commit | adopt：整樹套用，內容見 `git log cd424b0..upstream/main`；沒有逐筆挑選。 |

| 上游 PR／issue | 裁決與重新審查條件 |
|---|---|
| #336、#337、#339、#341–#374、#376–#382 | merged，對應以上 commit，全部採納。 |
| #375（open，kernelvale，head `c03474fe5380fdd2c3ed4ee1b0bfac71dbdcdac7`，base `ad3e934`，1 commit、8 檔、+119／-30） | defer，已讀完整 diff：把 `liveStory`、`resolveStory` 的合併鏈改為遞迴 CTE，`mergeStoryInto` 改在單一交易內重新發布，`groupSignal` 重設訊號並改用 `ANY(...::text[])` 避開 65535 參數上限。內容看來合理，但 PR 未合併，且動到事件歸組與合併交易，需要有 PostgreSQL 的完整 `npm test` 驗證（本機沒有）。fork 定位是跟進上游主線，不先於上游採納未合併的外部 PR。已在 `monitored` 釘住 head 與狀態；觸發條件：該 PR 合併（採納合併後的 commit）、關閉（記為 skip）或 head 改變（重讀 diff）。 |
| #383（merged，`7140b6f`，2 檔、+2／-2） | adopt：`apps/worker/src/schedules.ts` 的 `sources.adapt-intervals` 加 `missed: "once"`，`tests/agent-wake.test.ts` 一個 Finding 的 key 改為 `free-tokens.inbox:1:0`。審查中途它尚為 open 並曾暫列 defer，合併後（2026-11-10 10:24Z）於同日採納，已移出 `monitored`。兩檔不在分岔登記內，3-way 套用無衝突。 |
| issue #334 | 作者撤回，內容已移除；skip。 |
| issue #335 | closed；提出「24 小時花費上限」，維護者決定不加（花費異常只告警），根因已由 #336 修；skip，fork 不另加。重審條件：上游重開。 |
| issue #338 | closed；Cookie 同意與導航混入正文，上游已修並重新抽取；對應修正隨本次採納。 |
| issue #340 | closed；釘釘推送需求，由 #342 實作；已採納。 |

### 本機驗證（2026-11-10，整合來源 `8e02c95`）

- Node.js 24.22.1（`PATH` 前置 fnm 的 v24.22.1）：`npm run typecheck` exit 0、`npm run build -w @aihot/web` exit 0、`npm run test:web` 67/67、`npm run test:standalone` 280/280（含 fork 安全回歸）、`npm audit --package-lock-only` 0 vulnerabilities；`python tools/check_upstream_updates.py --strict` exit 0。
- `tools/dev_check.ps1`（預設 Node.js 26.12.1，BelowNormal 優先權）exit 0：環境驗證、typecheck、SSR build、網頁 67/67、分岔檢查（16 列吻合）、分岔契約 9/9、freshness 契約 2/2。
- 未做：需要 PostgreSQL 的 `npm test`（本機 5432 無監聽）、新遷移 0124–0127 在有資料庫上的升級驗證；X 歷史 backlog、釘釘、百度推送、文章封面的行為只有上游測試的證據，沒有實機採集（安全閥關閉）。

## 2026-11-03 追加採納（`41cee09..cd424b0`）

上游 main 在整樹採納後前進兩個 commit，即 #323 的合併：`dcb366e`、`cd424b0`，只觸及 `apps/web/app/components/ui/Menu.tsx` 與 `apps/web/tests/item-copy.test.ts`，整檔採納。Co-authored-by 致謝：Henry May <mei1733455431@gmail.com>、Claude Opus 5.5 <noreply@anthropic.com>。

## 2026-11-03 整樹採納（`79d962e..41cee09`）

已將 fetch 確認的 main `41cee09f70518fdcacdc307dcba58d635505bb41` 差量以逐檔三方合併採納：48 個 commit、230 個路徑、+5242／-1813，無文字衝突。下方 2026-11-02 的 40 筆 commit 裁決是歷史快照；其中 defer 均已隨本次整樹採納，三筆依賴 skip 已由上游安全版本涵蓋。PR #263 的 revision-checked 全文譯文入口與 #291 的分享圖補充字體一併採納。

- 分岔依 `DIVERGENCE.md` 保留：限流表全站計數、Markdown 跳脫、prefix 替換、手機導航、目錄捲動、測試 cleanup 與 `timelineAt`。`http-policy.ts` 的舊 `/sources` 規則已移除，prefix 回歸改用測試模組宣告的規則。
- 上游 `zod` 4.6.6 已符合原登記的 ≥4.6.6 收斂條件；`fast-uri`、`undici` 也已有安全修補，兩個 manifest 與 lock 改採上游，移除三列依賴分岔。
- 依保留既有檔案的限制，`day-header-year.test.ts`、`report-year.test.ts`、`sign-in-paths.standalone.test.ts` 留存；上游已把同類斷言併入既有測試，這三個路徑在新基準下屬 fork 自有測試。
- 新增 7 個遷移：0090、0091、0092、0105 是新增欄位；0121、0122、0123 是 `CONCURRENTLY IF NOT EXISTS` 索引。均為新檔、每檔一條語句，沒有修改已發布遷移。採納當時本機沒有 PostgreSQL，只有 CI 空庫全新安裝；既有資料庫的升級路徑於 2026-11-09 補驗，見下方「既有資料庫升級驗證」。
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
| #323（merged，`cd424b0`） | adopt：Menu 鍵盤導航與焦點修復，作者 Henry May。合併為 `dcb366e`（鍵盤導航、Esc 返回觸發鈕、Tab 離開關閉、`inert`／`aria-hidden`）與 `cd424b0`（移除容器 `onBlur` 關閉，修 Safari 按下按鈕不取得焦點而重開選單）。fork 的 `Menu.tsx` 與 `item-copy.test.ts` 原與上游 `41cee09` 相同（`Menu.tsx` 第 13 行 Escape 只 `setOpen(false)`、無 `triggerRef`），整檔改為 `cd424b0` 內容，兩檔皆非分岔登記檔。同 PR 的 webkit 與 Chromium 回歸隨 `item-copy.test.ts` 一併採納。 |
| #324、#325、#326、#327、#329、#330、#331、#332 | merged，分別對應以上八個 commit，全部採納。 |

issue #320 之後無新增，issue 水位不變。


### 本機驗證（2026-11-03，整合來源 `41cee09`）

- Node.js 24.22.1：`tools/dev_check.ps1` exit 0（typecheck、SSR build、網頁 65/65、分岔契約 9/9、freshness 契約 2/2）；`npm run test:standalone` 249/249，`npm audit --package-lock-only` 0 vulnerabilities，`check_upstream_updates.py --strict` exit 0。
- HTTP cookie 回歸在舊實作為 `true !== false`，採納後 5/5 fork 安全回歸通過。分岔檢查器新增回歸：基準新增檔存在但未追蹤時，舊檢查器誤報刪除；改依 Git filtered blob 比對後，相同內容與不同內容兩個案例皆通過，實際 15 列登記吻合。
- 公開樣本只下載一次後由 localhost fake server 重播：Google Research RSS 100 筆、Hugging Face RSS 895 筆，以及各自最新一篇原文；以 load hook 載入起點 `92d91d7` 原始碼，與採納後比對。995 筆的 URL、標題、日期、摘要、正文與狀態完全相同；兩篇正文分別 9424、9686 字元，SHA-256 與日期也完全相同。這項比對未呼叫模型或連線資料庫。
- 預設 Node.js 26.12.1 的 standalone 為 248/249：既有 secure-proxy fixture 把 IP 設為 SNI，Node 26 拋 `ERR_INVALID_ARG_VALUE`；同一程式與測試在專案指定的 Node 24.22.1 通過。沒有修改 TLS 驗證或放寬斷言。
- `git diff --check` 唯一提示為上游原有的 `tests/collection-body-preservation.test.ts:73` 檔尾空行；保留上游內容，沒有為格式建立額外分岔。

### 既有資料庫升級驗證（2026-11-09，`main` `94a2492`）

- 環境：EDB 官方免安裝 zip `postgresql-17.11-5-windows-x64-binaries.zip`（與 CI 的 `postgres:17` 同主版本；EDB 未公布雜湊、執行檔無數位簽章，記下 SHA-256 `80379b2c04d51c30225532e0ae04509899141e9957ed096fe749d7fd9df8f82f`，Defender 掃描無威脅），只聽 `127.0.0.1:5433`，未註冊服務；Node.js 24.22.1。驗完已停止並移除。
- 起點：以採納前 `92d91d7` 的遷移檔（0001–0089 共 64 檔，與現行同名檔內容相同）建 `aihot_upgrade_test`，灌入受影響三表的樣本：`sources` 4 列（四種 tier、三種參與模式）、`feedback` 200 列（五種狀態）、`articles` 50,000 列（含帶 `&sn=`、帶 `#` 片段的微信長網址身分鍵、`/s/` 短網址、`raw.externalId` 微信與非微信值）。
- 升級：在 `main` 執行 `npm run db:migrate`，exit 0，依序 `applied` 0090、0091、0092、0105（transaction，3–15ms）與 0121、0122、0123（index，88–135ms），`7 migration(s) applied`；重跑回報 `database is up to date`。
- 結果：`sources.selection_class`、`feedback.kind`、`feedback.idea` 為可 NULL `text`，`sources.uses` 為 `text[] NOT NULL DEFAULT '{}'`，既有列分別為 NULL 與 `{}`；三個 `articles_wechat_*` 索引 `indisvalid`、`indisready` 皆為 true，`EXPLAIN` 對應查詢都走該索引。三表原有欄位與 0089 以前 `schema_migrations` 的逐列 MD5 前後相同；刪除樣本後 `pg_dump --schema-only` 與同版本空庫全新安裝逐行相同。
- `npm test`：樣本留在模板庫時，告警與讀取負載測試會把樣本算進積壓與信源數而失敗（測試假設模板是空庫），故以刪除樣本的升級庫副本 `aihot_upgraded_test` 為模板跑：1042 項中 1010 通過、26 失敗、6 取消。其中 16 項是 Windows 本機限制，與遷移無關：`backup.test.ts` 10 項（GNU tar 把 `C:` 當遠端主機、建 symlink 需權限、`pg_dump` 錯誤訊息被在地化，且該檔跑完不退出）、`analyze-shutdown.test.ts` 與 `translate-shutdown.test.ts` 6 項（Windows 沒有可攔截的 SIGTERM，120 秒逾時），三檔合計 10 失敗 6 取消，在空庫全新安裝上結果相同；`page-metadata`、`malformed-public-paths` 14 項是先跑測試、未先 `npm run build -w @aihot/web`，建置後與並行時偶發失敗的 `signals`、`topics-withdrawal` 一起重跑 26/26 通過。同一 commit 在 Linux 的 [check.yml run 42414832835](https://github.com/SanHsien/AIHOT/actions/runs/42414832835) 完整 `npm test` 成功。

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
