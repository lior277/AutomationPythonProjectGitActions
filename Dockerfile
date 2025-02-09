# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/app \
    HOME=/home/testuser

# Set the working directory in the container
WORKDIR /app

# First create the user
RUN useradd -m testuser

# Then create directories and set permissions
RUN mkdir -p /app/test-results/logs && \
    mkdir -p /app/logs && \
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
        procps \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /tmp/.X11-unix \
    && chmod 1777 /tmp/.X11-unix

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp \
    && unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin \
    && rm /tmp/chromedriver_linux64.zip \
    && chmod +x /usr/local/bin/chromedriver

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt pytest-html

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Ensure test-results directory exists and is writable\n\
mkdir -p /app/test-results/logs\n\
chown -R testuser:testuser /app/test-results\n\
chmod 777 /app/test-results\n\
\n\
# Start virtual framebuffer\n\
Xvfb :99 & export DISPLAY=:99\n\
\n\
cd /app\n\
python -m pytest tests/ui/ -v\n\
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