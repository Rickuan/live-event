# Skill: exec-plan

> 將 PM 確認的需求轉換為可執行的工程規格。
> 定義實作 phases、tasks、技術選型與 dependencies。

## Trigger

```
/exec-plan @agent/artifacts/pm/{feature-name}.md
```

## Dependencies

| 參數 | 路徑 | 必要 |
|------|------|------|
| PM artifact | `agent/artifacts/pm/{feature-name}.md` | 是 |

## Process

### Step 1：讀取 PM artifact

讀取 Requirements 與 Decision Log。

### Step 2：確認技術選型

列出所有需要的 dependencies，版本鎖定至 minor（`^major.minor`）。
說明每個架構決策的理由。

### Step 3：切分 Phases 與 Tasks

切分原則：
- 每個 phase 屬於**單一 scope**（不可跨前後端）
- `shared` scope 歸屬 backend 執行
- Phase 的大小由 commit skill 決定如何打包，exec-plan 不預估行數
- 每個 task 是一段完整、可獨立描述的工作單位

Phase scope 可選值：
```
front/cards | front/filter | front/calendar | front/layout
back/scraper | back/parser | back/db | back/api | back/calendar
shared
```

### Step 4：輸出 artifact

## Output

**路徑：** `agent/artifacts/exec-plan/{feature-name}.md`

```markdown
# Exec Plan: {feature-name}

## Tech Stack

| Package | Version | Purpose |
|---------|---------|---------|
| ...     | ^x.y    | ...     |

## Architecture Decisions

| Decision | Chosen Approach | Reason |
|----------|----------------|--------|
| ...      | ...            | ...    |

## Phases

### Phase 1: {name}
- **scope:** back/db
- **commit-type:** feat

Tasks:
- [ ] Task 1.1: {description}
- [ ] Task 1.2: {description}

### Phase 2: {name}
- **scope:** back/api
- **commit-type:** feat

Tasks:
- [ ] Task 2.1: {description}

<!-- Last updated: YYYY-MM-DD HH:MM -->
```

## Notes

- Task checkbox 由 `/frontend` 和 `/backend` skill 執行完成後更新為 `[x]`
- `/commit` skill 讀取每個 phase 的 scope 與 commit-type 決定打包方式
