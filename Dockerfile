# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install curl and necessary dependencies for Google Chrome
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
    libgbm1 && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN curl -sS https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
    dpkg -i google-chrome.deb || apt-get install -y -f && \
    rm google-chrome.deb

# Install ChromeDriver with fallback
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1,2 || echo "114.0.5735.90") && \
    echo "Resolved Chrome version: $CHROME_VERSION" && \
    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION || echo "114.0.5735.90") && \
    if echo "$CHROMEDRIVER_VERSION" | grep -q 'Error'; then \
        CHROMEDRIVER_VERSION="114.0.5735.90"; \
    fi && \
    echo "Resolved ChromeDriver version: $CHROMEDRIVER_VERSION" && \
    curl -sS https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -o chromedriver.zip && \
    if [ -s chromedriver.zip ]; then \
        unzip chromedriver.zip && \
        mv chromedriver /usr/local/bin/ && \
        rm chromedriver.zip; \
    else \
        echo "Failed to download ChromeDriver. Check ChromeDriver version or network settings." && exit 1; \
    fi

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 80

# Wait for Selenium Hub to be ready, then run tests
CMD /bin/bash -c " \
    until curl -s http://selenium-hub:4444/wd/hub/status | grep -q '\"ready\":true'; do \
        echo 'Waiting for Selenium Hub to be ready...'; sleep 5; \
    done && \
    pytest -n auto --dist=loadfile tests/ui && pytest -n auto --dist=loadfile tests/api && python main.py"
