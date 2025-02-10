# Use an official Python runtime as a parent image
FROM python:3.10-slim

###################
# Environment Setup
###################

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \    # Prevent Python from writing pyc files
    PYTHONUNBUFFERED=1 \           # Prevent Python from buffering stdout and stderr
    PIP_NO_CACHE_DIR=1 \           # Disable pip cache
    PIP_DISABLE_PIP_VERSION_CHECK=1 \ # Disable pip version check
    PYTHONPATH=/app \              # Set Python path
    HOME=/home/testuser \          # Set home directory
    DISPLAY=:99                    # Set display for virtual framebuffer

# Set the working directory
WORKDIR /app

###################
# User Setup
###################

# Create test user and required directories
RUN useradd -m testuser && \
    mkdir -p /app/test-results/logs /app/logs && \
    mkdir -p /tmp/.X11-unix && \
    chmod 1777 /tmp/.X11-unix && \
    chown -R testuser:testuser /app /app/test-results /app/logs

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
        xvfb \          # Virtual framebuffer
        libxi6 \        # X11 library
        libgconf-2-4 \  # GConf library
        default-jdk \   # Java runtime
        ca-certificates \ # SSL certificates
        procps && \     # Process utilities
    # Add Chrome repository and install Chrome
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

###################
# ChromeDriver Setup
###################

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

###################
# Python Dependencies
###################

# Copy and install Python requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt pytest-html

###################
# Entrypoint Setup
###################

# Create entrypoint script
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

# Run tests
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

###################
# Final Setup
###################

# Copy the project files
COPY --chown=testuser:testuser . /app/

# Ensure all files are owned by testuser
RUN chown -R testuser:testuser /app

# Switch to non-root user for security
USER testuser

# Set the entrypoint
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]