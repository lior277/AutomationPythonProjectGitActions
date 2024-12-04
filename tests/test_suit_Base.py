from playwright.sync_api import sync_playwright, Page
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class TestSuitBase:
    """A base class for setting up and managing browser drivers with Selenium or Playwright."""

    @staticmethod
    def get_driver(browser_name: str) -> webdriver:
        """
        Returns a Selenium WebDriver instance based on the specified browser name.

        :param browser_name: The name of the browser ('chrome' or 'firefox').
        :return: A WebDriver instance.
        """
        if browser_name.lower() == "chrome":
            chrome_options = TestSuitBase.get_web_driver_options("chrome")
            driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()), options=chrome_options
            )
            driver.maximize_window()
        elif browser_name.lower() == "firefox":
            firefox_options = TestSuitBase.get_web_driver_options("firefox")
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()), options=firefox_options
            )
            driver.maximize_window()
        else:
            raise ValueError("Unsupported browser: Use 'chrome' or 'firefox'.")
        return driver

    @staticmethod
    def driver_dispose(page: Page = None, driver: webdriver = None):
        """
        Closes and disposes of the browser driver or Playwright page.

        :param page: A Playwright Page instance to close.
        :param driver: A Selenium WebDriver instance to quit.
        """
        if page is not None:
            page.context.close()
            page.close()

        if driver is not None:
            driver.quit()  # Quit Selenium driver session

    @staticmethod
    def get_driver_playwright(browser_name: str):
        """
        Returns a Playwright page instance for the specified browser.

        :param browser_name: The name of the browser ('chrome' or 'firefox').
        :return: A tuple of (page, playwright) for interaction and cleanup.
        """
        playwright = sync_playwright().start()
        if browser_name.lower() == "chrome":
            browser = playwright.chromium.launch(headless=False)
        elif browser_name.lower() == "firefox":
            browser = playwright.firefox.launch(headless=False)
        else:
            raise ValueError("Invalid browser name. Use 'chrome' or 'firefox'.")

        page = browser.new_page()
        return page, playwright  # Return both page and playwright instance for cleanup

    @staticmethod
    def get_web_driver_options(browser_name: str):
        """
        Returns WebDriver options for the specified browser.

        :param browser_name: The name of the browser ('chrome' or 'firefox').
        :return: WebDriver options instance.
        """
        if browser_name.lower() == "chrome":
            options = ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
            return options
        elif browser_name.lower() == "firefox":
            options = FirefoxOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
            return options
        else:
            raise ValueError("Unsupported browser: Use 'chrome' or 'firefox'.")
