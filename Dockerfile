# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        unzip \
        gnupg \
        bash \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m testuser \
    && mkdir -p /app/test-results /app/logs \
    && chown -R testuser:testuser /app /app/test-results /app/logs

# Copy and install requirements first to leverage Docker cache
COPY --chown=testuser:testuser requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create entrypoint script with proper formatting
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ensure we have write permissions\n\
if ! touch /app/test-results/.test_write_permission 2>/dev/null; then\n\
    echo "Error: Cannot write to /app/test-results directory"\n\
    exit 1\n\
fi\n\
rm -f /app/test-results/.test_write_permission\n\
\n\
# Run tests with proper error handling\n\
cd /app\n\
exec python -m pytest -v --html=/app/test-results/report.html --self-contained-html tests/ui/\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh && \
    chown testuser:testuser /app/entrypoint.sh

# Copy the project files
COPY --chown=testuser:testuser . /app/

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://selenium-hub:4444/wd/hub/status || exit 1

# Switch to non-root user
USER testuser

# Use ENTRYPOINT for the script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]