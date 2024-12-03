
from injector import inject
from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX


class HomePageUi:
    @inject
    def __init__(self, driver):
        self.driver = driver

    # locators
        self.__product = "//a[contains(.,'{0}')]"

    def click_on_item_from_home_store(self, product_name: str):
        locator = By.XPATH, self.__product.format(product_name)
        DriverEX.force_click(self.driver, locator)
        return self
