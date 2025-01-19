# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONPATH=/app

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

# Create necessary directories with proper permissions
RUN mkdir -p /app/test-results /app/logs && \
    chmod 777 /app/test-results /app/logs

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ensure test results directory exists\n\
mkdir -p /app/test-results\n\
\n\
# Run tests with verbose output and generate HTML report\n\
python -m pytest -v --html=/app/test-results/report.html --self-contained-html tests/ui/\n\
' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Create a non-root user and set proper permissions
RUN useradd -m testuser && \
    chown -R testuser:testuser /app && \
    chmod +x /app/entrypoint.sh

# Switch to non-root user
USER testuser

# Set working directory again to ensure proper permissions
WORKDIR /app

# Use ENTRYPOINT to ensure script is executed
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]