# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies for Chrome and ChromeDriver
RUN apt-get update && \
    apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    libx11-dev \
    libx11-6 \
    libgdk-pixbuf2.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libnss3 \
    libasound2 \
    libxss1 \
    libxtst6 \
    libappindicator3-1 \
    libnspr4 \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt

# Download and install the Chrome browser
RUN curl -sS https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o google-chrome.deb && \
    dpkg -i google-chrome.deb && \
    apt-get install -y -f && \
    rm google-chrome.deb

# Install the ChromeDriver version that corresponds to your version of Chrome
RUN LATEST_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$LATEST_VERSION/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    rm /tmp/chromedriver_linux64.zip

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
