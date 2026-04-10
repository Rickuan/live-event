# ── Setup ──────────────────────────────────────────────────────────────────
PYTHON := $(shell command -v python3.12 || command -v python3.11 || command -v python3.10)

.venv:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	.venv/bin/playwright install chromium

setup: .venv
	cp -n .env.example .env || true
	@echo ""
	@echo "✓ venv ready. Fill in backend/.env then run: make migrate"

# ── DB ─────────────────────────────────────────────────────────────────────
migrate:
	DATABASE_URL=postgresql://livevent:livevent@localhost:5432/livevent .venv/bin/alembic upgrade head

# ── Scraper ────────────────────────────────────────────────────────────────
scrape:
	.venv/bin/python -m scraper.run

# ── Docker ─────────────────────────────────────────────────────────────────
up:
	docker compose up

down:
	docker compose down
