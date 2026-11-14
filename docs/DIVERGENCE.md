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
| `apps/web/tests/article-outline.test.ts` | WebKit browser launch 在 fixture cleanup 區塊外。 | 將 launch 納入既有 `try/finally`，失敗仍關閉本機 fake API 與 web server。 | 避免缺少瀏覽器時測試程序遺留 localhost server。 | 上游含等價 cleanup 時刪除此列。 |
| `apps/web/app/routes/item.tsx` | 目錄邊界鍵盤攔截只呼叫 `preventDefault`。 | 在 capture phase 攔截，且於雙動畫畫格後恢復頁面捲動位置。 | WebKit 仍可能在已 prevented 的 nested-scroll 邊界鍵盤事件後捲動文件。 | 上游以等價方式維持目錄邊界不連鎖捲動時刪除此列。 |
| `apps/web/app/features/feed/FeedItem.tsx` | Phone card→item 導覽一律啟用 React Router view transition。 | Phone card 導覽停用 view transition，desktop 保留。 | WebKit 可使 deferred item route 的 view-transition update callback 逾時，URL／router 已返回 list 但 DOM 仍停在 reader。 | 上游含等價 phone fallback 時刪除此列。 |
| `apps/web/tests/navigation-performance.test.ts` | 深讀返回只驗證 cards、anchor 與日期折疊。 | 加驗 router 已回 home，並拒絕 WebKit view-transition callback timeout。 | 鎖定 URL/router 與 DOM 分岔的回歸。 | 上游涵蓋等價 router/DOM 與 pageerror 回歸時刪除此列。 |
| `packages/backend/src/publication/agent.ts` | `linkText` 只跳脫 `[`、`]`；`itemLines` 時間只輸出 `publishedAt`／`discoveredAt`。 | 連反斜線一起跳脫；`itemLines` 輸出站內時間（`timelineAt`），差距 ≥ 1 分鐘另列原文發布時間，`BRIEF_HINTS` 提示依站內時間過濾。 | 外部來源的標題結尾若是 `\`，會把收尾的 `]` 變成字面字元：標題 `x\](https://evil.example)` 在給 AI 的 Markdown 裡造出一個指向外部的連結（CodeQL #13；`tests/fork-security-fixes.standalone.test.ts`）；服務端以站內時間判斷視窗與排序，agent 文字若只印發布時間會使時間窗過濾誤刪條目（上游 #194 同類缺陷，見 docs/UPSTREAM.md #194 條目；回歸測試在 `tests/fork-security-fixes.standalone.test.ts`）。 | 上游的 `linkText` 也跳脫 `\` 且支援站內時間輸出時刪除此列。 |
| `packages/backend/src/publication/items.ts` | `ApiItemRow` 與 `API_ITEM_COLUMNS` 未選取 `timeline_at`。 | `ApiItemRow` 與 `API_ITEM_COLUMNS` 包含 `p.timeline_at`。 | 供 v1 items 公開讀取層產生帶有 `timelineAt` 的 payload（上游 #194 同類缺陷，見 docs/UPSTREAM.md #194 條目；回歸測試在 `tests/fork-security-fixes.standalone.test.ts`）。 | 上游公開讀取層包含 `timeline_at` 時刪除此列。 |
| `packages/backend/src/publication/publish.ts` | `V1ItemPayload` 與 `v1Payload` 僅含 `publishedAt` 與 `discoveredAt`。 | `V1ItemPayload` 與 `v1Payload` 新增可選 `timelineAt`，`syncLedger` 同步帶入 `timeline_at`。 | 讓公開契約與 agent 輸出能取得條目在站內時間軸上的時間（上游 #194 同類缺陷，見 docs/UPSTREAM.md #194 條目；回歸測試在 `tests/fork-security-fixes.standalone.test.ts`）。 | 上游在 `V1ItemPayload` 提供等價 `timelineAt` 時刪除此列。 |
| `packages/backend/src/publication/v1.ts` | `rowToV1` 轉換未傳遞 `timeline_at`。 | `rowToV1` 將 `row.timeline_at` 傳入 `v1Payload` 的 `timelineAt`。 | 使 v1 API 與 agent 讀取層的項目資料帶有站內時間（上游 #194 同類缺陷，見 docs/UPSTREAM.md #194 條目；回歸測試在 `tests/fork-security-fixes.standalone.test.ts`）。 | 上游 `rowToV1` 傳入等價欄位時刪除此列。 |
| `site/public/openapi-v1.json` | `Item` schema 僅定義 `publishedAt` 與 `discoveredAt`。 | `Item` schema 的 properties 新增可選 `timelineAt`（`format: date-time`）。 | 對齊 v1 API 公開契約擴充的 `timelineAt` 欄位（上游 #194 同類缺陷，見 docs/UPSTREAM.md #194 條目；回歸測試在 `tests/fork-security-fixes.standalone.test.ts`）。 | 上游 OpenAPI 包含等價定義時刪除此列。 |
| `packages/contracts/src/http-policy.ts` | prefix 轉址以 `location.replace("*", 路徑尾段)` 組新位址。 | 改用 `replaceAll("*", () => 路徑尾段)`。 | 字串形式的替換值會解讀 `$&`、`` $` ``、`$'`：``/sources/a$`b`` 轉成 `/admin/sources/a/admin/sourcesb`（CodeQL #15；`tests/fork-security-fixes.standalone.test.ts`）。 | 上游以函式或等價方式把路徑當資料替換時刪除此列。 |
| `apps/api/src/routes/admin-auth.ts` | 嘗試表超過 5000 筆時 `attempts.clear()`。 | 只清各 IP 的筆數，保留全站 `all` 計數。 | `trustProxy: true` 下 `X-Forwarded-For` 可偽造：用 5000 個不同位址各送一次，就把全站「50 次／15 分鐘」上限一起清掉，與註解「位址偽造時全站上限仍成立」相反（判讀 CodeQL #42／#43 時發現；`tests/fork-security-fixes.standalone.test.ts`）。 | 上游修剪表格時保留全站計數，就刪除此列。 |
| `.gitignore` | 不含 `upstream-review-report.md`。 | 末尾加入 `upstream-review-report.md`。 | `tools/check_upstream_updates.py` 預設把報告寫到目前目錄（通常是 repo 根目錄），不忽略就在工作樹留下未追蹤檔。 | 上游同樣忽略該檔案，或上游持有等價的審查工具輸出時刪除此列。 |
| `packages/backend/src/operations/baidu-push.ts` | 端點寫死 `http://data.zz.baidu.com/urls`；`reply.remain` 只驗 `typeof === "number"`；請求迴圈無次數與時間上限。 | 啟用時先 `secureEndpoint(config.baiduPushEndpoint)`，非 https 即拒絕；請求與回覆判讀改走 fork 新增的 `operations/baidu-push-guard.ts`（拒絕轉址、`remain` 必須是非負安全整數、單輪最多 50 次請求與 5 分鐘、空批次直接失敗）；持久化的舊 `remain` 同樣驗證，不合法則丟棄並以 1 筆重新探測。 | 負的或小數的 `remain` 會讓下一批為空而無限 POST，token 以明文 HTTP 的 query string 送出（Codex 覆核 F2／F1，2026-11-11；`tests/baidu-push-guard.standalone.test.ts`、`tests/baidu-push.test.ts`）。 | 上游改用 https 端點、驗證 `remain` 並限制單輪請求時刪除此列與 guard 檔；上游只改其一則保留本列，逐項對照。 |
| `packages/backend/src/config.ts` | 沒有 `baiduPushEndpoint`。 | 新增 `baiduPushEndpoint`（`BAIDU_PUSH_ENDPOINT`，預設為百度文件上的 http 位址，因此啟用時會被拒絕，直到明確設成 https）。 | 讓 https 端點可設定而不改程式；預設值不靜默送明文 token。 | 上游自行提供 https 端點設定時刪除此列。 |
| `.env.example` | 只列 `BAIDU_PUSH_ENABLED` 與 `BAIDU_PUSH_TOKEN`。 | 加註釋掉的 `BAIDU_PUSH_ENDPOINT` 與 https 要求說明。 | 與 `config.ts` 的新設定同步。 | 同 `config.ts` 列，一併刪除。 |
| `tests/baidu-push.test.ts` | 模擬 `http://` 端點。 | 夾具改設 https 端點，並加三個測試：拒絕明文端點、負／小數 `remain` 一次請求後失敗、儲存的非法 `remain` 被丟棄。 | 對應 `baidu-push.ts` 的 fork 修正（需要資料庫，本機沒有 PostgreSQL 時只由 CI／有庫環境執行）。 | 同 `baidu-push.ts` 列，一併處理。 |
| `packages/backend/package.json` | `fast-xml-parser` 釘 `5.11.1`。 | 釘 `5.12.0`（Dependabot #13，2026-11-15 在 main 連同鎖檔套用）。 | Dependabot PR 只改這個檔、沒更新根目錄的 `package-lock.json`，`npm ci` 因鎖檔不同步失敗；照 PR 內容在 main 改並重建鎖檔。 | 上游的 `fast-xml-parser` 升到 `5.12.0` 以上時改回上游版本並刪除本列。 |
| `package-lock.json` | 依上游 `packages/backend` 的 `fast-xml-parser@5.11.1` 解析。 | `npm install --package-lock-only` 重建：`fast-xml-parser` 5.12.0、`@nodable/entities` 3.1.0、`is-unsafe` 2.0.3、`strnum` 2.5.1；同時清掉 `apps/worker` 鎖檔項目裡已不在其 `package.json` 的 `@aihot/contracts`、`@aihot/industry`。 | 與上一列同一次更新。 | 跟上一列一起處理：上游升級後以上游鎖檔為準重建，並刪除本列。 |
