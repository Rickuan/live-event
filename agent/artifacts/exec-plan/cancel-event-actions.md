# ~~Exec Plan: cancel-event-actions~~

> ⚠️ **Superseded by `event-management.md`** (2026-04-10)
> 設計調整為單一 status enum + 統一操作區，此 plan 不再執行。

## Tech Stack

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | （現有） | DELETE endpoint |
| SQLAlchemy | （現有） | ORM delete |
| @tanstack/react-query | （現有） | deleteMutation |

## Architecture Decisions

| Decision | Chosen Approach | Reason |
|----------|----------------|--------|
| 刪除語意 | 永久刪除（hard delete） | is_cancelled 已代表軟性下架，刪除是明確的不可逆動作 |
| 刪除前置條件 | 無（任何活動皆可刪） | 簡化流程；admin 自行負責確認 |
| 刪除回傳 | 204 No Content | REST 標準，前端只需 invalidate cache |
| 前端確認流程 | 無二次確認 dialog | 按鈕只在 is_cancelled=true 時出現，已是明確意圖 |

## Phases

### Phase 1: Delete API endpoint
- **scope:** back/api
- **commit-type:** feat

Tasks:
- [ ] Task 1.1: 在 `admin.py` 新增 `DELETE /admin/events/{event_id}`，使用 Admin dependency 驗證 token，event 不存在回 404，成功回 204

### Phase 2: EventRow delete action
- **scope:** front/layout
- **commit-type:** feat

Tasks:
- [ ] Task 2.1: `EventRow` props 新增 `onDelete: (id: number) => void`
- [ ] Task 2.2: `is_cancelled=true` 時改渲染兩個按鈕：「重新上架」（灰色）與「刪除活動」（紅色 border）
- [ ] Task 2.3: `AdminDashboardPage` 新增 `deleteMutation`（`DELETE /admin/events/{id}`），成功後 invalidate `['admin','events']`，並將 `onDelete` 傳入 `EventRow`

<!-- Last updated: 2026-04-10 18:40 -->
