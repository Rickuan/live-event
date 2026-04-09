# Skill: test

> 根據 test-plan artifact，生成測試程式碼並自動執行。
> 測試失敗時只回報結果，不自動修改程式碼。

## Trigger

```
/test @agent/artifacts/test-plan/{feature-name}.md
```

## Dependencies

| 參數 | 路徑 | 必要 |
|------|------|------|
| test-plan artifact | `agent/artifacts/test-plan/{feature-name}.md` | 是 |

## 測試框架

| 類型 | 框架 | 設定檔 |
|------|------|-------|
| 黑箱 / 白箱 | Jest | `jest.config.ts` |
| E2E | Playwright | `playwright.config.ts` |

Playwright 使用 `webServer` config 管理 dev server 生命週期，無需手動啟動。

## 測試檔案位置

| 測試範圍 | 路徑 |
|---------|------|
| 單一 function / unit | `{module}.test.ts`（與原檔同層） |
| 整個功能模組 | `src/.../{feature}/__tests__/{testCase}.test.ts` |
| E2E | `tests/e2e/{feature}.spec.ts` |

## Process

### Step 1：讀取 test-plan

分出黑箱、白箱、E2E 三類測試項目。

### Step 2：生成測試程式碼

依照測試類型和範圍，將程式碼寫至對應路徑。

### Step 3：執行測試

```bash
# 黑箱 / 白箱
jest --coverage

# E2E
playwright test
```

### Step 4：更新 test-plan checkbox

- 通過 → `[x]`
- 失敗 → `❌`

### Step 5：輸出測試結果 artifact

測試失敗時**只回報**，不自動修改程式碼。

## Output

**路徑：** `agent/artifacts/test-results/{feature-name}.md`

```markdown
# Test Results: {feature-name}

## Summary
| 類型 | 通過 | 失敗 | 略過 |
|------|------|------|------|
| Black Box | X | Y | Z |
| White Box | X | Y | Z |
| E2E       | X | Y | Z |

## Failed Tests
### {test name}
- **Error:** {error message}
- **Suggestion:** {可能的修正方向}

## Passed Tests
<details>
<summary>展開列表</summary>

- {test name}
- {test name}

</details>

<!-- Last updated: YYYY-MM-DD HH:MM -->
```
