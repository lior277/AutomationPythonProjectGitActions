from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions


class TestSuitBase:
    SELENIUM_GRID_URL = "http://selenium-router:4444/wd/hub"
    RUN_LOCALLY = False

    @staticmethod
    def get_driver() -> webdriver:
        chrome_options = TestSuitBase.get_web_driver_options()

        print("Running tests on Selenium Grid...")
        try:
            # Set capabilities through ChromeOptions
            chrome_options.set_capability('browserName', 'chrome')
            chrome_options.set_capability('platformName', 'linux')
            chrome_options.set_capability('se:noVnc', True)
            chrome_options.set_capability('se:vncEnabled', True)

            driver = webdriver.Remote(
                command_executor=TestSuitBase.SELENIUM_GRID_URL,
                options=chrome_options
            )
            print(f"Successfully connected to Selenium Grid at {TestSuitBase.SELENIUM_GRID_URL}")
            return driver
        except WebDriverException as e:
            print(f"Error connecting to Selenium Grid at {TestSuitBase.SELENIUM_GRID_URL}: {e}")
            raise

    @staticmethod
    def driver_dispose(driver: webdriver = None):
        if driver is not None:
            try:
                driver.quit()
                print("WebDriver session successfully terminated.")
            except Exception as e:
                print(f"Error while quitting driver: {e}")

    @staticmethod
    def get_web_driver_options() -> ChromeOptions:
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

        # Additional stability options
        options.add_argument('--disable-extensions')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-web-security')

        return options