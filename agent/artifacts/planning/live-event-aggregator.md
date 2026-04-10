# Planning: live-event-aggregator

## Overview

一個聚合台灣音樂活動資訊的網站，從各售票平台爬取活動資料（MVP 以 Fansgo 為起點），以卡片形式呈現活動的時間、地點、票價、表演者與售票連結，供喜歡聽音樂的使用者瀏覽與篩選。部署目標：第一階段本機區網可用，第二階段自架伺服器公開上線。

---

## Architecture Diagram

```mermaid
graph TB
    subgraph Client
        Browser["Browser / Mobile (same LAN)"]
    end

    subgraph Frontend
        React["React + Vite + TypeScript\nTailwind + React Query"]
    end

    subgraph Backend
        FastAPI["FastAPI (Python)"]
        Scraper["Scraper Engine\n(Fansgo → extensible)"]
    end

    subgraph Database
        PG["PostgreSQL"]
    end

    subgraph External
        Fansgo["Fansgo\n(ticketing platform)"]
        Cron["Cron Job\n(daily, GitHub Actions / local)"]
    end

    Browser --> React
    React -->|REST API| FastAPI
    FastAPI --> PG
    Cron -->|trigger| Scraper
    Scraper -->|fetch| Fansgo
    Scraper -->|upsert| PG
```

---

## Class Diagram

```mermaid
classDiagram
    class Event {
        +int id
        +string title
        +datetime start_at
        +datetime end_at
        +int min_price
        +int max_price
        +string ticket_url
        +string info_url
        +string cover_image_url
        +int venue_id
        +string provider
        +string provider_event_id
        +datetime scraped_at
    }

    class Artist {
        +int id
        +string name
        +int genre_id
    }

    class EventArtist {
        +int event_id
        +int artist_id
    }

    class Venue {
        +int id
        +string name
        +string address
        +string city
    }

    class Genre {
        +int id
        +string name
    }

    Event "many" --> "1" Venue
    Event "many" <--> "many" Artist : via EventArtist
    Artist "many" --> "1" Genre
```

---

## DB Schema

```mermaid
erDiagram
    events {
        int id PK
        string title
        datetime start_at
        datetime end_at
        int min_price
        int max_price
        string ticket_url
        string info_url
        string cover_image_url
        int venue_id FK
        string provider
        string provider_event_id
        datetime scraped_at
    }

    artists {
        int id PK
        string name
        int genre_id FK
    }

    event_artists {
        int event_id FK
        int artist_id FK
    }

    venues {
        int id PK
        string name
        string address
        string city
    }

    genres {
        int id PK
        string name
    }

    events ||--o{ event_artists : ""
    artists ||--o{ event_artists : ""
    artists }o--|| genres : ""
    events }o--|| venues : ""
```

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant Cron
    participant Scraper
    participant Fansgo
    participant DB as PostgreSQL
    participant API as FastAPI
    participant FE as Frontend
    participant User

    Cron->>Scraper: trigger daily job
    Scraper->>Fansgo: fetch event listings
    Fansgo-->>Scraper: HTML / JSON response
    Scraper->>Scraper: parse & normalize
    Scraper->>DB: upsert events (by provider_event_id)

    User->>FE: open website
    FE->>API: GET /events?city=&genre=&date=
    API->>DB: query events with filters
    DB-->>API: event rows
    API-->>FE: JSON response
    FE-->>User: render event cards
```

---

## User Flow

```mermaid
flowchart TD
    A([使用者進入網站]) --> B[瀏覽活動卡片列表]
    B --> C{想篩選？}
    C -->|是| D[選擇篩選條件\n城市 / 類型 / 日期]
    D --> B
    C -->|否| E[點擊活動卡片]
    E --> F{想要的動作}
    F -->|買票| G[跳轉售票頁 ticket_url]
    F -->|看活動資訊| H[跳轉 Instagram / info_url]
    F -->|返回| B
```

---

## External Dependencies

| Service | Purpose | Auth Required |
|---------|---------|---------------|
| Fansgo | 爬取活動資料（MVP 起點） | 否（公開頁面） |
| GitHub Actions | 每日定時觸發爬蟲（免費 cron） | GitHub token |
| Google Calendar | 使用者訂閱活動行事曆 | **Postponed** |

---

## Deployment Plan

| 階段 | 方式 | 說明 |
|------|------|------|
| Phase 1 | 本機 + Docker Compose | 區網內電腦與手機皆可存取 |
| Phase 2 | 自架伺服器（Render / Railway / VPS）| 公開上線，社群使用 |

提供 `docker-compose.yml`，讓想自行部署的人也能一鍵啟動。

---

## Open Questions

留給 `/pm` 討論：

1. **TA 導向過濾條件**：爬蟲要排除哪些類型的活動？（例如：只抓獨立音樂、排除大型商演）條件由人工設定還是標籤自動化？
2. **活動更新與下架**：Fansgo 活動取消或售完時，網站如何處理？（隱藏 / 標記 / 刪除）
3. **票價顯示規則**：無票價資訊時顯示「免費」還是「待確認」？
4. **多 Provider 擴充介面**：之後加入 KKTIX、Accupass 等，Scraper 要設計 base class 還是 plugin 架構？
5. **封面圖片**：若 Fansgo 無圖或圖片失效，前端卡片的 fallback 設計？

<!-- Last updated: 2026-04-09 18:00 -->
