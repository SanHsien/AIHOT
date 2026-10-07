# 架構與維護決策記錄（DECISIONS.md）

本文件遵循精簡原則，僅記錄現行決定與一行理由。

---

## 決策清單

1. **以繁體中文作為主入口文件語言（`README.md`、`AGENTS.md`、`CLAUDE.md`、`docs/*.md`）**
   - **現行決定**：核心文件全面採用繁體中文，上游原版英文/簡中鏡像完整保留在 `README.en.md`。
   - **理由**：符合本機主要維護者溝通習慣，並便於台灣業界與個人熱點站落地。

2. **追蹤上游最新進展，分岔處嚴格登記於 `docs/DIVERGENCE.md`**
   - **現行決定**：接受隨維護深入必然產生的分岔，所有對上游持有檔之變更均登載於分岔表，並由 `tools/check_divergence.py` 機器強制比對。
   - **理由**：避免每次同步上游時遺失判斷脈絡，以機器檢查杜絕文件腐爛。

3. **協作流程採「做完就 push 到 main、不開分支、不開 PR」**
   - **現行決定**：個人維護線全部在 `origin/main` 進行，驗證通過直接 push，不留常駐分支。
   - **理由**：個人專案無需多餘分支審查摩擦，push 即為可靠備份。

4. **對外只打 `SanHsien/AIHOT`，禁止未經授權對上游開 PR**
   - **現行決定**：`gh repo set-default SanHsien/AIHOT`，所有 GitHub 操作限定在本 Fork 內。
   - **理由**：防範維護骨架與客製變更誤提至上游公共倉庫。

5. **全庫設定 `.gitattributes` 強制 `eol=lf`**
   - **現行決定**：根目錄設定 `* text=auto eol=lf`。
   - **理由**：避免 Windows 原生環境因 CRLF 導致 lint、diff 或 shell 解析誤報。

6. **開發與測試預設關閉模型與采集安全閥**
   - **現行決定**：單元測試與一般本機建置強制 `COLLECT_ENABLED=false` 與 `MODEL_CALLS_ENABLED=false`。
   - **理由**：防止本機測試非預期消耗外部付費 API 額度。

7. **分支只留 `main`；release 與 tag 只留最新一份**
   - **現行決定**：合併或結案後刪除工作分支；發布新版本並驗證成功後，移除較舊 release 與 tag。
   - **理由**：維持個人維護線簡潔，避免過期分支與重複發布物造成誤用。

8. **上游審查採六軸紀錄，不重做相同判斷**
   - **現行決定**：commit、PR、issue、branch、tag、release 的決策寫在 `docs/UPSTREAM.md`，SHA／狀態水位寫在 `tools/upstream_baseline.json`。
   - **理由**：相同 head 與狀態不應每次巡檢重新閱讀；只有內容或狀態改變才重審。
