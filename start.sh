#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"
FASTAPI_LOG="$LOG_DIR/fastapi.log"
GUI_LOG="$LOG_DIR/gui.log"
START_TIMEOUT=30

echo "Starting FastAPI server... (logs: $FASTAPI_LOG)"
# Use -m to run as a module
python -m app.main > "$FASTAPI_LOG" 2>&1 &
FASTAPI_PID=$!
echo "FastAPI PID: $FASTAPI_PID"

# Wait for HTTP 200 from the server root endpoint, with timeout.
echo "Waiting for FastAPI to become ready on http://127.0.0.1:8000/ (timeout: ${START_TIMEOUT}s)"
READY=0
for i in $(seq 1 $START_TIMEOUT); do
    if curl -sS --max-time 2 http://127.0.0.1:8000/ >/dev/null 2>&1; then
        READY=1
        break
    fi
    if ! kill -0 "$FASTAPI_PID" 2>/dev/null; then
        echo "FastAPI process ($FASTAPI_PID) exited before becoming ready. Check $FASTAPI_LOG"
        exit 1
    fi
    sleep 1
done

if [ "$READY" -ne 1 ]; then
    echo "Timed out waiting for FastAPI to become ready. Check $FASTAPI_LOG"
    kill -TERM "$FASTAPI_PID" 2>/dev/null || true
    exit 1
fi

echo "FastAPI is ready — starting Tkinter GUI (logs: $GUI_LOG)"
python -m gui.main > "$GUI_LOG" 2>&1 &
GUI_PID=$!
echo "GUI PID: $GUI_PID"

cleanup() {
    echo "Shutting down children..."
    kill -TERM "$FASTAPI_PID" "$GUI_PID" 2>/dev/null || true
    wait "$FASTAPI_PID" 2>/dev/null || true
    wait "$GUI_PID" 2>/dev/null || true
    exit 0
}

trap cleanup SIGINT SIGTERM

# Monitor: if either process exits, stop the other and exit.
while true; do
    if ! kill -0 "$FASTAPI_PID" 2>/dev/null; then
        echo "FastAPI process ($FASTAPI_PID) exited. Stopping GUI ($GUI_PID)."
        kill -TERM "$GUI_PID" 2>/dev/null || true
        break
    fi
    if ! kill -0 "$GUI_PID" 2>/dev/null; then
        echo "GUI process ($GUI_PID) exited. Stopping FastAPI ($FASTAPI_PID)."
        kill -TERM "$FASTAPI_PID" 2>/dev/null || true
        break
    fi
    sleep 1
done

# Wait for both to exit cleanly
wait "$FASTAPI_PID" 2>/dev/null || true
wait "$GUI_PID" 2>/dev/null || true
echo "Both processes stopped."
