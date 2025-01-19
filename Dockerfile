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

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ensure test-results directory exists and is writable\n\
mkdir -p /app/test-results\n\
chown -R testuser:testuser /app/test-results\n\
chmod 777 /app/test-results\n\
\n\
cd /app\n\
exec python -m pytest -v --html=/app/test-results/report.html --self-contained-html tests/ui/\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh && \
    chown testuser:testuser /app/entrypoint.sh

# Copy the project files
COPY --chown=testuser:testuser . /app/

# Give ownership to testuser
RUN chown -R testuser:testuser /app

# Switch to non-root user
USER testuser

# Use ENTRYPOINT for the script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]