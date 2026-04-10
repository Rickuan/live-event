#!/usr/bin/env bash
# 同時啟動前後端開發伺服器
# 用法: ./run_server/start.sh
# 結束: Ctrl+C (會同時關閉前後端)

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"

# 顏色
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${CYAN}[run_server]${NC} $1"; }
err() { echo -e "${RED}[run_server]${NC} $1" >&2; }

# 確認 venv 存在
if [ ! -f "$BACKEND/.venv/bin/uvicorn" ]; then
  err "找不到 $BACKEND/.venv — 請先執行 cd backend && make setup"
  exit 1
fi

# 確認 node_modules 存在
if [ ! -d "$FRONTEND/node_modules" ]; then
  err "找不到 $FRONTEND/node_modules — 請先執行 cd frontend && npm install"
  exit 1
fi

# 清理子程序
cleanup() {
  log "正在關閉伺服器..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
  log "已關閉"
}
trap cleanup EXIT INT TERM

# 啟動 FastAPI
log "${GREEN}啟動 Backend${NC} (FastAPI @ http://localhost:8000)"
cd "$BACKEND"
.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 2>&1 \
  | sed "s/^/${YELLOW}[backend]${NC} /" &
BACKEND_PID=$!

# 啟動 Vite
log "${GREEN}啟動 Frontend${NC} (Vite @ http://localhost:5173)"
cd "$FRONTEND"
npm run dev 2>&1 \
  | sed "s/^/${GREEN}[frontend]${NC} /" &
FRONTEND_PID=$!

log "兩個伺服器已啟動，按 Ctrl+C 結束"
wait
