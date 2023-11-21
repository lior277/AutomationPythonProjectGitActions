from selenium.webdriver.common.by import By
from InfraSracture.Infra.WebDriverExtention.web_driver_extension import WebDriver


class LumaHomePage:
    def __init__(self, driver):
        self.driver = driver

    # locators
    shop_new_yoga_btn = By.CSS_SELECTOR, "span[class='more button']"

    def click_on_shop_new_yoga_btn(self):
        WebDriver.force_click(self.driver, LumaHomePage.shop_new_yoga_btn)
        return self
