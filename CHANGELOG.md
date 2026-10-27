# 變更紀錄（CHANGELOG）

本檔案遵循 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.0.0/) 格式，並採用 [語意化版本（Semantic Versioning）](https://semver.org/lang/zh-TW/) 規則。
僅記錄本 Fork（SanHsien/AIHOT）自身的架構改動、維護與在地化變更；上游原版的改動請參閱上游 releases。

## [Unreleased]

### Changed
- 同步上游 `ce83484..79d962e`（PR #273–#275）：告警可改走群組機器人 Webhook（`FEISHU_ALERT_WEBHOOK_URL`）、日報跨年日期帶年份、登入頁路徑辨識補 Devise／WordPress／副檔名。
- 同步上游 `cc66cce..ce83484`（124 個 commit，4.0.0 引擎／站點分層、遷移約定、安全邊界與採集修正）；README、AGENTS 併入新結構並維持繁中。
- 撤回 fork 先前移植的 PR #79／#83／#85：上游已各自解決（見 `docs/UPSTREAM.md`），分岔列刪除；`_aihot.initialBackfillOnly` 開關移除，行為改採上游內建規則。
- 刪除 `CLAUDE.md`，補充內容併入 `AGENTS.md`；所有 agent 只讀 `AGENTS.md`。

### Security
- 修上游持有程式的三個缺陷（分岔列見 `docs/DIVERGENCE.md`）：Agent Markdown 的連結文字補跳脫反斜線，外部標題不能再造出連結（CodeQL #13）；prefix 轉址把路徑當資料替換（CodeQL #15）；登入嘗試表修剪時保留全站計數，偽造 `X-Forwarded-For` 不能重置上限。
- 其餘 39 筆 CodeQL 告警逐筆附 source/sink 理由關閉，判讀見 `docs/DECISIONS.md` 第 9 條。

### Fixed
- `fork-check` 的分岔檢查過去從未真正執行（CI 沒有上游基準 commit，檢查器印 `Skipping check.` 後 exit 0）：缺基準改回 exit 2，workflow 先抓上游 main。
- `check_divergence.py` 把被改名的上游檔案也算成分岔（原本 `R` 狀態會漏掉）。
- `check_dependency_freshness.py`：加了 `# freshness-hold:` 的 Action 顯示 `HELD`，不再報 `CHECK FAILED`。
- `dependency-freshness` workflow：列 Dependabot PR 失敗時標為 `CHECK FAILED`，不再當成「沒有 PR」。
- 提前採納上游安全修補 commit `e4478cb`、`879afa3`、`14fe1da`、`31fa181`：
  - 升級 `source-map-js` 至 1.2.2（修復 GHSA-68fv-2mgg-jv7q DoS 漏洞）。
  - 升級 `@modelcontextprotocol/client` 至 2.2.0（修復 GHSA-6qxp-vccf-f47h 憑證外洩漏洞）。
  - 升級 `sharp` 至 0.35.5（修復 GHSA-wq5f-xc86-pv6w librsvg 依賴漏洞）。

### Added
- 初始化 Fork 鷹架結構與開發標準：
  - `AGENTS.md`：AI Coding Agent 單一真相源與個人協作約定。
  - `CLAUDE.md`：Claude Code 薄補丁（繁體中文、精簡輸出、驗證指引）。
  - `FORK.md`：Fork 宗旨、上游追蹤原則與回貢判準。
  - `NOTICE.md`：授權條款、品牌限制與第三方素材聲明。
  - `SKILL.md`：專案 Agent 技能合約。
  - `docs/DIVERGENCE.md`：上游持有檔案分岔登記表。
  - `docs/DEVELOPMENT.md`：本地開發、環境前置與測試指令指南。
  - `docs/DECISIONS.md`：維護決策記錄。
  - `REVIEW.md`：首期質量覆核報告與驗收記錄。
  - `tools/upstream_baseline.json`：上游基準 Commit（`04846072`）標記。
  - `tools/check_divergence.py`：分岔自動化比對驗證器。
  - `tools/dev_check.ps1`：本地一鍵品質檢查腳本。
  - `scripts/verify-env.py`：本機環境依賴前置檢查。
  - `.gitattributes`：設定 `* text=auto eol=lf` 避免跨平台換行問題。
  - `README.en.md`：保留上游原版鏡像。
- 翻轉 `README.md` 為完整繁體中文版，並補齊 Fork 導引與開發指引。

### Changed
- 合併上游 `main` 至 `cc66cce`：正式站核心同步、公開介面 3.0.0、日週月報流程、主題編年史、模型榜 v17、手機版重寫與兩筆後續修正。
- 更新繁中／英文 README，使內容對齊上游最新產品能力。
- 建立 `docs/UPSTREAM.md` 六軸審查紀錄與可重審條件；更新 `tools/upstream_baseline.json` 水位。
- 清除遠端分支 `codex/article-body-fidelity-20261002`；本 fork 與上游均只保留 `main`。
- 移植上游 PR #83：RSS 信源支援 `summaryIsBody: true` 放行短摘要作為本文，新增 `tests/rss-summary-body.test.ts`。
- 移植上游 PR #85：信源支援 `_aihot.initialBackfillOnly`，解決長歷史 RSS 第二次抓取過量灌入舊文之成本問題（Issue #86）。

### Fixed
- 移植上游 PR #79：修復 `tests/architecture.test.ts` 在 Windows 原生反斜線路徑下導致模組所屬權比對假性失敗的缺陷。
