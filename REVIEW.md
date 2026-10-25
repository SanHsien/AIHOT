# 專案覆核紀錄（REVIEW.md）

> 覆核日期：2026-10-25（上游同步至 `ce83484`）
> 覆核範圍：`SanHsien/AIHOT` 整樹同步上游 `cc66cce..ce83484`（124 commit，4.0.0 引擎／站點分層）、舊移植（#79、#83、#85）撤回、依賴稽核與分岔登記
> 維持方式：latest-only（只留最新覆核現狀）

---

## 覆核結論

- **狀態**：合格（PASS）；後端整合測試與瀏覽器測試本機缺 PostgreSQL／Playwright WebKit，交由 CI 驗證。
- **分支與版本衛生**：本 fork 與上游均只有 `main`；兩邊皆無 tag／release。殘留分支 `ci/job-names-20261024`、`security/alerts-20261024`、`tmp-probe-delete` 已於 2026-10-25 清除。
- **上游同步**：上游差量 3-way 套到 fork 樹，整批採納；判準八（隱藏內容）對整份差量與 66 個未合併 PR 的現行 head 掃描無隱藏載荷。
- **舊移植撤回**（2026-10-25）：PR #79（路徑正規化）、#83（`summaryIsBody`）、#85（`initialBackfillOnly`）上游已各自等效解決（`50b562b` 等），fork 改採上游版，`initialBackfillOnly` 開關移除。
- **上游審查機制**：[`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 [`tools/upstream_baseline.json`](tools/upstream_baseline.json)（commit `ce83484`、PR #269、issue #267、open PR #263）。
- **分岔登記**：7 筆上游持有檔案分岔全數登記於 [`docs/DIVERGENCE.md`](docs/DIVERGENCE.md)，機械檢查通過。

---

## 驗證證據清單

| 驗證項目 | 執行指令 | 實際結果 |
|---|---|---|
| Node.js 依賴鎖定 | `npm ci` | 成功；`npm audit` 0 項 |
| TypeScript 型別檢查 | `npm run typecheck` | 0 error |
| 前端 SSR 建置 | `npm run build -w @aihot/web` | 成功 |
| 前端測試（不含瀏覽器） | `node --test apps/web/tests/*.test.ts` | 非瀏覽器項目 PASS；瀏覽器項目本機缺 WebKit／新版 Chromium，以 CI 為準 |
| rss 專屬測試 | `node --test tests/rss-summary-body.test.ts` | 1 筆 PASS |
| 上游分岔比對 | `python tools/check_divergence.py` | 7 upstream files diverge, 100% matched |
| 分岔檢查器合約測試 | `python tests/test_fork_divergence.py` | 6 筆 PASS |
| 依賴新鮮度 | `python tools/check_dependency_freshness.py` | exit 0（setup-node 為已登記延後） |

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
