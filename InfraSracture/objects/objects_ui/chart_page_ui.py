from selenium import webdriver
from selenium.webdriver.common.by import By

from InfraSracture.Infra.dal.web_driver_extention.web_driver_extension import DriverEX


class ChartPageUi:
    def __init__(self, driver: webdriver):
        self.driver = driver

    # locators
        self.place_order_btn = By.CSS_SELECTOR, "button[class*='success']"

    def click_on_place_order_btn(self):
        DriverEX.force_click(self.driver, self.place_order_btn)
        return self
