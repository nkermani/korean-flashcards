#!/bin/bash

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"
FASTAPI_LOG="$LOG_DIR/fastapi.log"
GUI_LOG="$LOG_DIR/gui.log"
START_TIMEOUT=30
VENV_PATH="./venv"
ENV_PATH="./app/.env"
PYTHON_VENV_PATH="$VENV_PATH/bin/python"

check_api_key_exist() {
    if [ ! -f "$ENV_PATH" ]; then
        echo "$ENV_PATH file not found. Please create it with your Mistral API key as per setup instructions."
        exit 1
    fi

    # Making sure .env file has MISTRAL_API_KEY set
    if ! grep -q '^MISTRAL_API_KEY=' "$ENV_PATH"; then
        echo "MISTRAL_API_KEY not set in $ENV_PATH. Please set it with your API key."
        exit 1
    fi
}

# Making sure user is at root directory
if [ "$(pwd)" != "$ROOT_DIR" ]; then
    echo "Please run this script from the root directory: $ROOT_DIR"
    exit 1
fi

# --- Making sure virtual environment exists ---
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment $VENV_PATH not found. Please run: ./setup.sh first."
    exit 1
fi

# --- Making sure .env file exists ---
check_api_key_exist

echo "Starting FastAPI server... (logs: $FASTAPI_LOG)"
# Use -m to run as a module
"$PYTHON_VENV_PATH" -m app.main > "$FASTAPI_LOG" 2>&1 &
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
"$PYTHON_VENV_PATH" -m gui.main > "$GUI_LOG" 2>&1 &
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
