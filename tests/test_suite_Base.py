import sys
import traceback
import os

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.remote_connection import RemoteConnection
import logging

from webdriver_manager.chrome import ChromeDriverManager


class TestSuiteBase:
    SELENIUM_GRID_URL = "http://localhost:4444/wd/hub"
    RUN_LOCALLY = True

    @classmethod
    def get_driver(cls) -> webdriver:
        chrome_options = cls.get_web_driver_options()

        if cls.RUN_LOCALLY:
            try:
                # Standard ChromeDriverManager installation
                driver_path = ChromeDriverManager().install()

                # Verify driver executable permissions
                os.chmod(driver_path, 0o755)

                service = Service(
                    executable_path=driver_path,
                    log_path='chromedriver.log'  # Detailed ChromeDriver logs
                )

                driver = webdriver.Chrome(service=service, options=chrome_options)

                # Additional driver verification
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)

                logging.info("Successfully created local Chrome WebDriver")
                return driver

            except WebDriverException as e:
                # Comprehensive error logging
                logging.error(f"WebDriver Exception: {e}")
                logging.error(f"Detailed traceback: {traceback.format_exc()}")

                # Enhanced system diagnostics
                logging.info(f"Python version: {sys.version}")
                try:
                    import selenium
                    logging.info(f"Selenium version: {selenium.__version__}")
                except Exception:
                    logging.info("Could not retrieve Selenium version")

                # Log Chrome options and path details
                logging.info(f"Chrome options: {chrome_options.arguments}")
                logging.info(f"ChromeDriver path: {driver_path}")

                # Check system environment
                try:
                    import shutil
                    chrome_path = shutil.which('google-chrome') or shutil.which('chrome')
                    logging.info(f"Chrome executable path: {chrome_path}")
                except Exception:
                    logging.error("Could not find Chrome executable")

                raise

        else:
            # Grid execution code
            logging.info("Attempting to connect to Selenium Grid...")
            try:
                remote_connection = RemoteConnection(cls.SELENIUM_GRID_URL)

                # Enhanced capabilities
                chrome_options.set_capability('platformName', 'linux')
                chrome_options.set_capability('se:noVNC', True)
                chrome_options.set_capability('se:vncEnabled', True)
                chrome_options.set_capability('acceptInsecureCerts', True)

                chrome_options.page_load_strategy = 'normal'
                chrome_options.add_argument('--remote-debugging-port=9222')
                chrome_options.add_experimental_option('useAutomationExtension', False)

                driver = webdriver.Remote(
                    command_executor=remote_connection,
                    options=chrome_options
                )

                # Enhanced timeouts
                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)
                driver.set_script_timeout(30)

                logging.info(f"Successfully connected to Selenium Grid at {cls.SELENIUM_GRID_URL}")
                return driver

            except WebDriverException as e:
                logging.error(f"Error connecting to Selenium Grid at {cls.SELENIUM_GRID_URL}: {e}")
                logging.error(f"Detailed traceback: {traceback.format_exc()}")
                raise

    @classmethod
    def driver_dispose(cls, driver: webdriver = None):
        """
        Safely quit the WebDriver session.
        """
        if driver is not None:
            try:
                driver.quit()
                logging.info("WebDriver session successfully terminated.")
            except Exception as e:
                logging.error(f"Error while quitting driver: {e}")

    @staticmethod
    def get_web_driver_options() -> ChromeOptions:
        """
        Configure and return Chrome WebDriver options.
        """
        options = ChromeOptions()

        # Container and system compatibility
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Headless configuration
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

        # Window and language settings
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=en-GB')

        # Security and performance options
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-software-rasterizer')

        # Logging configurations
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')  # Minimal logging

        return options


# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('selenium_tests.log')
    ]
)