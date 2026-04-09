# Skill: worklog

> 彙整上次執行 /worklog 至今的所有變更，生成中文 session summary。
> 資料來源為 git log 與 exec-plan 的完成項目，不依賴即時寫入。

## Trigger

```
/worklog
```

## Dependencies

無需 @file 參數。自動讀取：
- `git log`（上次 worklog session 至今的 commits）
- `agent/artifacts/exec-plan/*.md`（`[x]` 完成的 tasks）

## Process

### Step 1：取得 git log 範圍

讀取 `agent/worklog/sessions/` 下最新的 session 檔案，
取得上次 worklog 的時間，作為 `git log` 的起始點。

若從未執行過 /worklog，則取今日所有 commits。

```bash
git log --oneline --since="{last_session_time}"
```

### Step 2：讀取 exec-plan 完成項目

掃描 `agent/artifacts/exec-plan/` 下所有 `.md` 檔案，
收集所有 `[x]` 完成的 tasks（排除上次 worklog 已記錄的）。

### Step 3：彙整生成中文 session summary

將 git commits 與 exec-plan tasks 對應，
以「在 {file} 新增/修改了 {feature}，以實現 {task}」格式描述每項變更。

### Step 4：輸出 artifact

## Output

**路徑：** `agent/worklog/sessions/YYYY-MM-DD-HH-MM.md`

```markdown
# Session: YYYY-MM-DD HH:MM

## 完成的工作

### {feature-name}
- 在 {file} 新增了 {feature}，以實現 {task description}
- 在 {file} 修改了 {feature}，以實現 {task description}

## 使用的 Skills
/planning | /pm | /exec-plan | /backend | /frontend | /test-plan | /test | /commit

## Commits
| Hash | Message |
|------|---------|
| {short hash} | {commit message} |

<!-- Last updated: YYYY-MM-DD HH:MM -->
```
