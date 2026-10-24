# 分岔登記表

本檔只登記本 fork 對**上游持有檔案**的修改。Fork 新增檔案（例如 `FORK.md`、`README.en.md`、`docs/UPSTREAM.md`、`tools/`）不算逐檔分岔，清單見 [`FORK.md`](../FORK.md)。

## 維護契約

修改任何上游持有檔案，必須在表內加一列。[`tools/check_divergence.py`](../tools/check_divergence.py) 會比對 `tools/upstream_baseline.json` 的 `reviewed_through` 與目前工作樹；實際變更與登記不一致即失敗。

最後一欄必須寫可執行判準，讓下一次同步不用重做判斷。

| 上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理 |
|---|---|---|---|---|
| `README.md` | 簡體中文產品說明、快速開始、自訂行業與文件索引。 | 完整改寫為繁體中文，加入語言切換、Fork 說明、維護文件與本機驗證入口；產品內容已同步至上游公開介面 3.0.0。 | 公開入口以繁中為主，且需要向使用者揭露本 fork 的維護與驗證方式。 | 上游更新時，把新增或改變的產品能力人工翻譯整合到對應章節；保留 Fork 說明與繁中入口，不得整檔覆蓋。 |
| `README.en.md` | 上游沒有此路徑；來源內容位於簡體中文 `README.md`。 | 新增完整英文版，與繁中 README 維持同一資訊架構。 | GitHub About 與 README 皆提供繁中／英文雙語，讓非中文讀者可直接使用。此路徑由分岔檢查器視為 `README.md` 的語言鏡像。 | 上游 `README.md` 有產品能力變更時，同步更新繁中與英文版本；不得把簡中原文整份覆蓋到本檔。 |
| `AGENTS.md` | 簡體中文產品規則：自訂行業、執行檢查、架構邊界與程式碼風格。 | 繁中化並加入本 fork 的 GitHub 邊界、分岔檢查、上游水位紀錄與直接推 main 工作流；保留上游全部有效規則。 | `AGENTS.md` 是所有 coding agent 的單一真相源，必須同時承載產品規則與 fork 邊界。 | 上游新增規則時人工合併並翻成繁中；Fork 邊界保持不動。若上游規則已被新架構淘汰，依新版本更新，不為零 diff 保留舊規則。 |
| `CLAUDE.md` | 一行 `@AGENTS.md`。 | 已刪除；原補充內容併入 `AGENTS.md`。 | 只維護業界通用的 `AGENTS.md`；Claude Code 在沒有 `CLAUDE.md` 時直接讀 `AGENTS.md`。 | 不收回本檔；上游若改成實質規則，將有效內容併入 `AGENTS.md`。 |
| `docs/sources.md` | 未提及 `_aihot.initialBackfillOnly` 選項。 | 移植上游 PR #85：於信源規則補充 `_aihot.initialBackfillOnly: true` 說明。 | 讓自訂信源維護者清楚防止歷史資料過量灌入的設定方式。 | 上游若合併 PR #85 或自行補充相同說明，採用上游版本並刪除此列。 |
| `packages/backend/src/sources/collect.ts` | 首次匯入後之抓取對發布過久的歷史資料不做過濾（Issue #86）。 | 移植上游 PR #85：當配置 `_aihot.initialBackfillOnly: true` 時，後續抓取過濾早於加入前 48 小時之歷史存量。 | 防止長歷史 RSS 信源在第二次抓取時大量灌入舊資料造成分析費用浪費。 | 上游若合併 PR #85 或以等效機制解決，採用上游版本並刪除此列。 |
| `packages/backend/src/sources/config-keys.ts` | `_aihot` 僅支援 `initialBackfillLimit` 與 `initialBackfillMonths`。 | 移植上游 PR #85：在 `_aihot` 新增 `"initialBackfillOnly"`。 | 與 `collect.ts` 配合放行該設定欄位。 | 上游若合併 PR #85 則刪除此列。 |
| `packages/backend/src/sources/rss.ts` | `feedText` 判定本文要求 `bodyText.length > 280 && !teaser`。 | 移植上游 PR #83：當配置 `summaryIsBody: true` 時，即使短摘要亦放行作為本文。 | 播客或短訊息類 RSS 信源摘要即本文，避免非預期發起無效詳情頁抓取。 | 上游若合併 PR #83 則刪除此列。 |
| `tests/architecture.test.ts` | 以 `path.relative` 產出路徑比對目錄名稱與規則。 | 移植上游 PR #79：將路徑轉換為 posix 斜線（`split(path.sep).join("/")`）。 | Windows 反斜線會導致模組所屬權與介面讀取判定全部誤報。 | 上游若合併 PR #79 則刪除此列；若修改架構規則保留正規化代碼。 |
| `tests/collection-tail.test.ts` | 未包含 `initialBackfillOnly` 之後續抓取行為測試。 | 移植上游 PR #85：新增 `initialBackfillOnly 時，下一次普通采集不再補進加入前的舊條目` 案例。 | 確保防歷史舊文灌入機制受測試覆蓋。 | 上游若合併 PR #85 則刪除此列。 |
| `package.json` | 依賴 `@modelcontextprotocol/client: 2.1.0`。 | 提前採納上游 PR #144（commit `879afa3`）升至 `2.2.0`，再升至 `2.3.0`（上游主線現值）。 | 安全修補（GHSA-6qxp-vccf-f47h 憑證外洩；GHSA-6prh-2h8m-c8cw）。 | 上游主線跟進時此分岔自然消除；整樹同步時刪除此列。 |
| `packages/backend/package.json` | 依賴 `sharp: 0.35.4`、`sanitize-html: 2.17.7`、`undici: 8.11.2`、`zod: 4.6.5`。 | `sharp` 提前採納上游 PR #145（commit `14fe1da`）升至 `0.35.5`；`sanitize-html` 升至 `2.18.1`、`undici` 升至 `8.12.3`（皆為上游 `b3998dc` 現值）；`zod` 升至 `4.6.7`（上游尚在 `4.6.5`，fork 先行）。 | 安全修補（GHSA-wq5f-xc86-pv6w；sanitize-html GHSA-cv27-6wvh-8x7j、GHSA-x3q4-9hxx-gx8m、GHSA-374f-7chj-9948、GHSA-c9rx-x947-fp3h；undici GHSA-4qv8-2p9j-2685、GHSA-f72v-6w45-q472、GHSA-xjj6-f33q-929c；zod GHSA-mrhx-c7xc-m3w5）。 | 上游主線跟進時此分岔自然消除；若上游的 `zod` 已 ≥ `4.6.6` 則整列刪除，否則保留 `zod` 一項。 |
| `apps/api/package.json` | 依賴 `sharp: 0.35.4`、`@modelcontextprotocol/server: 2.1.0`、`fastify: 5.12.5`、`zod: 4.6.5`。 | `sharp` 升至 `0.35.5`；`@modelcontextprotocol/server` 升至 `2.3.0`、`fastify` 升至 `5.12.7`（皆為上游 `b3998dc` 現值）；`zod` 升至 `4.6.7`（上游尚在 `4.6.5`，fork 先行）。 | 安全修補（GHSA-wq5f-xc86-pv6w；MCP server GHSA-jm63-cq47-j5jp、GHSA-46jr-4wx8-v453、GHSA-rvq5-wwqv-78pq；fastify GHSA-389g-gv7q-r4x8；zod GHSA-mrhx-c7xc-m3w5）。 | 上游主線跟進時此分岔自然消除；若上游的 `zod` 已 ≥ `4.6.6` 則整列刪除，否則保留 `zod` 一項。 |
| `package-lock.json` | 依賴舊版 lockfile（舊版 sharp、MCP client／server、sanitize-html、vite、fastify、undici、zod、fast-uri）。 | 以 `npm install --package-lock-only --ignore-scripts` 依上列 manifest 重生，並把傳遞依賴 `undici`（cheerio 底下）升至 `7.30.1`、`fast-uri` 升至 `3.1.9`／`4.2.3`。 | 清除 `npm audit` 全部 4 項及 Dependabot 開啟中的 20 項警示。 | 上游主線跟進時此分岔自然消除；整樹同步時以上游 lockfile 為準並重跑 `npm audit`。 |
| `apps/web/package.json` | 依賴 `vite: 8.3.1`。 | 升至 `vite: 8.3.3`（上游 `b3998dc` 現值）。 | 安全修補（GHSA-587h-7wmj-h5pm、GHSA-r825-w8mm-5pxw、GHSA-698v-4r3x-3vcv；開發伺服器／建置工具鏈）。 | 上游主線跟進時此分岔自然消除；整樹同步時刪除此列。 |
