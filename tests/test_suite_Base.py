import sys
import traceback
import os
import logging
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver

class TestSuiteBase:
    """
    Base class for Selenium test suite with support for both local and grid execution.
    Provides comprehensive logging and driver management functionality.
    """

    # Configuration constants
    SELENIUM_GRID_URL = "http://selenium-hub:4444/wd/hub"
    RUN_LOCALLY = False

    # Set up logging configuration
    log_dir = os.path.join(os.getcwd(), 'test-results', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # Create handlers
    stream_handler = logging.StreamHandler()
    test_file_handler = logging.FileHandler(os.path.join(log_dir, 'selenium_tests.log'))
    debug_file_handler = logging.FileHandler(os.path.join(log_dir, 'selenium_debug.log'))
    error_file_handler = logging.FileHandler(os.path.join(log_dir, 'selenium_errors.log'))

    # Set levels for handlers
    stream_handler.setLevel(logging.INFO)
    test_file_handler.setLevel(logging.INFO)
    debug_file_handler.setLevel(logging.DEBUG)
    error_file_handler.setLevel(logging.ERROR)

    # Set formatters for handlers
    stream_handler.setFormatter(formatter)
    test_file_handler.setFormatter(formatter)
    debug_file_handler.setFormatter(formatter)
    error_file_handler.setFormatter(formatter)

    # Get the root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(test_file_handler)
    root_logger.addHandler(debug_file_handler)
    root_logger.addHandler(error_file_handler)

    # Create class logger
    logger = logging.getLogger(__name__)

    @classmethod
    def get_driver(cls) -> WebDriver:
        """Creates and returns a WebDriver instance based on configuration."""
        chrome_options = cls.get_web_driver_options()

        try:
            if cls.RUN_LOCALLY:
                return cls._create_local_driver(chrome_options)
            else:
                return cls._create_grid_driver(chrome_options)
        except Exception as e:
            cls.logger.error(f"Failed to create WebDriver: {str(e)}")
            cls.logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    @classmethod
    def _create_local_driver(cls, chrome_options: ChromeOptions) -> WebDriver:
        """Creates a local Chrome WebDriver instance."""
        cls.logger.info("Setting up local Chrome WebDriver...")

        try:
            service = Service()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            cls._configure_driver_timeouts(driver)
            cls.logger.info("Local Chrome WebDriver created successfully")
            return driver

        except Exception as e:
            cls._log_driver_creation_error(e, chrome_options)
            raise

    @classmethod
    def _create_grid_driver(cls, chrome_options: ChromeOptions) -> WebDriver:
        """Creates a Remote WebDriver instance connected to Selenium Grid."""
        cls.logger.info(f"Connecting to Selenium Grid at {cls.SELENIUM_GRID_URL}")

        try:
            chrome_options.set_capability('platformName', 'linux')
            chrome_options.set_capability('se:noVNC', True)
            chrome_options.set_capability('se:vncEnabled', True)
            chrome_options.set_capability('acceptInsecureCerts', True)

            driver = webdriver.Remote(
                command_executor=cls.SELENIUM_GRID_URL,
                options=chrome_options
            )

            cls._configure_driver_timeouts(driver)
            cls.logger.info("Successfully connected to Selenium Grid")
            return driver

        except WebDriverException as e:
            cls.logger.error(f"Failed to connect to Selenium Grid: {str(e)}")
            cls.logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    @classmethod
    def _configure_driver_timeouts(cls, driver: WebDriver) -> None:
        """Configures standard timeouts for the WebDriver instance."""
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        driver.set_script_timeout(30)

    @classmethod
    def _log_driver_creation_error(cls, error: Exception, chrome_options: ChromeOptions) -> None:
        """Logs detailed information about driver creation failures."""
        cls.logger.error(f"WebDriver creation failed: {str(error)}")
        cls.logger.error(f"Traceback: {traceback.format_exc()}")
        cls.logger.debug(f"Python version: {sys.version}")

        try:
            import selenium
            cls.logger.debug(f"Selenium version: {selenium.__version__}")
        except Exception:
            cls.logger.debug("Could not retrieve Selenium version")

        cls.logger.debug(f"Chrome options: {chrome_options.arguments}")

    @classmethod
    def driver_dispose(cls, driver: Optional[WebDriver] = None) -> None:
        """Safely disposes of the WebDriver instance."""
        if driver is not None:
            try:
                driver.quit()
                cls.logger.info("WebDriver session terminated successfully")
            except Exception as e:
                cls.logger.error(f"Error while disposing driver: {str(e)}")

    @staticmethod
    def get_web_driver_options() -> ChromeOptions:
        """Configures and returns Chrome WebDriver options."""
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

        # Remote debugging configuration
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option('useAutomationExtension', False)

        # Logging configurations
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')

        return options