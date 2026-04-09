# Skill: commit

> 將 exec-plan 中已完成但尚未 commit 的 tasks 打包成 commit。
> 必須經過使用者確認 commit message 後才執行，不自動 push。

## Trigger

```
/commit @agent/artifacts/exec-plan/{feature-name}.md
```

## Dependencies

| 參數 | 路徑 | 必要 |
|------|------|------|
| exec-plan artifact | `agent/artifacts/exec-plan/{feature-name}.md` | 是 |

## Commit Message 規範

格式：`{type}({scope}): {description}`（純英文）

### Types
| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修正 |
| `refactor` | 重構（不影響行為） |
| `test` | 測試相關 |
| `docs` | 文件 |
| `chore` | 工具、設定、依賴更新 |
| `style` | 格式調整（不影響邏輯） |

### Scopes
| Scope | 用途 |
|-------|------|
| `front/cards` | 活動卡片元件 |
| `front/filter` | 篩選 UI |
| `front/calendar` | Calendar view UI |
| `front/layout` | 全域 layout |
| `back/scraper` | 爬蟲引擎 |
| `back/parser` | 資料清洗與正規化 |
| `back/db` | Schema、migration、model |
| `back/api` | API endpoints |
| `back/calendar` | Google Calendar 整合 |
| `shared` | 前後端共用型別與常數 |
| `agent` | agent config、skills |

## Branch 命名

| 情境 | 格式 | 範例 |
|------|------|------|
| 新功能 | `feat/{feature-name}` | `feat/event-scraper` |
| 修復 | `fix/{issue-slug}` | `fix/missing-price-field` |
| 重構 | `refactor/{scope}` | `refactor/parser` |

## Process

### Step 1：讀取 exec-plan

找出所有 `[x]` 完成但尚未 commit 的 tasks。

### Step 2：打包 commit 單位

依照 phase 的 scope 與 commit-type 決定如何打包。

**500 行限制檢查：**
若預計打包的變更超過 500 行，停止並回報：
```
⚠️  本次變更估計超過 500 行（約 {N} 行）。

建議拆分方式：
1. 先 commit Task {N.1} + {N.2}（約 {X} 行）
2. 再 commit Task {N.3}（約 {Y} 行）

請確認拆分方式後重新執行 /commit。
```

### Step 3：確認 branch

檢查目前是否在正確 branch。若 branch 不存在，從 `main` 建立：
```bash
git checkout -b {branch-name}
```

### Step 4：展示 commit message，等待確認

向使用者展示 commit message（純英文），等待確認後才執行。

```
Proposed commit message:
─────────────────────────────
{type}({scope}): {description}

Tasks completed:
- Task N.1: {description}
- Task N.2: {description}

Agent-generated commit
─────────────────────────────
Confirm? [y/n]
```

### Step 5：執行 commit（確認後）

```bash
git add {相關檔案}
git commit -m "{message}"
```

### Step 6：不 push

Push 由使用者手動執行或另外指令，本 skill 不自動 push。
