# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app

# Create a non-root user first
RUN useradd -m testuser

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
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories and set permissions
RUN mkdir -p /app/test-results /app/logs && \
    chown -R testuser:testuser /app && \
    chmod -R 777 /app  # Give full permissions to all files and directories

# Copy requirements first to leverage Docker cache
COPY --chown=testuser:testuser requirements.txt /app/

# Install Python packages as root to avoid permission issues
RUN pip install --no-cache-dir -r requirements.txt

# Create and set permissions for the entrypoint script first
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ensure test results directory exists and has correct permissions\n\
mkdir -p /app/test-results\n\
chmod -R 777 /app/test-results\n\
\n\
cd /app\n\
python -m pytest -v --html=/app/test-results/report.html --self-contained-html tests/ui/\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh && \
    chown testuser:testuser /app/entrypoint.sh

# Copy the project files with correct ownership
COPY --chown=testuser:testuser . /app/

# Make sure all files are accessible
RUN chmod -R 777 /app

# Switch to non-root user
USER testuser

# Verify the entrypoint script exists and is executable
RUN ls -la /app/entrypoint.sh && \
    test -x /app/entrypoint.sh

# Use ENTRYPOINT for the script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]