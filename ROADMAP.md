# 路線圖

> 本 repo 後續工作的單一真相源。做完一項，就在同一個 commit 刪掉那一列；新工作只加在這裡。
> 現況段的數字是 2026-10-29 依 `main` `94a3df150d2b` 查的快照，開工前先重查 GitHub。

## 現況
這是以信源採集、模型精選與自動成刊為核心的行業網站框架 fork（[AGENTS.md:3](AGENTS.md)）。2026-10-29 `gh` 查詢記錄各主要 workflow 最近結果成功、開啟中的安全告警為 0；issues 停用，未查到 issue（2026-10-29 `gh` 查詢）。安全修正與 CI 分岔檢查已有驗證，REVIEW 驗證證據表已校正，但上游紀錄仍殘留前一輪敘述（[docs/UPSTREAM.md:38](docs/UPSTREAM.md)）。

## 近期：可以直接動手
| 項目 | 為什麼 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 修正上游審查文件的零產品分岔前提 | 已有安全與導航修正，舊前提不再成立 | `docs/UPSTREAM.md` 的保留分岔與 closed PR 判準對齊 `docs/DIVERGENCE.md`；逐筆理由仍留在既有決策，不複製成本檔的待辦 | Codex | [docs/UPSTREAM.md:28](docs/UPSTREAM.md)、[docs/UPSTREAM.md:38](docs/UPSTREAM.md)；[docs/DECISIONS.md:63](docs/DECISIONS.md) |

## 中期：等條件成立再做
| 項目 | 觸發條件 | 驗收方式 | 建議執行者 | 證據 |
| --- | --- | --- | --- | --- |
| 重評全文譯文入口 | 上游 #263 head 或狀態變動，或 #261 有結論 | 讀現行 diff 與寫入邊界，採用須通過型別、網頁、後端整合及分岔檢查；未採用則記具體理由 | Codex | [docs/UPSTREAM.md:34](docs/UPSTREAM.md)、[docs/UPSTREAM.md:44](docs/UPSTREAM.md) |
| 處理分享圖缺字 | 上游 #267 出現實作，或 fork 實際分享圖缺字 | 用原缺字文字重產分享圖，字形可見、既有圖像流程正常 | Codex | [docs/UPSTREAM.md:45](docs/UPSTREAM.md) |
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
