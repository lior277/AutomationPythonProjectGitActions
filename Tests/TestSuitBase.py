import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class TestSuitBase:
    browser_name = ""

    def get_browser(browser_name: string) -> string:
        TestSuitBase.browser_name = browser_name
        return browser_name

    def get_driver(self) -> webdriver:
        if TestSuitBase.browser_name.lower() == "chrome":
            chrome_option = TestSuitBase.get_web_driver_options(self="chrome")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_option)
            driver.maximize_window()
        elif TestSuitBase.browser_name.lower() == "firefox":
            firefox_option = TestSuitBase.get_web_driver_options(self="firefox")
            firefox_binary_path = '/usr/bin/firefox'
            options = firefox_option
            options.binary_location = firefox_binary_path
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()
            # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_option)
        else:
            raise Exception("Unknown browser")
        return driver

    def get_web_driver_options(self) -> webdriver:
        match self:
            case "chrome":
                options = webdriver.ChromeOptions()
                options.add_argument('--start-maximised')
                options.add_argument('--window-size=1920,1080')
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
