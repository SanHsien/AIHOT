# 專案覆核紀錄（REVIEW.md）

> 覆核日期：2026-10-04
> 覆核範圍：`SanHsien/AIHOT` 上游主線同步（公開介面 3.0.0）、分支清理、六軸審查紀錄與候選 PR 移植（#79、#83、#85）
> 維持方式：latest-only（只留最新覆核現狀）

---

## 覆核結論

- **狀態**：合格（PASS）
- **分支與版本衛生**：本 fork 與上游遠端均只保留 `main` 分支（多餘遠端分支 `origin/codex/article-body-fidelity-20261002` 已授權刪除）；上游與本 fork 目前均無任何 tag 或 release，無舊版本殘留。
- **上游同步與候選移植**：
  - 完整合併上游 main 3 筆新提交至 `cc66cce`（公開介面 3.0.0、正式站同步與評測修正）。
  - 移植 PR #79：修復 `tests/architecture.test.ts` 在 Windows 下反斜線導致架構規則假性報錯的缺陷。
  - 移植 PR #83：新增 `packages/backend/src/sources/rss.ts` 的 `summaryIsBody: true` 支援與測試。
  - 移植 PR #85：新增 `_aihot.initialBackfillOnly`，徹底解決長歷史 RSS 第二次抓取過量灌入舊文的成本問題（修復 Issue #86）。
  - 判定 PR #80 因上游 commit `5794327` 已移除 `deleteAllJobs` 而不需移植。
- **上游審查機制**：建立 [`docs/UPSTREAM.md`](docs/UPSTREAM.md) 與 [`tools/upstream_baseline.json`](tools/upstream_baseline.json) 六軸水位（commit `cc66cce`、PR #91、issue #88、branches `main`）。
- **分岔登記**：10 筆上游持有檔案分岔全數登記於 [`docs/DIVERGENCE.md`](docs/DIVERGENCE.md)，機械檢查通過。

---

## 驗證證據清單

| 驗證項目 | 執行指令 | 實際結果 |
|---|---|---|
| Node.js 依賴鎖定 | `npm ci --no-audit --no-fund` | 293 packages installed cleanly |
| TypeScript 型別檢查 | `npm run typecheck` | 6 個子專案檢查 0 error 通過 |
| 前端 SSR 建置 | `npm run build -w @aihot/web` | Client 與 SSR Server build 成功 |
| 前端單元測試 | `node --test apps/web/tests/*.test.ts` | 29 筆測試全數 PASS（0 fail） |
| PR #83 專屬測試 | `node --test tests/rss-summary-body.test.ts` | 1 筆測試全數 PASS（0 fail） |
| 上游分岔比對 | `python tools/check_divergence.py` | 10 upstream files diverge, 100% matched |
| 分岔檢查器合約測試 | `python tests/test_fork_divergence.py` | 6 筆測試全數 PASS（0 fail） |
| 遠端分支清理 | `git branch -a` | 僅剩 `main`，無殘留遠端分支 |
| Tag 與 Release 狀態 | `git tag && gh release list` | 確認目前無殘留 tag 與 release |

---

## 風險評估與修復追蹤

| 風險項目 | 等級 | 風險說明 | 緩解措施 / 修復狀態 |
|---|---|---|---|
| 多餘遠端分支累積 | P1 | 殘留分支易導致維護漂移或誤開 PR | 已刪除 `origin/codex/article-body-fidelity-20261002`，只保留 `main`。**[已修復]** |
| 上游更新重做與遺漏 | P1 | 每次巡檢若無紀錄須重新逐筆閱讀 PR/issue | 建立 `docs/UPSTREAM.md` 與 `tools/upstream_baseline.json` 六軸水位。**[已修復]** |
| Windows 路徑架構測試報錯 | P1 | 反斜線造成架構比對失敗 | 移植 PR #79 路徑正規化。**[已修復]** |
| 短摘要 RSS 無效抓取 | P2 | 摘要短於 280 字會被誤當 teaser 發起爬頁 | 移植 PR #83 `summaryIsBody: true` 放行短本文。**[已修復]** |
| 長 RSS 歷史灌入成本 | P1 | 新增長 RSS 信源可能於第二次抓取灌入上千筆舊文（上游 Issue #86） | 移植 PR #85 `_aihot.initialBackfillOnly`。**[已修復]** |
| Reasoning 模型失敗 | P1 | 深度思考模型因 max_tokens 不足導致 chatJson 輸出空白（上游 Issue #88） | 已於 `docs/UPSTREAM.md` 記錄 `LLM_EXTRA_JSON={"max_tokens":10000}` 方案。**[追蹤中]** |
