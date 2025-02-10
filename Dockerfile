# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    HOME=/home/testuser \
    DISPLAY=:99

# Set the working directory in the container
WORKDIR /app

# Create test user and directories
RUN useradd -m testuser && \
    mkdir -p /app/test-results/logs /app/logs && \
    mkdir -p /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix && \
    chown -R testuser:testuser /app /app/test-results /app/logs

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
        procps && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt pytest-html

# Create entrypoint script using heredoc
RUN cat << 'EOF' > /app/entrypoint.sh
#!/bin/bash
set -e

# Ensure directories exist with proper permissions
mkdir -p /app/test-results/logs
chown -R testuser:testuser /app/test-results
chmod 777 /app/test-results

# Start virtual framebuffer
Xvfb :99 -screen 0 1920x1080x24 &

# Wait for Xvfb to start
sleep 1

cd /app
python -m pytest tests/ui/ -v \
    --html=/app/test-results/report.html \
    --self-contained-html \
    --capture=tee-sys \
    --log-cli-level=INFO
EOF

# Set script permissions
RUN chmod +x /app/entrypoint.sh && \
    chown testuser:testuser /app/entrypoint.sh

# Copy the project files
COPY --chown=testuser:testuser . /app/

# Ensure all files are owned by testuser
RUN chown -R testuser:testuser /app

# Switch to non-root user
USER testuser

# Use ENTRYPOINT for the script
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]