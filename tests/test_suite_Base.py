import sys
import platform
import traceback
import os
import logging
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class TestSuiteBase:
    """Base class for Selenium test suite with support for both local and grid execution."""

    # Environment detection
    PLATFORM = platform.system().lower()
    IS_WINDOWS = PLATFORM == 'windows'
    IS_CI = os.getenv('CI', '').lower() == 'true'
    IS_GITHUB_ACTIONS = os.getenv('GITHUB_ACTIONS', '').lower() == 'true'

    # **Force local execution (ignoring SELENIUM_GRID_URL)**
    RUN_LOCALLY = False  # Ensure local execution

    # Set up logging configuration
    log_dir = os.path.join(os.getcwd(), 'test-results', 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Configure logging with a single formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # Create handlers
    stream_handler = logging.StreamHandler()
    test_file_handler = logging.FileHandler(os.path.join(log_dir, 'selenium_tests.log'))
    debug_file_handler = logging.FileHandler(os.path.join(log_dir, 'selenium_debug.log'))

    # Set levels for handlers
    stream_handler.setLevel(logging.INFO)
    test_file_handler.setLevel(logging.INFO)
    debug_file_handler.setLevel(logging.DEBUG)

    # Set formatters for handlers
    stream_handler.setFormatter(formatter)
    test_file_handler.setFormatter(formatter)
    debug_file_handler.setFormatter(formatter)

    # Get the root logger and add handlers
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stream_handler)
    root_logger.addHandler(test_file_handler)
    root_logger.addHandler(debug_file_handler)

    # Create class logger
    logger = logging.getLogger(__name__)

    @classmethod
    def get_driver(cls) -> WebDriver:
        """Creates and returns a WebDriver instance based on configuration."""
        cls.logger.info(f"Platform: {cls.PLATFORM}")
        cls.logger.info(f"CI Mode: {cls.IS_CI}")
        cls.logger.info(f"GitHub Actions: {cls.IS_GITHUB_ACTIONS}")
        cls.logger.info(f"Running locally: {cls.RUN_LOCALLY}")

        # Get browser options
        chrome_options = cls.get_web_driver_options()

        try:
            cls.logger.info("Forcing local Chrome WebDriver")
            return cls._create_local_driver(chrome_options)
        except Exception as e:
            cls.logger.error(f"Failed to create WebDriver: {str(e)}")
            cls.logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    @classmethod
    def _create_local_driver(cls, chrome_options: ChromeOptions) -> WebDriver:
        """Creates a local Chrome WebDriver instance."""
        try:
            # Use WebDriver Manager to handle ChromeDriver installation and version matching
            service = ChromeService(ChromeDriverManager().install())

            cls.logger.info("Attempting to create Chrome WebDriver")

            driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )

            cls._configure_driver_timeouts(driver)
            driver.maximize_window()

            cls.logger.info("Local Chrome WebDriver created successfully")
            return driver

        except WebDriverException as e:
            cls.logger.error("Failed to initialize WebDriver. Potential version mismatch:")
            cls.logger.error(f"Error details: {str(e)}")
            cls.logger.error("Suggestions:")
            cls.logger.error("1. Ensure Chrome browser and ChromeDriver versions are compatible")
            cls.logger.error("2. Update Chrome browser")
            cls.logger.error("3. Manually download matching ChromeDriver")
            raise

        except Exception as e:
            cls._log_driver_creation_error(e, chrome_options)
            raise

    @classmethod
    def _configure_driver_timeouts(cls, driver: WebDriver) -> None:
        """Sets standard timeouts for WebDriver."""
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        driver.set_script_timeout(30)

    @classmethod
    def _log_driver_creation_error(cls, error: Exception, chrome_options: ChromeOptions) -> None:
        """Logs detailed error information."""
        cls.logger.error(f"WebDriver creation failed: {str(error)}")
        cls.logger.error(f"Traceback: {traceback.format_exc()}")
        cls.logger.debug(f"Python version: {sys.version}")
        cls.logger.debug(f"Platform: {cls.PLATFORM}")
        cls.logger.debug(f"Chrome options: {chrome_options.arguments}")
        cls.logger.debug(f"Environment variables:")
        cls.logger.debug(f"  CI: {os.environ.get('CI', 'not set')}")
        cls.logger.debug(f"  GITHUB_ACTIONS: {os.environ.get('GITHUB_ACTIONS', 'not set')}")
        cls.logger.debug(f"  RUN_LOCALLY: {os.environ.get('RUN_LOCALLY', 'not set')}")

    @classmethod
    def driver_dispose(cls, driver: Optional[WebDriver] = None) -> None:
        """Safely disposes of WebDriver instance."""
        if driver:
            try:
                driver.quit()
                cls.logger.info("WebDriver disposed successfully")
            except Exception as e:
                cls.logger.error(f"Error disposing WebDriver: {str(e)}")

    @staticmethod
    def get_web_driver_options() -> ChromeOptions:
        """Configures Chrome options."""
        options = ChromeOptions()

        # Basic options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=en-GB')

        # Additional language settings
        options.add_argument('--accept-language=en-US,en;q=0.9')

        # Logging configurations
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')

        # Performance and compatibility options
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
        options.add_argument('--ignore-certificate-errors')

        # Add headless mode only in CI
        if os.getenv('CI', 'false').lower() == 'true':
            options.add_argument('--headless=new')
            options.add_argument('--disable-gpu')

        return options