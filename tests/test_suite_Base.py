import sys
import traceback
import os
import shutil
import subprocess
import logging
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


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

    # Configure logging with multiple handlers for different log levels
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(log_dir, 'selenium_tests.log')),
            logging.FileHandler(os.path.join(log_dir, 'selenium_debug.log'), level=logging.DEBUG),
            logging.FileHandler(os.path.join(log_dir, 'selenium_errors.log'), level=logging.ERROR)
        ]
    )

    # Create class logger
    logger = logging.getLogger(__name__)

    @classmethod
    def get_driver(cls) -> WebDriver:
        """
        Creates and returns a WebDriver instance based on configuration.
        Returns local Chrome WebDriver or Remote WebDriver for Grid.

        Returns:
            WebDriver: Configured WebDriver instance

        Raises:
            WebDriverException: If driver creation fails
            Exception: For other unexpected errors
        """
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
        """
        Creates a local Chrome WebDriver instance.

        Args:
            chrome_options: Configured ChromeOptions instance

        Returns:
            WebDriver: Local Chrome WebDriver instance
        """
        cls.logger.info("Setting up local Chrome WebDriver...")

        try:
            cls._ensure_chrome_installed()

            driver_path = ChromeDriverManager().install()
            os.chmod(driver_path, 0o755)

            service = Service(
                executable_path=driver_path,
                log_path=os.path.join(cls.log_dir, 'chromedriver.log')
            )

            driver = webdriver.Chrome(service=service, options=chrome_options)
            cls._configure_driver_timeouts(driver)

            cls.logger.info("Local Chrome WebDriver created successfully")
            return driver

        except Exception as e:
            cls._log_driver_creation_error(e, chrome_options)
            raise

    @classmethod
    def _create_grid_driver(cls, chrome_options: ChromeOptions) -> WebDriver:
        """
        Creates a Remote WebDriver instance connected to Selenium Grid.

        Args:
            chrome_options: Configured ChromeOptions instance

        Returns:
            WebDriver: Remote WebDriver instance
        """
        cls.logger.info(f"Connecting to Selenium Grid at {cls.SELENIUM_GRID_URL}")

        try:
            remote_connection = RemoteConnection(cls.SELENIUM_GRID_URL)

            # Configure Grid-specific capabilities
            chrome_options.set_capability('platformName', 'linux')
            chrome_options.set_capability('se:noVNC', True)
            chrome_options.set_capability('se:vncEnabled', True)
            chrome_options.set_capability('acceptInsecureCerts', True)

            driver = webdriver.Remote(
                command_executor=remote_connection,
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
        """
        Configures standard timeouts for the WebDriver instance.

        Args:
            driver: WebDriver instance to configure
        """
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        driver.set_script_timeout(30)

    @classmethod
    def _ensure_chrome_installed(cls) -> None:
        """
        Verifies Chrome browser installation.

        Raises:
            Exception: If Chrome installation check fails
        """
        try:
            chrome_path = shutil.which('google-chrome') or shutil.which('chrome')
            if chrome_path:
                cls.logger.info(f"Chrome found at: {chrome_path}")
                return

            cls.logger.info("Chrome not found. Using WebDriver Manager to manage Chrome.")

        except Exception as e:
            cls.logger.error(f"Chrome installation check failed: {str(e)}")
            raise

    @classmethod
    def _log_driver_creation_error(cls, error: Exception, chrome_options: ChromeOptions) -> None:
        """
        Logs detailed information about driver creation failures.

        Args:
            error: The exception that occurred
            chrome_options: The ChromeOptions instance being used
        """
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
        """
        Safely disposes of the WebDriver instance.

        Args:
            driver: WebDriver instance to dispose
        """
        if driver is not None:
            try:
                driver.quit()
                cls.logger.info("WebDriver session terminated successfully")
            except Exception as e:
                cls.logger.error(f"Error while disposing driver: {str(e)}")

    @staticmethod
    def get_web_driver_options() -> ChromeOptions:
        """
        Configures and returns Chrome WebDriver options.

        Returns:
            ChromeOptions: Configured options instance
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

        # Remote debugging configuration
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option('useAutomationExtension', False)

        # Logging configurations
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--log-level=3')

        return options