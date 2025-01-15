import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_network_connectivity():
    """Test basic network connectivity to multiple endpoints"""
    test_urls = [
        'https://www.google.com',
        'https://www.github.com',
        'https://www.example.com'
    ]

    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            assert response.status_code == 200, f"Failed to connect to {url}"
        except requests.RequestException as e:
            pytest.fail(f"Network connectivity test failed for {url}: {e}")


def test_selenium_connection():
    """Comprehensive Selenium connectivity and basic functionality test"""
    try:
        # Configure Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')

        # Create Remote WebDriver connection
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options
        )

        try:
            # Navigate to test website
            driver.get('https://www.example.com')

            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )

            # Additional checks
            assert driver.title is not None, "Page title is empty"
            assert driver.current_url == 'https://www.example.com/', "Incorrect URL"

        finally:
            # Always ensure driver is closed
            driver.quit()

    except Exception as e:
        pytest.fail(f"Selenium connection test failed: {e}")


def test_browser_capabilities():
    """Test Selenium Grid browser capabilities"""
    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        # Create Remote WebDriver connection
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options
        )

        try:
            # Check browser capabilities
            capabilities = driver.capabilities

            assert 'chrome' in capabilities['browserName'].lower(), "Not using Chrome"
            assert capabilities['browserVersion'] is not None, "Browser version not detected"

        finally:
            # Always ensure driver is closed
            driver.quit()

    except Exception as e:
        pytest.fail(f"Browser capabilities test failed: {e}")