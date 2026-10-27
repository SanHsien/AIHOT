# 上游審查紀錄

最後審查：2026-10-28（上游 `79d962e`、PR 水位 #275、issue 水位 #271）

本檔只記可執行結論。機器水位與 open PR head SHA 放在 [`tools/upstream_baseline.json`](../tools/upstream_baseline.json)。相同 SHA、狀態與庫存不重審；任一項變動才重新評估。

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

見 [`DIVERGENCE.md`](DIVERGENCE.md)：README／AGENTS 繁中化、`CLAUDE.md` 刪除，以及 `zod` 4.6.7 與傳遞依賴（`undici`、`fast-uri`）的安全版本。

## Open pull requests

| PR | Head | 決定 | 重新審查條件 |
|---:|---|---|---|
| [#263](https://github.com/KKKKhazix/AIHOT/pull/263) | `656564f`（2026-10-27 重取 `refs/pull/263/head` 仍是同一 SHA，無 force-push） | 暫不移植。新增「全文譯文導入入口」，動 `editorial/translate.ts`＋測試共 35 行；屬新的寫入入口（對應 open issue #261），產品行為尚未被上游收下，本 fork 沒有需要它的模組。判準八掃描 0 命中（2026-10-27 對 `b3998dc..656564f` 差量重掃：2 檔 35 行，無「空白夾程式」、無超長單行、無 `eval`／`new Function(`／`globalThis`、無長 base64）。 | head SHA 或狀態改變。 |

## Closed, unmerged pull requests

判準六：本 fork 的產品碼同步後與上游逐位元組相同（分岔只在文件與依賴版本），所以「被上游拒收的 PR 不可能在修只有本 fork 才有的缺陷」成立；只檢查本 fork 額外承擔的情境（Windows、繁中）。#93、#94、#101 的主題已由上游整合的 #105／#116 吸收；#255（Dockerfile 釘 `node:24.22.1`）不收：基底映像 `node:24-trixie-slim` 是浮動標籤，重建時就會取得最新 24.x，釘死反而不會自動跟進安全版；#158／#159（`dev.sh`）依賴 POSIX shell，本 fork 的本機驗證走 `tools/dev_check.*`。其餘（#99、#100、#113–#115、#118、#129、#194、#207、#211、#240、#245、#247、#248、#258、#262、#264，加上先前 #24–#72 系列）皆為新功能、資料提案或已被合併 PR 取代；只有上游重開或以新 PR 重提才重新評估。判準八對全部 66 個未合併 PR 的現行 head 掃描：命中的只有 PR 內的測試素材（`tests/fixtures/game-sources/*`）、品牌圖檔（`site/brand/nameplates/*.svg`）與一行測試用 `new Function(SIDEBAR_BOOT_SCRIPT)`，皆非隱藏載荷，且都不移植。

## Open issues

| Issue | 決定 | 重新審查條件 |
|---:|---|---|
| [#261](https://github.com/KKKKhazix/AIHOT/issues/261) | 模組恢復全文譯文的寫入入口提案；與 PR #263 同一件事，本 fork 暫不跟。 | #263 合併或 issue 有結論。 |
| [#267](https://github.com/KKKKhazix/AIHOT/issues/267) | 分享圖允許站點補充字體（補 Noto Sans SC 子集缺字）。本 fork 沒有自訂分享圖字體的需求；缺字只影響罕用字。 | 上游提出實作，或本 fork 站點出現分享圖缺字。 |
| [#270](https://github.com/KKKKhazix/AIHOT/issues/270) | 使用者詢問公眾號與社媒信源為何常被阻擋；純提問、無缺陷、無 PR，不需動作。2026-10-26 上游維護者回覆並**關閉**（狀態由 open 變 closed）：公眾號走 `mp_account`（`DAJIALA_KEY`）、X 走 `x_search`，其他走 RSSHub／外部推送，設定見 `docs/sources.md`；仍無程式變更。 | 上游重開，或出現缺陷結論或關聯 PR。 |
| [#271](https://github.com/KKKKhazix/AIHOT/issues/271) | **2026-10-26 上游關閉**：由 `aa8e5b1`（PR #273，告警 Webhook）實作，本 fork 已隨 commit 軸採納。以下為原判讀：詢問飛書系統告警為何走應用機器人而非 Webhook，建議告警可選 Webhook。**不是缺陷、無 PR**：維護者 2026-10-26 回覆原因（內部群同時轉發帶截圖的反饋，圖片上傳只有應用機器人能做），「告警單獨走 Webhook 要先在產品上定」，尚無結論。本 fork 實況：`packages/backend/src/notify/feishu.ts:111-121` 的 `sendAlert` 只走 `FEISHU_ALERT_CHAT_ID`／`FEISHU_INTERNAL_CHAT_ID` 應用機器人，且 `FEISHU_INTERNAL_ENABLED` 預設關（`.env.example:73`）；本 fork 未啟用飛書，上游額度痛點不適用（判準七：理由的主詞是飛書個人免費企業的使用者，不是本 fork）。不移植、無需動作。 | 上游出現告警 Webhook 的 PR／commit，或本 fork 開啟 `FEISHU_INTERNAL_ENABLED`。 |

已關閉的舊追蹤項（#67、#77、#86、#88）全部在上游關閉，結論見上節。#88（推理模型 `max_tokens`）已由 #105 的「推理模型額度」處理，workaround `LLM_EXTRA_JSON` 不再需要；README 已記載 `LLM_REASONING_TOKENS`。

## Branches, tags, releases

- 上游分支：只有 `main`（2026-10-28 `git ls-remote` 為 `79d962e`）；無 tag、無 GitHub Release。issue 編號 #272 查詢回 404（已刪除或移轉），沒有可審內容。
- 本 fork 分支：只有 `main`（`ci/job-names-20261024`、`security/alerts-20261024`、`tmp-probe-delete` 已於 2026-10-25 清除）；無 tag、無 Release。
