# Postponed: fansi-go-event-detail

## Scope

在 FANSI GO 爬蟲中，額外抓取每個活動的詳情頁（`/events/{EVENTID}`），
補充活動列表頁沒有的資訊：票價、price_type。

目前狀態：
- 票價欄位（`min_price`, `max_price`, `price_type`）全部存為 `tbd`
- 詳情頁確定有票價資訊，需要實作 `FansiGoScraper._fetch_detail(event_id)` 並在 parse 後補值

## Reason for Deferral

優先讓網頁可以跑起來。Detail fetch 會讓爬蟲變慢（每個活動多一個 HTTP request），
且 `tbd` 對 POC 展示來說可接受。

## Conditions to Revisit

- 基本網頁（列表 + 卡片 + 篩選）穩定上線後
- 票價顯示對使用者有實際需求時

## 實作方向

```python
# FansiGoScraper 新增 method
async def _fetch_detail(self, event_id: str) -> dict:
    # Playwright: goto /events/{event_id}, wait for price element, extract
    ...

# run() 改為：fetch listing → parse → for each event: fetch_detail → update price fields
```

<!-- Last updated: 2026-04-09 19:50 -->
