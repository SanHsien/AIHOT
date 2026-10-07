# Fork 維護說明

本專案 fork 自 [`KKKKhazix/AIHOT`](https://github.com/KKKKhazix/AIHOT)，沿用 MIT 授權與完整 Git 歷史。

## 維護目標

- 直接跟進上游產品主線，不為維持零差異而保留舊版。
- 對外文件以繁體中文為主，並提供完整英文 README。
- 在 Windows 11 原生環境提供可重現的一鍵驗證。
- 每筆上游持有檔案的差異都登記於 [`docs/DIVERGENCE.md`](docs/DIVERGENCE.md)，由 `tools/check_divergence.py` 強制一致。
- 上游 commit、PR、issue、branch、tag 與 release 的決定記在 [`docs/UPSTREAM.md`](docs/UPSTREAM.md)，水位記在 `tools/upstream_baseline.json`，避免重複審查。

## GitHub 邊界

- 日常修改通過驗證後直接推 `origin/main`，不保留工作分支或 fork 內 PR。
- 未經維護者在當次對話明確同意，不得向上游開 PR、Issue、發布 Release 或 push。
- 分支只保留 `main`。
- Release 與 tag 只保留最新一份；刪除舊項目前仍須確認最新版本可下載且 tag 指向正確 commit。

## 上游同步

1. Fetch 上游完整 refs，盤點 main、所有 PR／issue（含 closed）、branches、tags 與 releases。
2. 讀 diff 後在 `docs/UPSTREAM.md` 記錄採納、延後或拒絕，以及重新審查條件。
3. 合併適合的上游 main；只在缺陷仍存在、測試能證明且上游尚未合併時移植 PR。
4. 更新 `tools/upstream_baseline.json`，讓相同 SHA 與狀態不再重審。
5. 執行完整閘門；綠燈後 commit、push `origin/main`。

## Fork 新增檔案

- 雙語與治理：`README.en.md`、`FORK.md`、`NOTICE.md`、`SKILL.md`、`CHANGELOG*.md`、`REVIEW.md`。
- 維護文件：`docs/DEVELOPMENT.md`、`docs/DECISIONS.md`、`docs/DIVERGENCE.md`、`docs/UPSTREAM.md`。
- 維護工具：`tools/check_divergence.py`、`tools/upstream_baseline.json`、`tools/dev_check.ps1`、`tools/dev_check.sh`、`scripts/verify-env.py`。
- CI：`.github/workflows/fork-check.yml`。

核心產品程式碼、資料庫、Prompt 與部署流程原則上直接跟隨上游；本 fork 自行移植的上游 PR 必須在分岔表留下逐檔判準。
