# Skill: planning

> 新產品、新功能、或重大架構調整時使用。
> 輸出 high concept 設計文件，作為後續所有 skill 的基礎。

## Trigger

```
/planning
```

## Dependencies

無（流程起點，不需要 @file 參數）

## Process

### Step 1：問卷蒐集需求

依序詢問以下問題，每題逐一確認後再進行下一題：

1. 這個功能/產品要解決什麼問題？目標使用者是誰？
2. 主要的實體有哪些？（例如：Event、Artist、Venue）
3. 需要哪些外部服務/API？（例如：Google Calendar、售票平台）
4. 技術棧有限制嗎？（前端框架、後端語言、DB 類型）
5. 有效能或規模的要求嗎？（DAU、資料量、爬取頻率）

### Step 2：生成 artifact

根據問卷回答，生成以下所有圖表與文件內容。
圖表一律使用 Mermaid 語法。

### Step 3：輸出至指定路徑

輸出前確認 feature name（用於檔名），以 kebab-case 命名。

## Output

**路徑：** `agent/artifacts/planning/{feature-name}.md`

**結構：**

```markdown
# Planning: {feature-name}

## Overview
一段話描述產品目標與使用者。

## Architecture Diagram
（Mermaid 系統架構圖：前端 / 後端 / 爬蟲 / DB / 外部服務）

## Class Diagram
（Mermaid class diagram：主要實體與關係）

## DB Schema
（Mermaid ER diagram）

## Sequence Diagram
（Mermaid sequence diagram：主要流程的時序）

## User Flow
（Mermaid flowchart：使用者操作流程）

## External Dependencies
| Service | Purpose | Auth Required |
|---------|---------|---------------|
| ...     | ...     | ...           |

## Open Questions
尚未確定的決策，留給 /pm 討論。

<!-- Last updated: YYYY-MM-DD HH:MM -->
```
