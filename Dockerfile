# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Environment Setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONPATH=/app
ENV HOME=/home/testuser
ENV DISPLAY=:99
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

# Create test user and required directories
RUN useradd -m testuser && \
    mkdir -p /app/test-results/logs /app/logs && \
    mkdir -p /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix && \
    chown -R testuser:testuser /app /app/test-results /app/logs

# Install Chrome and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        gnupg \
        ca-certificates && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        google-chrome-stable \
        curl \
        unzip \
        xvfb \
        libxi6 \
        libgconf-2-4 \
        default-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install specific ChromeDriver version
RUN CHROME_VERSION=$(google-chrome-stable --version | cut -d ' ' -f3) && \
    CHROMEDRIVER_VERSION=120.0.6099.71 && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Copy and install Python requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt pytest-html pytest-cov

# Copy entrypoint script
COPY docker-entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh && \
    chown testuser:testuser /app/entrypoint.sh

# Copy the project files
COPY --chown=testuser:testuser . /app/

# Ensure all files are owned by testuser
RUN chown -R testuser:testuser /app

# Switch to non-root user for security
USER testuser

# Set the entrypoint
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]