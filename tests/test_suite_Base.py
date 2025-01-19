from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.remote_connection import RemoteConnection
import logging


class TestSuiteBase:
    SELENIUM_GRID_URL = "http://localhost:4444/wd/hub"  # Changed from selenium-hub to localhost
    RUN_LOCALLY = True  # Changed to True for local execution

    @classmethod
    def get_driver(cls) -> webdriver:
        """
        Create and return a Selenium WebDriver instance.
        Returns:
            webdriver: Configured WebDriver instance
        """
        chrome_options = cls.get_web_driver_options()

        if cls.RUN_LOCALLY:
            try:
                # Create local Chrome WebDriver
                driver = webdriver.Chrome(options=chrome_options)
                logging.info("Successfully created local Chrome WebDriver")
                return driver
            except WebDriverException as e:
                logging.error(f"Error creating local Chrome WebDriver: {e}")
                raise
        else:
            # Grid execution code
            logging.info("Attempting to connect to Selenium Grid...")
            try:
                remote_connection = RemoteConnection(cls.SELENIUM_GRID_URL)

                # Set capabilities
                chrome_options.set_capability('platformName', 'linux')
                chrome_options.set_capability('se:noVNC', True)
                chrome_options.set_capability('se:vncEnabled', True)

                driver = webdriver.Remote(
                    command_executor=remote_connection,
                    options=chrome_options
                )

                driver.set_page_load_timeout(30)
                driver.implicitly_wait(10)

                logging.info(f"Successfully connected to Selenium Grid at {cls.SELENIUM_GRID_URL}")
                return driver

            except WebDriverException as e:
                logging.error(f"Error connecting to Selenium Grid at {cls.SELENIUM_GRID_URL}: {e}")
                raise

    @classmethod
    def driver_dispose(cls, driver: webdriver = None):
        """
        Safely quit the WebDriver session.

        Args:
            driver (webdriver, optional): WebDriver instance to quit
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

        Returns:
            ChromeOptions: Configured Chrome options
        """
        options = ChromeOptions()

        # Required for running in container
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Headless configuration
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')

        # Window and language settings
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--lang=en-GB')

        # Additional stability and performance options
        options.add_argument('--disable-extensions')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-web-security')

        # Performance and logging options
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-software-rasterizer')

        # Logging configuration
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        return options


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)