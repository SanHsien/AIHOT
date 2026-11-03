# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `94a3df150d2b` 查的快照，開工前先重查 GitHub。

## 現況
這是以信源採集、模型精選與自動成刊為核心的行業網站框架 fork（[AGENTS.md:3](AGENTS.md)）。2026-10-29 `gh` 查詢記錄各主要 workflow 最近結果成功、開啟中的安全告警為 0；issues 停用，未查到 issue（2026-10-29 `gh` 查詢）。安全修正與 CI 分岔檢查已有驗證，REVIEW 驗證證據表已校正；上游審查文件已對齊現行安全與導航分岔，closed PR 依實際缺陷與分岔變動重審（[docs/UPSTREAM.md](docs/UPSTREAM.md)）。Agent 輸出已支援站內時間（`timelineAt`）並附時間過濾提示，V1 契約與回歸測試已補齊。

2026-11-03：以 `92d91d7` 為起點整樹採納上游 `79d962e..41cee09`（48 個 commit、7 個新增遷移），保留已登記安全、導航與站內時間分岔；其後追加採納 #323 合併的 `dcb366e`、`cd424b0`（Menu 鍵盤導航）；commit 水位為完整 `cd424b0a513c7c8535b6f291b106a3086d6b75bf`，PR 水位 #332，無追蹤中的 open PR。Node.js 24.22.1 的完整本機閘門通過（`27ced027`：網頁 65/65、standalone 249/249、分岔契約 9/9；追加採納 `cd424b0` 後 `dev_check` 網頁 67/67、分岔契約 9/9），上游 `--strict` exit 0；本機無可用 `_test`／`_ci` PostgreSQL（5432 無監聽）。2026-11-03 `27ced027` 推送後的 [check.yml run 41619101964](https://github.com/SanHsien/AIHOT/actions/runs/41619101964)：`check`、`docker` 兩個 job 均成功，該 job 的 PostgreSQL 是空庫（`aihot_ci`），驗到的是全新安裝；7 個遷移（0090、0091、0092、0105、0121、0122、0123）對既有資料庫的升級路徑未驗證。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 驗證 7 個新遷移對既有資料庫的升級 | CI 只跑空庫全新安裝，0090-0123 範圍內的 7 個新遷移（0090、0091、0092、0105、0121、0122、0123）沒有在已有資料的庫上執行過 | 取得名稱以 `_test` 或 `_ci` 結尾、內容為既有已填資料資料庫的 PostgreSQL 副本，執行遷移並記錄輸出（新增欄位與三個 `CONCURRENTLY` 索引全部套用、無錯誤），再以該庫執行 `npm test` 全綠 | 維護者提供副本，Codex 執行 | [AGENTS.md:35](AGENTS.md)、[AGENTS.md:58](AGENTS.md)、[docs/UPSTREAM.md](docs/UPSTREAM.md) |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 建立自訂行業站與選文校準 | 維護者確認品牌、信源、條款與標註樣本 | 依 customize 與 selection 文件完成設定、跑標註評測與本機 smoke；開啟外部採集及付費模型前確認預算 | 維護者 | [AGENTS.md:20](AGENTS.md)、[AGENTS.md:22](AGENTS.md)、[README.md:94](README.md) |
| 收斂上游已修好的 fork 補丁 | 上游修改對應安全或導航檔案 | 比較分岔行為，等效修正才刪 fork 補丁與登記列；相關回歸及 `python tools/check_divergence.py` 通過 | Codex | [docs/DECISIONS.md:63](docs/DECISIONS.md)、[AGENTS.md:12](AGENTS.md) |

## 刻意不做
| 不做什麼 | 理由 | 什麼情況下重新考慮 |
| --- | --- | --- |
| 重開已逐筆判讀的 CodeQL 項目或採用未發布安全候選整包 | 判讀與修正依 [docs/DECISIONS.md:41](docs/DECISIONS.md)；未採用的候選（ingest `Bearer` 手寫解析、static.ts 拿掉快取、json-list 改 cheerio、init-env `flag: "wx"`）經判讀為送不進的 ReDoS、已被正則擋住的誤報或 won't fix，判讀見 [docs/DECISIONS.md:41](docs/DECISIONS.md) | 新告警或 source/sink、防護邊界改變 |
| 為無共同祖先改寫歷史 | 歷史壓縮已知，採用基準差量套用即可 | 維護者另立歷史遷移需求 |
| 為測試開啟外部採集、模型與通知 | 安全閥與費用邊界見 [AGENTS.md:30](AGENTS.md)、[AGENTS.md:31](AGENTS.md) | 獲准執行有停止條件的實機驗收 |

## 維護方式
依 [tools/upstream_baseline.json](tools/upstream_baseline.json) 做增量巡檢；只有新 commit、追蹤 PR head、issue 狀態或 release 改變才重審，判斷記 [docs/UPSTREAM.md](docs/UPSTREAM.md)。依賴更新沿用 freshness 與安全告警流程；同步後跑 [AGENTS.md](AGENTS.md) 指定檢查，完整後端與瀏覽器驗證可沿用對應 SHA 的 CI 證據。
