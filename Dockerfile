# ============================================================
# Stage 1: Build Angular Frontend
# ============================================================
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files first for layer caching
COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci --legacy-peer-deps

# Copy remaining frontend source
COPY frontend/ ./

# Build production bundle (output goes to dist/frontend/browser)
RUN npm run build -- --configuration production

# ============================================================
# Stage 2: Final Production Image (Python + nginx)
# ============================================================
FROM python:3.11-slim AS production

# Install system deps: nginx + libs needed by opencv-python-headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    build-essential \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies directly into the system site-packages
# (avoid --prefix, which breaks native .so extension modules like cv2)
# Install Python dependencies from curated Docker-specific requirements
# (avoids Windows-only packages and encoding issues in the full pip freeze)
COPY backend/requirements-docker.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    python -c "import cv2; print('✅ cv2 OK:', cv2.__version__)"

# Copy backend application code
WORKDIR /app
COPY backend/ ./backend/

# Create required runtime directories
RUN mkdir -p /app/backend/data /app/backend/uploads/videos

# Copy Angular build output into nginx web root
COPY --from=frontend-builder /app/frontend/dist/frontend/browser /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf
RUN rm -f /etc/nginx/sites-enabled/default

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Cloud Run listens on $PORT (default 8080)
EXPOSE 8080

CMD ["/start.sh"]
