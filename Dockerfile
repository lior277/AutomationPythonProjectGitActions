# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies for Google Chrome, selenium, and ChromeDriver
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    curl \
    wget \
    dpkg \
    libx11-6 \
    libx11-xcb1 \
    libxdamage1 \
    libxrandr2 \
    libgdk-pixbuf2.0-0 \
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
    libappindicator1 \
    fonts-liberation \
    xdg-utils \
    libayatana-appindicator3-1 \
    libdrm2 \
    libgbm1 \
    libvulkan1 \
    libtk8.6 \
    tcl8.6 \
    tk8.6 \
    unzip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Chrome browser
RUN curl -sS https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
    dpkg -i google-chrome.deb && \
    apt-get install -y -f && \
    rm google-chrome.deb

# Install ChromeDriver
RUN curl -sS https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -o chromedriver.zip && \
    unzip chromedriver.zip && \
    mv chromedriver /usr/local/bin/ && \
    rm chromedriver.zip

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run tests
RUN pytest

# Run main.py when the container launches
CMD ["python", "main.py"]