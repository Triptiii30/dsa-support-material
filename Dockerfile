# Lightweight Python 3.11 Runtime
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    HOST=0.0.0.0

# Set working directory
WORKDIR /app

# Create a non-privileged user for secure container execution
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy dependency definition (pure standard library)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt || true

# Copy project source code
COPY dataset/ ./dataset/
COPY modules/ ./modules/
COPY web/ ./web/
COPY server.py main.py ./

# Set file permissions and switch to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose default HTTP server port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/initial-data')" || exit 1

# Start production server
CMD ["python", "server.py"]
