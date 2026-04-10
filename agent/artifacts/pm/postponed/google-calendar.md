# Postponed: google-calendar

## Scope

讓使用者可以將網站上的活動同步到 Google Calendar。
原始構想：使用者有一個專門紀錄演出活動的 Google Calendar，同步內容包含節目名稱、地點、活動頁面連結。

整合方向（初步）：
- 只自動**新增**新活動到 Calendar，不更新、不刪除
- 使用者授權後，爬蟲每日執行時自動 push 新活動

## Reason for Deferral

非 POC 範圍。需要 Google OAuth 授權流程，增加 backend 複雜度與使用者操作摩擦，不是產品核心體驗。

## Conditions to Revisit

- 核心爬蟲 + 卡片展示穩定運作後
- 有使用者明確提出需求時

## 注意事項（整合前必須確認）

DB 設定了超過 **400 天**的活動自動刪除機制。整合 Google Calendar 前需確認：

- 初步評估：Calendar 整合只做「新增」不做「更新或刪除」，DB 刪除不影響已同步到 Calendar 的活動 → **預計無問題**
- 但需在實作前再次驗證此假設，確認 Calendar event 的 lifecycle 與 DB record 完全解耦

<!-- Last updated: 2026-04-09 18:30 -->
