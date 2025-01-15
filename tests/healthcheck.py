import requests
import selenium


def test_selenium_connection():
    """Basic Selenium connectivity test"""
    try:
        # Add a simple Selenium connectivity test
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.example.com')
        driver.quit()
        assert True
    except Exception as e:
        print(f"Selenium connection test failed: {e}")
        raise


def test_network_connectivity():
    """Basic network connectivity test"""
    try:
        response = requests.get('https://www.google.com', timeout=5)
        assert response.status_code == 200
    except Exception as e:
        print(f"Network connectivity test failed: {e}")
        raise