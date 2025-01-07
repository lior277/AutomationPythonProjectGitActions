from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os

class TestSuitBase:
    @staticmethod
    def get_driver() -> webdriver:
        chrome_options = ChromeOptions()

        # Check if we are in debug mode (you can set this as an environment variable or a flag)
        is_debug = os.getenv('DEBUG_MODE', 'false').lower() == 'false'

        if is_debug:
            # Disable headless mode for debugging (GUI mode)
            print("Running in debug mode - Chrome GUI will open.")
            chrome_options.add_argument('--no-sandbox')  # Needed for some systems in Docker
            chrome_options.add_argument('--disable-dev-shm-usage')  # Docker-related fix
            # No need for headless in debug mode
        else:
            # Run in headless mode for non-debug runs (ideal for CI/CD)
            print("Running in headless mode - No GUI.")
            chrome_options.add_argument('--headless')  # Chrome will run in headless mode
            chrome_options.add_argument('--no-sandbox')  # Needed for some systems in Docker
            chrome_options.add_argument('--disable-dev-shm-usage')  # Docker-related fix

        # Set up the WebDriver to use Selenium Grid (point to the Hub)
        driver = webdriver.Remote(
            command_executor='http://selenium-hub:4444/wd/hub',
            options=chrome_options
        )

        # Optionally, you can specify window size for non-headless mode
        if is_debug:
            chrome_options.add_argument('window-size=1920x1080')  # Fixed window size for debugging

        return driver

    @staticmethod
    def driver_dispose(driver: webdriver = None):
        if driver is not None:
            driver.close()
        if driver is not None:
            driver.quit()
