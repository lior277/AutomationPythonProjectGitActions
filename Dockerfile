# Use an official Python runtime as a parent image
FROM python:3.10-slim

###################
# Environment Setup
###################

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    HOME=/home/testuser \
    DISPLAY=:99 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /app

###################
# User Setup
###################

# Create test user and required directories
RUN useradd -m testuser && \
    mkdir -p /app/test-results/{logs,screenshots,reports} && \
    mkdir -p /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix && \
    chown -R testuser:testuser /app

###################
# System Dependencies
###################

# Install system dependencies and Chrome
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        unzip \
        gnupg \
        xvfb \
        libxi6 \
        libgconf-2-4 \
        default-jdk \
        ca-certificates \
        procps \
        fonts-liberation \
        libasound2 \
        libatk-bridge2.0-0 \
        libatk1.0-0 \
        libatspi2.0-0 \
        libcups2 \
        libdbus-1-3 \
        libdrm2 \
        libgbm1 \
        libgtk-3-0 \
        libnspr4 \
        libnss3 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libxshmfence1 \
        xdg-utils && \
    # Add Chrome repository and install Chrome
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

###################
# ChromeDriver Setup
###################

# Install ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{ print $3 }' | cut -d'.' -f1) && \
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}") && \
    wget -N https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

###################
# Python Dependencies
###################

# Copy requirements files
COPY requirements*.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    if [ -f requirements-dev.txt ]; then pip install --no-cache-dir -r requirements-dev.txt; fi

###################
# Test Setup
###################

# Create and configure test directories
RUN mkdir -p /app/test-results/{logs,screenshots,reports} && \
    chown -R testuser:testuser /app/test-results

# Create entrypoint script
COPY docker-entrypoint.sh /app/entrypoint.sh

# Set script permissions
RUN chmod +x /app/entrypoint.sh && \
    chown testuser:testuser /app/entrypoint.sh

###################
# Final Setup
###################

# Copy the project files
COPY --chown=testuser:testuser . /app/

# Set file permissions
RUN chown -R testuser:testuser /app && \
    chmod -R 755 /app

# Switch to non-root user for security
USER testuser

# Set the entrypoint
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]