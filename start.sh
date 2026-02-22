#!/bin/sh
set -e

# Ensure runtime directories exist
mkdir -p /app/backend/data /app/backend/uploads/videos

# Initialise DB tables and seed demo data (idempotent — safe to run every boot)
cd /app/backend
echo "--- Initialising database tables ---"
python -c "from app.database import engine, Base; import app.models; Base.metadata.create_all(bind=engine); print('✅ Tables ready')"

echo "--- Seeding demo data ---"
python seed_ground_truth.py

# Start FastAPI backend (binds to localhost:8000, not exposed externally)
uvicorn app.main:app \
    --host 127.0.0.1 \
    --port 8000 \
    --workers 2 \
    --log-level info &

BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"

# Wait for uvicorn to be ready before nginx starts accepting traffic
echo "--- Waiting for backend to be ready ---"
for i in $(seq 1 30); do
    if python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" 2>/dev/null; then
        echo "✅ Backend is ready"
        break
    fi
    echo "  Waiting... ($i/30)"
    sleep 1
done

# Start nginx in the foreground (Cloud Run needs at least one foreground process)
# nginx will listen on $PORT (default 8080) via the conf
nginx -g "daemon off;"
