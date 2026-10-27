# 分岔登記表

本檔只登記本 fork 對**上游持有檔案**的修改。Fork 新增檔案（例如 `FORK.md`、`README.en.md`、`docs/UPSTREAM.md`、`tools/`）不算逐檔分岔，清單見 [`FORK.md`](../FORK.md)。

## 維護契約

修改任何上游持有檔案，必須在表內加一列。[`tools/check_divergence.py`](../tools/check_divergence.py) 會比對 `tools/upstream_baseline.json` 的 `reviewed_through` 與目前工作樹；實際變更與登記不一致即失敗。

最後一欄必須寫可執行判準，讓下一次同步不用重做判斷。

| 上游檔案 | 上游原狀 | 本 fork 狀態 | 為什麼分岔 | 跟進上游時怎麼處理 |
|---|---|---|---|---|
| `README.md` | 簡體中文產品說明、快速開始、自訂行業與文件索引。 | 完整改寫為繁體中文，加入語言切換、Fork 說明、維護文件與本機驗證入口；產品內容已同步至上游 4.0.0 引擎（`site/`、`modules/` 分層）。 | 公開入口以繁中為主，且需要向使用者揭露本 fork 的維護與驗證方式。 | 上游更新時，把新增或改變的產品能力人工翻譯整合到對應章節；保留 Fork 說明與繁中入口，不得整檔覆蓋。 |
| `README.en.md` | 上游沒有此路徑；來源內容位於簡體中文 `README.md`。 | 新增完整英文版，與繁中 README 維持同一資訊架構。 | GitHub About 與 README 皆提供繁中／英文雙語，讓非中文讀者可直接使用。此路徑由分岔檢查器視為 `README.md` 的語言鏡像。 | 上游 `README.md` 有產品能力變更時，同步更新繁中與英文版本；不得把簡中原文整份覆蓋到本檔。 |
| `AGENTS.md` | 簡體中文產品規則：自訂行業、執行檢查、架構邊界與程式碼風格。 | 繁中化並加入本 fork 的 GitHub 邊界、分岔檢查、上游水位紀錄與直接推 main 工作流；保留上游全部有效規則（含 `site/`／`modules/` 分層、遷移約定與測試守行為）。 | `AGENTS.md` 是所有 coding agent 的單一真相源，必須同時承載產品規則與 fork 邊界。 | 上游新增規則時人工合併並翻成繁中；Fork 邊界保持不動。若上游規則已被新架構淘汰，依新版本更新，不為零 diff 保留舊規則。 |
| `CLAUDE.md` | 一行 `@AGENTS.md`。 | 已刪除；原補充內容併入 `AGENTS.md`。 | 只維護業界通用的 `AGENTS.md`；Claude Code 在沒有 `CLAUDE.md` 時直接讀 `AGENTS.md`。 | 不收回本檔；上游若改成實質規則，將有效內容併入 `AGENTS.md`。 |
| `packages/backend/package.json` | 依賴 `zod: 4.6.5`（其餘與本 fork 一致）。 | `zod` 升至 `4.6.7`。 | 安全修補（GHSA-mrhx-c7xc-m3w5）。 | 上游的 `zod` 已 ≥ `4.6.6` 時刪除此列，否則保留。 |
| `apps/api/package.json` | 依賴 `zod: 4.6.5`。 | `zod` 升至 `4.6.7`。 | 安全修補（GHSA-mrhx-c7xc-m3w5）。 | 上游的 `zod` 已 ≥ `4.6.6` 時刪除此列，否則保留。 |
| `package-lock.json` | 上游 lockfile（`undici` 7.30.0、`fast-uri` 3.1.8／4.2.1、`zod` 4.6.5）。 | 依本 fork manifest 重生；傳遞依賴 `undici`（cheerio 底下）升至 `7.30.1`、`fast-uri` 升至 `3.1.9`／`4.2.3`，`zod` 4.6.7。 | 清除 `npm audit` 全部項目（GHSA-xjj6-f33q-929c 等）。 | 整樹同步時以上游 lockfile 為底，重做 `npm install --package-lock-only` 與 `npm audit`；上游已含這些版本時刪除此列。 |
| `apps/web/tests/article-outline.test.ts` | WebKit browser launch 在 fixture cleanup 區塊外。 | 將 launch 納入既有 `try/finally`，失敗仍關閉本機 fake API 與 web server。 | 避免缺少瀏覽器時測試程序遺留 localhost server。 | 上游含等價 cleanup 時刪除此列。 |
| `apps/web/app/routes/item.tsx` | 目錄邊界鍵盤攔截只呼叫 `preventDefault`。 | 在 capture phase 攔截，且於雙動畫畫格後恢復頁面捲動位置。 | WebKit 仍可能在已 prevented 的 nested-scroll 邊界鍵盤事件後捲動文件。 | 上游以等價方式維持目錄邊界不連鎖捲動時刪除此列。 |
| `apps/web/app/features/feed/FeedItem.tsx` | Phone card→item 導覽一律啟用 React Router view transition。 | Phone card 導覽停用 view transition，desktop 保留。 | WebKit 可使 deferred item route 的 view-transition update callback 逾時，URL／router 已返回 list 但 DOM 仍停在 reader。 | 上游含等價 phone fallback 時刪除此列。 |
| `apps/web/tests/navigation-performance.test.ts` | 深讀返回只驗證 cards、anchor 與日期折疊。 | 加驗 router 已回 home，並拒絕 WebKit view-transition callback timeout。 | 鎖定 URL/router 與 DOM 分岔的回歸。 | 上游涵蓋等價 router/DOM 與 pageerror 回歸時刪除此列。 |
| `packages/backend/src/publication/agent.ts` | `linkText` 只跳脫 `[`、`]`。 | 連反斜線一起跳脫。 | 外部來源的標題結尾若是 `\`，會把收尾的 `]` 變成字面字元：標題 `x\](https://evil.example)` 在給 AI 的 Markdown 裡造出一個指向外部的連結（CodeQL #13；`tests/fork-security-fixes.standalone.test.ts`）。 | 上游的 `linkText` 也跳脫 `\` 時刪除此列。 |
| `packages/contracts/src/http-policy.ts` | prefix 轉址以 `location.replace("*", 路徑尾段)` 組新位址。 | 改用 `replaceAll("*", () => 路徑尾段)`。 | 字串形式的替換值會解讀 `$&`、`` $` ``、`$'`：``/sources/a$`b`` 轉成 `/admin/sources/a/admin/sourcesb`（CodeQL #15；`tests/fork-security-fixes.standalone.test.ts`）。 | 上游以函式或等價方式把路徑當資料替換時刪除此列。 |
