# Skill: pm

> 根據 planning artifact 主動發現遺漏需求，討論優缺點與風險，
> 並輸出確認後的需求文件與延後功能清單。

## Trigger

```
/pm @agent/artifacts/planning/{feature-name}.md
```

## Dependencies

| 參數 | 路徑 | 必要 |
|------|------|------|
| planning artifact | `agent/artifacts/planning/{feature-name}.md` | 是 |

## Process

### Step 1：讀取 planning artifact

讀取 Overview、External Dependencies、Open Questions。

### Step 2：主動分析並提出遺漏需求

從以下面向逐一檢視，主動提出 planning 中未涵蓋的議題：

- **Edge cases**：使用者行為異常、資料缺失、空狀態
- **安全性 / 隱私**：資料來源授權、使用者資料處理
- **規模風險**：爬蟲頻率、API rate limit、DB 增長速度
- **UX 缺口**：功能有定義但互動細節不清楚的地方
- **相依服務 fallback**：外部 API 失敗時的降級策略
- **法規合規**：爬取公開資料的法律注意事項（robots.txt、著作權、個資法）

### Step 3：逐項與使用者討論

每個議題說明：
- 問題描述
- 建議做法
- 優點 / 缺點 / 風險等級（High 70% / Mid 40% / Low 15%）

可主動建議將某功能延後，並說明延後理由。

### Step 4：輸出 artifact

## Output

### 主要 artifact

**路徑：** `agent/artifacts/pm/{feature-name}.md`

```markdown
# PM: {feature-name}

## Requirements
確定要做的需求，每條附 rationale。

| # | Requirement | Rationale |
|---|-------------|-----------|
| R1 | ... | ... |

## Risk Register

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| ...  | High / Mid / Low | 70% / 40% / 15% | ... |

## Legal & Compliance Notes
公開資料爬取的相關法規研究與注意事項。

## Decision Log
| Decision | Options Considered | Conclusion | Reason |
|----------|--------------------|------------|--------|
| ...      | ...                | ...        | ...    |

## Deferred
已移至 postponed/ 的項目：
- [{feature}](./postponed/{feature}.md)

<!-- Last updated: YYYY-MM-DD HH:MM -->
```

### 延後功能 artifact（每個延後功能獨立一份）

**路徑：** `agent/artifacts/pm/postponed/{feature-name}.md`

```markdown
# Postponed: {feature-name}

## Scope
說明這個功能的範圍與原本的設計想法。

## Reason for Deferral
當時討論延後的理由。

## Conditions to Revisit
什麼情況下可以重新評估這個功能。

<!-- Last updated: YYYY-MM-DD HH:MM -->
```
