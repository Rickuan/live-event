# Skill: test-plan

> 根據 PM 需求與工程規格，分別定義黑箱、白箱、E2E 測試文件。
> 只產文件，不產程式碼。

## Trigger

```
/test-plan @agent/artifacts/pm/{feature-name}.md
           @agent/artifacts/exec-plan/{feature-name}.md
```

## Dependencies

| 參數 | 路徑 | 必要 |
|------|------|------|
| PM artifact | `agent/artifacts/pm/{feature-name}.md` | 是 |
| exec-plan artifact | `agent/artifacts/exec-plan/{feature-name}.md` | 是 |

## 三類測試的職責分工

| 類型 | 框架 | 來源 | 驗證對象 |
|------|------|------|---------|
| 黑箱測試 | Jest | exec-plan | 函式的輸入輸出，不管內部實作 |
| 白箱測試 | Jest | exec-plan | 內部邏輯、邊界條件、實作細節 |
| E2E 測試 | Playwright | PM artifact | 使用者操作流程、商業邏輯 |

## Process

### Step 1：讀取兩份 artifact

- 從 exec-plan 提取各 module 的功能描述 → 產生黑箱與白箱測試
- 從 PM Requirements 提取使用者需求 → 產生 E2E 測試

### Step 2：生成三類測試項目

每個測試條目必須是可獨立執行、結果明確的情境。

### Step 3：輸出 artifact

## Output

**路徑：** `agent/artifacts/test-plan/{feature-name}.md`

```markdown
# Test Plan: {feature-name}

## Black Box Tests（Jest）
函式 I/O 驗證，不關心內部如何實作。

### {Module Name}
- [ ] Test: {描述}
      Input:    {輸入值}
      Expected: {預期輸出}

## White Box Tests（Jest）
內部邏輯與邊界條件驗證。

### {Module/Function Name}
- [ ] Test: {描述}
      Input:    {輸入值}
      Expected: {預期輸出或行為}
      Edge case: {邊界條件說明}

## E2E Tests（Playwright）
操作流程與商業邏輯驗證。

### {User Story / 功能名稱}
- [ ] Test: {描述}
      Given:  {前置條件}
      When:   {使用者操作}
      Then:   {預期結果}

<!-- Last updated: YYYY-MM-DD HH:MM -->
```
