# CLAUDE.md — Claude Code 薄補丁

> 本檔案為 Claude Code 專屬薄補丁。
> **通用規則與單一真相源見 [`AGENTS.md`](AGENTS.md)**，此處不重複維護共通架構與程式碼規範。

---

## 互動風格與基本規則

1. **單一真相源**：所有架構規範、協作邊界與硬性規則請參照 `AGENTS.md`。
2. **溝通語言**：繁體中文（術語與程式碼識別符維持原文）。
3. **精簡模式**：先結論後細節，去除冗贅客套，工具輸出先消化再以白話結論回報。
4. **Git 工作流**：驗證通過後直接 commit + push `origin main`，不開 PR、不開分支；對外只打 `SanHsien/AIHOT`。
5. **分岔必登記**：修改上游持有檔案時，同步更新 `docs/DIVERGENCE.md`，並執行 `python tools/check_divergence.py` 驗收。

## 關鍵驗收指令

```bash
npm run typecheck
npm run build -w @aihot/web
node --test apps/web/tests/*.test.ts
python tools/check_divergence.py
```
