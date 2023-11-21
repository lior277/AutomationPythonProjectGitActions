import string

from selenium.webdriver.common.by import By
from InfraSracture.Infra.WebDriverExtention.web_driver_extension import WebDriver


class CollectionPage:
    def __init__(self, driver):
        self.driver = driver

    __item_in_yoga_collection = By.XPATH, "//a[contains(.,'{0}')]"

    def click_on_item_in_collection(self, item_name: string):
        locator = By.XPATH, "//a[contains(.,'{0}')]".format(item_name)
        WebDriver.force_click(self.driver, locator)
        return self
