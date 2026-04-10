from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import admin, events, genres, venues

app = FastAPI(title="Live Event Aggregator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(genres.router)
app.include_router(venues.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}
