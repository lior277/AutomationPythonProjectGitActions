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
    # ... (previous logging setup remains the same)

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
            # More comprehensive Chrome options
            chrome_options.add_argument('--remote-allow-origins=*')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--allow-insecure-localhost')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            # Experimental options for compatibility
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            # Attempt to get ChromeDriver with automatic version matching
            service = ChromeService(ChromeDriverManager().install())

            cls.logger.info(f"Using ChromeDriver from: {service.path}")

            driver = webdriver.Chrome(
                service=service,
                options=chrome_options
            )

            # Use JavaScript to set window size and maximize
            driver.set_window_size(1920, 1080)
            driver.execute_script("window.focus();")

            cls.logger.info("Local Chrome WebDriver created successfully")
            return driver

        except Exception as e:
            cls.logger.error("Comprehensive WebDriver initialization failure:")
            cls.logger.error(f"Error details: {str(e)}")
            cls.logger.error(f"Traceback: {traceback.format_exc()}")
            cls.logger.error("Troubleshooting steps:")
            cls.logger.error("1. Verify Chrome browser version")
            cls.logger.error("2. Ensure ChromeDriver compatibility")
            cls.logger.error("3. Check Selenium and WebDriver Manager versions")
            cls.logger.error("4. Verify system configuration")

            # Additional diagnostic information
            cls.logger.debug(f"Python version: {sys.version}")
            cls.logger.debug(f"Platform: {platform.platform()}")

            raise

    # ... (rest of the class remains the same)

    @staticmethod
    def get_web_driver_options() -> ChromeOptions:
        """Configures Chrome options with enhanced compatibility."""
        options = ChromeOptions()

        # Basic options
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=en-GB')

        # Performance and compatibility options
        options.add_argument('--remote-allow-origins=*')
        options.add_argument('--disable-web-security')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-insecure-localhost')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Logging and performance
        options.add_argument('--log-level=3')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')

        # Disable browser features that might cause issues
        options.add_experimental_option('excludeSwitches',
                                        ['enable-logging', 'enable-automation', 'ignore-certificate-errors']
                                        )
        options.add_experimental_option('useAutomationExtension', False)

        # Headless mode for CI
        if os.getenv('CI', 'false').lower() == 'true':
            options.add_argument('--headless=new')

        return options