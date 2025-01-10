from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException

class TestSuitBase:
    # Use localhost for testing locally outside Docker; otherwise, use 'selenium-hub' inside Docker
    SELENIUM_GRID_URL = "http://localhost:4444/wd/hub"  # Update to "http://selenium-hub:4444/wd/hub" if running inside Docker
    RUN_LOCALLY = False  # Toggle to True for local debugging

    @staticmethod
    def get_driver() -> webdriver:
        chrome_options = TestSuitBase.get_web_driver_options()

        if TestSuitBase.RUN_LOCALLY:
            print("Running tests locally...")
            try:
                driver = webdriver.Chrome(options=chrome_options)
            except WebDriverException as e:
                print(f"Error initializing local WebDriver: {e}")
                raise
        else:
            print("Running tests on Selenium Grid...")
            try:
                driver = webdriver.Remote(
                    command_executor=TestSuitBase.SELENIUM_GRID_URL,
                    options=chrome_options
                )
            except WebDriverException as e:
                print(f"Error connecting to Selenium Grid at {TestSuitBase.SELENIUM_GRID_URL}: {e}")
                raise

        driver.maximize_window()
        return driver

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
        options.add_argument('--lang=en-GB')
        options.add_argument('--accept-language=en-US,en;q=0.9')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
        options.add_argument('--window-size=1920,1080')  # Ensure tests run in a consistent viewport size
        if not TestSuitBase.RUN_LOCALLY:
            options.add_argument('--headless')  # Headless mode for Grid testing
        return options
