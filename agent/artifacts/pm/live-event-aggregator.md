# PM: live-event-aggregator

## Requirements

| # | Requirement | Rationale |
|---|-------------|-----------|
| R1 | 爬蟲使用**白名單** keyword 機制：活動標題或描述包含白名單關鍵字才寫入 DB | 維持 TA 相關性，避免商演或無關活動污染資料 |
| R2 | 活動新增 `is_cancelled`、`is_sold_out`、`is_hidden` 三個 flag | 分離「平台狀態」與「管理員操作」；is_hidden 供開發者手動下架用 |
| R3 | `start_at` 超過 **400 天**的活動從 DB 自動刪除 | 控制 DB 成長；400 天保留足夠的歷史緩衝 |
| R4 | `start_at < today` 的活動以**灰階**顯示，仍可點擊 | 提供歷史瀏覽，同時視覺區分即將與過去活動 |
| R5 | 新增 `price_type` enum：`paid` / `free` / `donation` / `tbd` | 區分免費、樂捐、待確認三種無售票情境，避免混用 price=0 |
| R6 | 票價顯示規則：`paid` → 價格區間；`free` → 「免費」；`donation` → 「樂捐」；`tbd` → 「票價待確認」 | 明確前端文案，避免使用者誤判 |
| R7 | Scraper 設計 `BaseScraper` abstract class，每個 provider 實作 `fetch()` 與 `parse()` | MVP 只有 FANSI GO，但架構支援未來擴充 KKTIX、Accupass 等 |
| R8 | 活動卡片使用**純色底色**，不使用封面圖片 | 降低複雜度，避免外部圖片 CDN 依賴與失效問題 |
| R9 | 爬蟲執行後寫入 `last_scraped_at` 與 `events_count`；若 `events_count = 0` 則在開發者儀表板顯示警告 | 防止爬蟲靜默失效（FANSI GO 改版等）|
| R10 | 開發者隱藏登入：點擊 logo **5 次**進入帳號密碼頁 | 不暴露 admin 入口給一般使用者 |
| R11 | 開發者儀表板：顯示爬蟲健康狀態、手動新增 / 下架 / 隱藏活動 | 讓開發者能在爬蟲失效時手動維護資料 |

---

## DB Schema 補充

因 PM 討論新增以下欄位（更新 planning 的 schema）：

**events 表新增：**
- `is_cancelled` BOOLEAN DEFAULT FALSE
- `is_sold_out` BOOLEAN DEFAULT FALSE
- `is_hidden` BOOLEAN DEFAULT FALSE
- `price_type` ENUM('paid', 'free', 'donation', 'tbd')

---

## Risk Register

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| FANSI GO 改版導致爬蟲解析失敗 | High | 40% | R9 爬蟲健康監控 + 開發者儀表板警告 |
| 白名單設定過窄，漏掉符合 TA 的活動 | Mid | 40% | 白名單設定檔易編輯，開發者可手動新增；定期人工審查 |
| 開發者儀表板增加實作範圍 | Mid | 確定 | 列入 exec-plan phase，獨立為一個 milestone |
| 樂捐活動 price_type 判斷需人工標記或解析文字 | Low | 60% | 爬蟲先以 `tbd` 或 `donation` keyword 偵測，無法確定則標 `tbd` |
| 400天刪除 + Google Calendar 未來整合衝突 | Low | 15% | 已記錄於 postponed/google-calendar.md，整合前需確認影響 |

---

## Legal & Compliance Notes

- **平台**：FANSI GO（`go.fansi.me`）
- **robots.txt 確認（2026-04-09）**：禁止路徑為 `/dashboard`、`/api/`、`/corporation`、`/private/`；公開活動頁面無限制 → **爬取合規**
- 爬取頻率每日一次，不構成過度請求
- 資料僅含公開活動資訊，無個人資料，無個資法疑慮
- 網站 footer 標明資料來源「FANSI GO」

---

## Decision Log

| Decision | Options Considered | Conclusion | Reason |
|----------|--------------------|------------|--------|
| 爬蟲過濾機制 | 白名單 / 黑名單 / 全抓前端篩 | **白名單** | 確保 TA 相關性；黑名單維護成本高；全抓會稀釋內容 |
| 過期活動處理 | 隱藏 / 灰階顯示 / 刪除 | **灰階顯示 + 400天後刪除** | 保留歷史瀏覽價值，同時控制 DB 成長 |
| 封面圖片 | Fansgo CDN 圖片 / 純色底色 | **純色底色** | 消除外部圖片依賴，後期可按 genre 配色（已列 postponed）|
| 爬蟲失效通知 | Email / Log only / 開發者儀表板 | **開發者儀表板** | 同時解決通知與手動操作需求 |
| 樂捐活動 | price=0 / 新增 price_type | **price_type enum** | 語意明確，前端顯示無歧義 |

---

## Deferred

已移至 postponed/ 的項目：

- [Google Calendar 整合](./postponed/google-calendar.md)
- [Instagram 作為 Provider](./postponed/instagram-provider.md)
- [Genre 導向卡片底色](./postponed/genre-card-colors.md)

<!-- Last updated: 2026-04-09 18:30 -->
