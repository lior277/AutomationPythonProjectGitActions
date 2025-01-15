# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for Google Chrome and other necessary tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    wget \
    unzip \
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
    gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Get Chrome version and install matching ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | awk -F'.' '{print $1}') && \
    CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION") && \
    echo "Using ChromeDriver version: $CHROMEDRIVER_VERSION" && \
    wget -q "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Add a health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:80/ || exit 1

# Command to run tests
CMD ["/bin/bash", "-c", "pytest -n auto --dist=loadfile tests/ui && pytest -n auto --dist=loadfile tests/api && python main.py"]