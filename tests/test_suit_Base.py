from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class TestSuitBase:
    @staticmethod
    def get_driver() -> webdriver:
        chrome_options = TestSuitBase.get_web_driver_options()

        # Automatically fetch the correct version of chromedriver
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),  # Automatically gets the right version
            options=chrome_options
        )

        driver.maximize_window()
        return driver

    @staticmethod
    def driver_dispose(driver: webdriver = None):
        if driver is not None:
            driver.close()
        if driver is not None:
            driver.quit()

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
        return options
