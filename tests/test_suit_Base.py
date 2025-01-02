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
        is_debug = os.getenv('DEBUG_MODE', 'false').lower() == 'true'

        if is_debug:
            # Disable headless mode for debugging (GUI mode)
            print("Running in debug mode - Chrome GUI will open.")
            chrome_options.add_argument('--no-sandbox')  # Needed for some systems in Docker
            chrome_options.add_argument('--lang=en-GB')
            chrome_options.add_argument('--accept-language=en-US,en;q=0.9')
            chrome_options.add_argument('--disable-dev-shm-usage')  # Docker-related fix
            # No need for headless in debug mode
            chrome_options.add_argument('window-size=1920x1080')  # Fixed window size for debugging
        else:
            # Run in headless mode for non-debug runs (ideal for CI/CD)
            print("Running in headless mode - No GUI.")
            chrome_options.add_argument('--lang=en-GB')
            chrome_options.add_argument('--accept-language=en-US,en;q=0.9')
            chrome_options.add_argument('--headless')  # Chrome will run in headless mode
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-browser-side-navigation')
            chrome_options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')

        # Add common options
        chrome_options.add_argument('--remote-debugging-port=9222')  # Enable debugging

        # Set up the ChromeDriver with ChromeDriverManager
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

        driver.maximize_window()  # Ensure the window is maximized in debug mode
        return driver

    @staticmethod
    def driver_dispose(driver: webdriver = None):
        if driver:
            print("Teardown: Closing the browser.")
            driver.quit()  # This will stop the session and close the browser
