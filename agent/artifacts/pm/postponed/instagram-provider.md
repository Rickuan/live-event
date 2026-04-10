# Postponed: instagram-provider

## Scope

將 Instagram 作為獨立的活動資料來源（Provider）。

背景：部分電子音樂活動不使用售票平台，活動消息發布於 Instagram，現場收現金。
這類活動在 FANSI GO 等售票平台上不會出現，只能透過 Instagram post 獲取資訊。

技術需求：
- 爬取特定 Instagram 帳號或 hashtag 的 post
- 從 post 內容解析活動資訊（時間、地點、表演者）
- 實作 `InstagramScraper` 繼承 `BaseScraper`

## Reason for Deferral

Instagram 不提供公開 API 給非官方爬蟲，爬取需要模擬登入或使用非官方手段，合規風險較高。
此外，從非結構化的 post 文字解析活動資訊需要 NLP，複雜度高。POC 階段不納入。

## Conditions to Revisit

- 核心售票平台 provider 穩定後
- 有明確的 Instagram Graph API 或合規爬取方案
- 或改為手動輸入功能（開發者在儀表板手動新增這類活動）

<!-- Last updated: 2026-04-09 18:30 -->
