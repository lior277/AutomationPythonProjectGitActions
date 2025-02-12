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

# Install system dependencies
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
    # Add Chrome repository
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    # Install Chrome
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # Install specific version of ChromeDriver
    CHROME_VERSION=$(google-chrome --version | cut -d " " -f3 | cut -d "." -f1) && \
    wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION > /tmp/chromedriver_version && \
    CHROMEDRIVER_VERSION=$(cat /tmp/chromedriver_version) && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    # Cleanup
    rm -rf /tmp/chromedriver* && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

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