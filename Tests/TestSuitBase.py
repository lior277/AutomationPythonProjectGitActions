import string
from playwright.sync_api import sync_playwright, Page
from selenium import webdriver


class TestSuitBase:

    @staticmethod
    def get_driver(browser_name: string) -> webdriver:
        if browser_name.lower() == "chrome":
            chrome_option = TestSuitBase.get_web_driver_options(browser_name.lower())
            driver = webdriver.Chrome(options=chrome_option)
            # service=ChromeService(ChromeDriverManager().install()), options=chrome_option)
            driver.maximize_window()
        elif browser_name.lower() == "firefox":
            firefox_option = TestSuitBase.get_web_driver_options(browser_name.lower())
            firefox_binary_path = '/usr/bin/firefox'
            options = firefox_option
            options.binary_location = firefox_binary_path
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_option)
        else:
            raise Exception("Unknown browser")
        return driver

    @staticmethod
    def driver_dispose(page: Page = None, driver: webdriver = None):
        if page is not None:
            page.close()

        if driver is not None:
            driver.close()
            driver.quit()

    @staticmethod
    def get_driver_playwright(browser_name: str):
        playwright = sync_playwright().start()
        if browser_name.lower() == 'chrome':
            browser = playwright.chromium.launch(headless=False)
        elif browser_name.lower() == 'firefox':
            browser = playwright.firefox.launch(headless=False)
        else:
            raise ValueError("Invalid browser name. Use 'chromium', 'firefox', or 'webkit'.")

        page = browser.new_page()

        return page

    def get_web_driver_options(self) -> webdriver:
        match self:
            case "chrome":
                options = webdriver.ChromeOptions()
                # options.add_argument('--start-maximised')
                # options.add_argument('--window-size=1920,1080')
                options.add_argument('--ignore-ssl-errors')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-browser-side-navigation')
                options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
                return options

            case "firefox":
                options = webdriver.FirefoxOptions()
                options.add_argument('--ignore-ssl-errors')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-browser-side-navigation')
                options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
                return options
