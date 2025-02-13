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
from webdriver_manager.core.os_manager import ChromeType


class TestSuiteBase:
    # Existing logging setup remains the same

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
        """Creates a local Chrome WebDriver instance with advanced error handling."""
        try:
            # Attempt to get ChromeDriver with specific version matching
            driver_path = ChromeDriverManager(
                chrome_type=ChromeType.GOOGLE
            ).install()

            service = ChromeService(executable_path=driver_path)

            cls.logger.info(f"Using ChromeDriver from: {driver_path}")

            driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )

            cls._configure_driver_timeouts(driver)
            driver.maximize_window()

            cls.logger.info("Local Chrome WebDriver created successfully")
            return driver

        except Exception as e:
            cls.logger.error("Comprehensive WebDriver initialization failure:")
            cls.logger.error(f"Error details: {str(e)}")
            cls.logger.error(f"Traceback: {traceback.format_exc()}")
            cls.logger.error("Troubleshooting steps:")
            cls.logger.error("1. Verify Chrome browser version")
            cls.logger.error("2. Download compatible ChromeDriver manually")
            cls.logger.error("3. Check Selenium and WebDriver Manager versions")
            cls.logger.error("4. Verify system compatibility")

            # Additional diagnostic information
            cls.logger.debug(f"Python version: {sys.version}")
            cls.logger.debug(f"Platform: {platform.platform()}")

            raise

    @classmethod
    def _configure_driver_timeouts(cls, driver: WebDriver) -> None:
        """Sets standard timeouts for WebDriver."""
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        driver.set_script_timeout(30)

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
        """Configures Chrome options with enhanced compatibility."""
        options = ChromeOptions()

        # Basic options
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=en-GB')

        # Enhanced compatibility options
        options.add_argument('--remote-allow-origins=*')
        options.add_experimental_option('useAutomationExtension', False)

        # Disable specific Chrome features that might cause issues
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])

        # Logging and performance
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')

        # Headless mode for CI
        if os.getenv('CI', 'false').lower() == 'true':
            options.add_argument('--headless=new')

        return options