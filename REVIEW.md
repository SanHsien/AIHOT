# 專案覆核紀錄（REVIEW.md）

> 覆核日期：2026-10-28（上游同步至 `79d962e`）
> 覆核範圍：上游 `ce83484..79d962e`（PR #273–#275）同步、41 筆 CodeQL 逐筆判讀、fork 自有程式（`tools/`、`scripts/`、`.github/workflows/`、fork 的前端修正）深度掃描；前一輪為 `cc66cce..ce83484` 整樹同步
> 維持方式：latest-only（只留最新覆核現狀）

---

## 覆核結論

- **狀態**：合格（PASS）；後端整合測試與瀏覽器測試本機缺 PostgreSQL／Playwright WebKit，交由 CI 驗證。
- **分支與版本衛生**：本 fork 與上游均只有 `main`；兩邊皆無 tag／release。殘留分支 `ci/job-names-20261024`、`security/alerts-20261024`、`tmp-probe-delete` 已於 2026-10-25 清除。
- **上游同步**：上游差量 3-way 套到 fork 樹，整批採納；判準八（隱藏內容）對整份差量與 66 個未合併 PR 的現行 head 掃描無隱藏載荷。
- **舊移植撤回**（2026-10-25）：PR #79（路徑正規化）、#83（`summaryIsBody`）、#85（`initialBackfillOnly`）上游已各自等效解決（`50b562b` 等），fork 改採上游版，`initialBackfillOnly` 開關移除。
- **上游審查機制**：[`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 [`tools/upstream_baseline.json`](tools/upstream_baseline.json)（commit `79d962e`、PR #275、issue #271、open PR #263、open issue #261／#267）。
- **CodeQL**（2026-10-28）：41 筆全在上游持有檔案；3 個真缺陷修掉並加分岔列與回歸測試，其餘逐筆附理由關閉，判讀見 [`docs/DECISIONS.md`](docs/DECISIONS.md) 第 9 條。
- **分岔登記**：14 筆上游持有檔案分岔全數登記於 [`docs/DIVERGENCE.md`](docs/DIVERGENCE.md)，機械檢查通過。

---

## 驗證證據清單

| 驗證項目 | 執行指令 | 實際結果 | 證據所屬 SHA / CI Run |
|---|---|---|---|
| Node.js 依賴鎖定 | `npm ci` | 成功（CI 以 `--no-audit` 執行；本機 2026-10-29 `npm audit --package-lock-only` 為 0 項，無 run 證據） | `f10c456`（Check run 40745313346） |
| TypeScript 型別檢查 | `npm run typecheck` | 0 error | `f10c456`（Check run 40745313346、Fork Quality run 40745313375） |
| 前端 SSR 建置 | `npm run build -w @aihot/web` | 成功 | `f10c456`（Check run 40745313346、Fork Quality run 40745313375） |
| 前端測試（含瀏覽器） | `node --test apps/web/tests/*.test.ts` | 64 筆 PASS（本機非瀏覽器項目通過、瀏覽器項目缺 WebKit；CI 64 筆全綠） | `f10c456`（Check run 40745313346） |
| 後端整合測試 | `DATABASE_URL=... npm test` | 950 筆 PASS（本機缺 PostgreSQL，交由 CI 驗證） | `f10c456`（Check run 40745313346） |
| rss 專屬測試 | `node --test tests/rss-summary-body.test.ts` | 1 筆 PASS | `f10c456`（Check run 40745313346） |
| 站點與 MCP 檢查 | `node scripts/smoke.ts` / `node scripts/mcp-check.ts` | all checks passed / MCP contract check passed | `f10c456`（Check run 40745313346） |
| 上游分岔比對 | `python tools/check_divergence.py` | 14 upstream files diverge, 14 registered（100% matched） | `f10c456`（Fork Quality run 40745313375；`94a3df1` run 40570939094） |
| 分岔檢查器合約測試 | `python tests/test_fork_divergence.py` | 8 筆 PASS | `f10c456`（Fork Quality run 40745313375；`94a3df1` run 40570939094） |
| 分岔依賴測試 | `python tests/test_dependency_freshness.py` | 2 筆 PASS | `f10c456`（Fork Quality run 40745313375） |
| 依賴新鮮度 | `python tools/check_dependency_freshness.py` | exit 0（setup-node 為已登記延後） | `94a3df1`（Dependency freshness run 40570939136） |

---

## 風險評估與修復追蹤

| 風險項目 | 等級 | 風險說明 | 緩解措施 / 修復狀態 |
|---|---|---|---|
| 多餘遠端分支累積 | P1 | 殘留分支易導致維護漂移或誤開 PR | 只保留 `main`。**[已修復]** |
| 上游更新重做與遺漏 | P1 | 每次巡檢若無紀錄須重新逐筆閱讀 PR/issue | `docs/UPSTREAM.md` 與基準線水位已更新到 `ce83484`。**[已修復]** |
| 上游落後 124 commit、Upstream check 紅燈 | P1 | 水位停在 `cc66cce` | 整樹同步並推進水位。**[已修復]** |
| Windows 路徑架構測試報錯 | P1 | 反斜線造成架構比對失敗 | 上游已改 posix 路徑，移植撤回。**[已由上游解決]** |
| 短摘要 RSS 無效抓取 | P2 | 摘要短於 280 字被誤當 teaser | 上游已含 `summaryIsBody`。**[已由上游解決]** |
| 長 RSS 歷史灌入成本 | P1 | 第二次抓取灌入舊文（上游 Issue #86） | 上游 `50b562b` 內建 48 小時規則。**[已由上游解決]** |
| Reasoning 模型失敗 | P1 | `max_tokens` 不足（上游 Issue #88） | 上游 #105 處理推理額度；README 記載 `LLM_REASONING_TOKENS`。**[已由上游解決]** |
| Agent Markdown 連結文字可被外部標題截斷 | P1 | 標題結尾的 `\` 讓收尾 `]` 失效，造出指向外部的連結（CodeQL #13） | `linkText` 一併跳脫 `\`。**[已修復 `6668f48`，2026-10-28]** |
| 轉址路徑裡的 `$` 被當替換樣板 | P2 | ``/sources/a$`b`` 轉到 `/admin/sources/a/admin/sourcesb`（CodeQL #15） | 改用函式替換。**[已修復 `634f90d`，2026-10-28]** |
| 偽造來源位址可重置全站登入嘗試上限 | P1 | 嘗試表滿 5000 筆時連 `all` 計數一起清掉 | 只清各 IP 的筆數。**[已修復 `37b043e`，2026-10-28]** |
| CI 分岔檢查從未真正執行 | P1 | CI 沒有上游基準 commit，檢查器 `Skipping check.` 後 exit 0 | 缺基準改為 exit 2，`fork-check` 先抓上游 main。**[已修復 `4494983`，2026-10-28]** |
| 改名的上游檔案逃過分岔登記 | P2 | `git diff --name-status` 預設偵測改名，`R` 狀態未計入 | 加 `--no-renames`，`T` 也計入。**[已修復 `b23376b`，2026-10-28]** |
| `freshness-hold` 的 Action 報 CHECK FAILED | P2 | 文件寫明的暫緩機制反而讓 `--strict` 失敗 | 版本改從 ref 讀，暫緩列不算檢查失敗。**[已修復 `81cc213`，2026-10-28]** |
| Dependabot PR 清單失敗被當成「沒有」 | P2 | `gh` 失敗回 `[]`，工作流程照樣綠 | 失敗標 CHECK FAILED 並要求處理。**[已修復 `03d6fb9`，2026-10-28]** |
