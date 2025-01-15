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
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    unzip \
    gnupg \
    libgconf-2-4 \
    libx11-6 \
    libx11-xcb1 \
    libxdamage1 \
    libxrandr2 \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libxss1 \
    libasound2 \
    libxtst6 \
    libappindicator3-1 \
    fonts-liberation \
    xdg-utils \
    libvulkan1 \
    libgbm1 \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1) \
    && CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_MAJOR_VERSION}) \
    && wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64.zip chromedriver-linux64

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Create test results directory with proper permissions
RUN mkdir -p /app/test-results && chmod 777 /app/test-results

# Create pytest configuration file
RUN echo "[pytest]\n\
asyncio_mode = auto\n\
asyncio_default_fixture_loop_scope = function\n\
html_report_title = Test Report\n\
html_report_template = null\n\
html_report_theme = dark" > /app/pytest.ini

# Copy the rest of the application code
COPY . /app

# Ensure all necessary directories have correct permissions
RUN mkdir -p /app/logs && \
    chmod 777 /app/logs && \
    chmod 777 /app/test-results

# Create a