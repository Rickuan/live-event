# Skill: backend

> 根據 exec-plan，自動按順序實作後端程式碼。
> 每次執行處理一個未完成的 back/* 或 shared phase。
> shared scope 由本 skill 負責執行。

## Trigger

```
/backend @agent/artifacts/exec-plan/{feature-name}.md
```

## Dependencies

| 參數 | 路徑 | 必要 |
|------|------|------|
| exec-plan artifact | `agent/artifacts/exec-plan/{feature-name}.md` | 是 |

## Process

### Step 1：讀取 exec-plan

找出所有 scope 為 `back/*` 或 `shared` 的 phases，
取第一個包含未完成 task（`[ ]`）的 phase。

**shared scope 說明：**
shared phase 包含前後端共用的 TypeScript interface、型別定義、常數等。
由 backend skill 先定義，前端直接 import。

### Step 2：逐 task 實作程式碼

按照 task 順序依序實作。
每個 task 完成後立即更新 exec-plan 對應的 checkbox：`[ ]` → `[x]`

### Step 3：標記不確定之處

若 exec-plan 的描述不夠明確，在程式碼中標記：
```typescript
// TODO: confirm — {具體問題描述}
```
不自行假設，等 phase 結束後統一列出。

### Step 4：Phase 結束後確認 TODO

Phase 所有 tasks 完成後，列出本次所有 `TODO: confirm` 項目，
逐一請使用者確認後再繼續。

## Output

- 實作完成的程式碼檔案
- 更新後的 exec-plan artifact（checkbox 狀態）
- 不輸出獨立 artifact

## Test File Location

| 測試範圍 | 路徑 |
|---------|------|
| 單一 function / unit | `{module}.test.ts`（與原檔同層） |
| 整個功能模組 | `src/.../{feature}/__tests__/{testCase}.test.ts` |
