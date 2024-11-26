from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX


class UpperMenuUi:
    def __init__(self, driver):
        self.driver = driver

    # locators
        self.chart_menu = By.CSS_SELECTOR, "a[id='cartur']"
        self.logout_menu = By.CSS_SELECTOR, "a[id='logout2']"

    def click_on_chart_menu_item(self):
        DriverEX.force_click(self.driver, self.chart_menu)
        return self

    def click_on_logout_menu_item(self):
        DriverEX.force_click(self.driver, self.logout_menu)
        return self
