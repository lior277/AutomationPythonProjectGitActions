# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

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

# Copy the entire project first
COPY . /app

# Create necessary directories with proper permissions
RUN mkdir -p /app/test-results /app/logs && \
    chmod 777 /app/test-results /app/logs

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create entrypoint script using RUN command with shell
RUN printf '#!/bin/bash\n\
set -e\n\
\n\
# Ensure test results directory exists\n\
mkdir -p /app/test-results\n\
\n\
# Run tests with verbose output and generate HTML report\n\
pytest -v --html=/app/test-results/report.html --self-contained-html tests/ui/\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh && \
    cat /app/entrypoint.sh  # Print the script to verify its contents

# Verify the script exists
RUN ls -l /app/entrypoint.sh

# Create a non-root user
RUN useradd -m testuser && \
    chown -R testuser:testuser /app

# Switch to non-root user
USER testuser

# Set working directory
WORKDIR /app

# Default command
CMD ["/bin/bash", "/app/entrypoint.sh"]