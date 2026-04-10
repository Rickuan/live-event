# Exec Plan: live-event-aggregator

## Tech Stack

### Backend

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | ^0.115 | Web framework |
| uvicorn | ^0.32 | ASGI server |
| sqlalchemy | ^2.0 | ORM |
| alembic | ^1.14 | DB migrations |
| psycopg2-binary | ^2.9 | PostgreSQL driver |
| pydantic | ^2.9 | Data validation & settings |
| httpx | ^0.27 | Async HTTP client（爬蟲用）|
| beautifulsoup4 | ^4.12 | HTML parsing |
| python-jose[cryptography] | ^3.3 | JWT token（admin auth）|
| passlib[bcrypt] | ^1.7 | 密碼 hash |
| pyyaml | ^6.0 | 白名單設定檔讀取 |
| python-dotenv | ^1.0 | 環境變數管理 |

### Frontend

| Package | Version | Purpose |
|---------|---------|---------|
| react | ^18.3 | UI framework |
| react-router-dom | ^7.13 | 路由 |
| @tanstack/react-query | ^5.90 | Server state 管理 |
| axios | ^1.13 | HTTP client |
| tailwindcss | ^3.4 | Utility CSS |
| clsx + tailwind-merge | ^2.1 / ^3.5 | 條件 class 組合 |

### Infrastructure

| Tool | Purpose |
|------|---------|
| Docker + Docker Compose | 本機開發環境（PostgreSQL + FastAPI + React）|
| GitHub Actions | 每日爬蟲 cron job（`0 2 * * *` UTC）|

---

## Architecture Decisions

| Decision | Chosen Approach | Reason |
|----------|----------------|--------|
| ORM | SQLAlchemy 2.0（非 1.x）| 原生 async 支援、型別推斷更完整 |
| HTTP client | httpx（非 requests）| async-native，與 FastAPI 生態一致 |
| Admin auth | JWT（stateless）| 單人開發者使用，不需要 session 管理 |
| Admin credentials | 環境變數（`ADMIN_USERNAME` / `ADMIN_PASSWORD_HASH`）| 不存 DB、不需要帳號管理功能 |
| Whitelist config | `scraper/whitelist.yaml`（git 追蹤）| 易編輯、可 review、與程式碼同步 |
| Filter state | URL query params（`?city=&genre=&date=`）| 可分享連結、瀏覽器 back 正確 |
| Cron 本機開發 | 手動執行 `python -m scraper.run` | 本機不依賴 cron daemon；GitHub Actions 處理自動排程 |

---

## Phases

### Phase 1: Project Scaffold & Docker
- **scope:** back/db
- **commit-type:** chore

Tasks:
- [x] Task 1.1: 建立專案目錄結構（`backend/`、`frontend/`、`scraper/`）
- [x] Task 1.2: 建立 `docker-compose.yml`（services: postgres, backend, frontend）
- [x] Task 1.3: 建立 `backend/Dockerfile` 與 `frontend/Dockerfile`
- [x] Task 1.4: 建立 `backend/.env.example`（`DATABASE_URL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD_HASH`, `SECRET_KEY`）

---

### Phase 2: Shared Types
- **scope:** shared
- **commit-type:** feat

Tasks:
- [x] Task 2.1: 定義 TypeScript 共用型別（`PriceType`, `Event`, `Artist`, `Venue`, `Genre`, `EventDetail`）
- [x] Task 2.2: 定義 API response 型別（`EventListResponse`, `EventDetailResponse`, `AdminHealthResponse`）

---

### Phase 3: Database Models & Migrations
- **scope:** back/db
- **commit-type:** feat

Tasks:
- [x] Task 3.1: 建立 SQLAlchemy `Base` 與 `database.py`（engine、session factory、`get_db` dependency）
- [x] Task 3.2: 定義 ORM models
  - `Venue`（id, name, address, city）
  - `Genre`（id, name）
  - `Artist`（id, name, genre_id FK）
  - `Event`（id, title, start_at, end_at, min_price, max_price, price_type, ticket_url, info_url, venue_id FK, provider, provider_event_id, is_cancelled, is_sold_out, is_hidden, scraped_at）
  - `EventArtist`（event_id FK, artist_id FK）
  - `ScraperLog`（id, provider, run_at, events_count, has_warning）
- [x] Task 3.3: Alembic 初始化（`alembic init`）與 `env.py` 設定
- [x] Task 3.4: 生成並執行 initial migration（建立所有 table）
- [x] Task 3.5: 實作 `cleanup.py`：刪除 `start_at < now() - 400 days` 的 events（含 cascade 刪除 event_artists）

---

### Phase 4: Scraper Engine
- **scope:** back/scraper
- **commit-type:** feat

Tasks:
- [x] Task 4.1: 定義 `BaseScraper` abstract class（`fetch() -> str`、`parse(html: str) -> list[EventRaw]`、`run() -> int`）
- [x] Task 4.2: 定義 `EventRaw` dataclass（scraper 輸出的原始資料結構）
- [x] Task 4.3: 建立 `scraper/whitelist.yaml`（keyword 列表初始值，例如：indie, punk, jazz, house, tance, bass, techno, metal, rock, pop 等）
- [x] Task 4.4: 實作 `WhitelistFilter`（載入 yaml，判斷 EventRaw 是否符合白名單）
- [x] Task 4.5: 實作 `FansiGoScraper.fetch()`（以 httpx 抓取 `go.fansi.me` 活動列表頁）
- [x] Task 4.6: 實作 `FansiGoScraper.parse()`（BeautifulSoup 解析 HTML，提取 title, date, venue, artists, price, ticket_url, info_url；`price_type` 以關鍵字偵測：「免費」→ free、「樂捐」→ donation、有價格 → paid、其他 → tbd）
- [x] Task 4.7: 實作 `UpsertRunner`（依 `provider_event_id` upsert events；同步 artists、venues；維護 event_artists）
- [x] Task 4.8: 實作 `scraper/run.py`（main entry point：fetch → filter → parse → upsert → 寫入 ScraperLog；events_count=0 時 `has_warning=True`）

---

### Phase 5: REST API
- **scope:** back/api
- **commit-type:** feat

Tasks:
- [x] Task 5.1: 建立 FastAPI app entry point（`main.py`）與 router 結構
- [x] Task 5.2: 實作 `GET /events`（query params: `city`, `genre_id`, `date_from`, `date_to`, `include_past: bool = False`；`is_hidden=False` 固定過濾）
- [x] Task 5.3: 實作 `GET /events/{id}`（單一活動詳情）
- [x] Task 5.4: 實作 `POST /admin/login`（驗證 username/password，回傳 JWT；credentials 從環境變數讀取）
- [x] Task 5.5: 實作 admin middleware（JWT 驗證 dependency）
- [x] Task 5.6: 實作 `GET /admin/health`（回傳最新 ScraperLog：run_at, events_count, has_warning）
- [x] Task 5.7: 實作 `POST /admin/events`（手動新增活動）
- [x] Task 5.8: 實作 `PATCH /admin/events/{id}`（更新 is_hidden / is_cancelled）
- [x] Task 5.9: 設定 CORS（開發: `localhost:5173`；生產: 環境變數）

---

### Phase 6: Frontend Layout & Routing
- **scope:** front/layout
- **commit-type:** feat

Tasks:
- [x] Task 6.1: 確認 Vite + Tailwind + React Query 設定（`tailwind.config.js`、`QueryClientProvider`）
- [x] Task 6.2: 建立 `axios` instance（`baseURL` 從 env var `VITE_API_URL` 讀取）
- [x] Task 6.3: 建立 React Router 路由（`/` → EventListPage, `/admin/login` → AdminLoginPage, `/admin` → AdminDashboardPage）
- [x] Task 6.4: 建立 `Navbar` 元件（logo + 點擊 5 次觸發 navigate to `/admin/login` 的 hidden handler）
- [x] Task 6.5: 建立 `Footer` 元件（標明資料來源：「活動資料來源：FANSI GO」）
- [x] Task 6.6: 建立 `AdminLoginPage`（帳號密碼表單，成功後 JWT 存入 localStorage，redirect to `/admin`）
- [x] Task 6.7: 建立 `AdminDashboardPage`（顯示 ScraperLog health card；事件列表含 hide/cancel 操作按鈕）
- [x] Task 6.8: 建立 `ProtectedRoute` wrapper（未登入則 redirect to `/admin/login`）

---

### Phase 7: Event Cards
- **scope:** front/cards
- **commit-type:** feat

Tasks:
- [x] Task 7.1: 建立 `PriceBadge` 元件（依 `price_type` 顯示：paid → 價格區間、free → 「免費」、donation → 「樂捐」、tbd → 「票價待確認」）
- [x] Task 7.2: 建立 `EventCard` 元件（純色底色、title、start_at、venue.city + venue.name、artists、PriceBadge；past event → `grayscale opacity-60` class）
- [x] Task 7.3: 建立 `EventGrid` 元件（RWD grid：mobile 1 col, tablet 2 col, desktop 3 col）
- [x] Task 7.4: 建立 `EmptyState` 元件（無符合條件活動時顯示）
- [x] Task 7.5: 建立 `EventListPage`（組合 FilterBar + EventGrid + EmptyState）

---

### Phase 8: Filter UI
- **scope:** front/filter
- **commit-type:** feat

Tasks:
- [x] Task 8.1: 建立 `useEvents` hook（呼叫 `GET /events`，接收 filter 參數，回傳 events + loading + error）
- [x] Task 8.2: 建立 `useFilterState` hook（讀寫 URL query params：city, genre_id, date_from, date_to, include_past）
- [x] Task 8.3: 建立 `FilterBar` 元件（城市 select、Genre select、日期範圍 input、「顯示過去活動」toggle）
- [x] Task 8.4: `GET /genres` API endpoint（供 FilterBar genre select 使用）
- [x] Task 8.5: `GET /venues/cities` API endpoint（供 FilterBar 城市 select 使用）

---

### Phase 9: GitHub Actions Cron
- **scope:** back/scraper
- **commit-type:** chore

Tasks:
- [ ] Task 9.1: 建立 `.github/workflows/scraper.yml`（cron: `0 2 * * *` UTC；執行 `python -m scraper.run`；設定 `DATABASE_URL` secret）
- [ ] Task 9.2: 建立 `.github/workflows/scraper.yml` 的手動觸發（`workflow_dispatch`，供測試用）

<!-- Last updated: 2026-04-09 20:55 -->
