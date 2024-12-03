from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX


class PlaceOrderPageUi:
    def __init__(self, driver: webdriver):
        self.driver = driver

    # locators
        self.__form_fields = "input[id='{0}']"
        self.purchase_btn = By.CSS_SELECTOR, "button[onclick='purchaseOrder()']"

    def set_name(self, name: str):
        locator = By.CSS_SELECTOR, self.__form_fields.format("name")
        DriverEX.send_keys_auto(driver=self.driver, by=locator, input_text=name)
        return self

    def set_country(self, country: str):
        locator = By.CSS_SELECTOR, self.__form_fields.format("country")
        DriverEX.send_keys_auto(driver=self.driver, by=locator, input_text=country)
        return self

    def set_city(self, city: str):
        locator = By.CSS_SELECTOR, self.__form_fields.format("city")
        DriverEX.send_keys_auto(driver=self.driver, by=locator, input_text=city)
        return self

    def set_credit_card(self, card: str):
        locator = By.CSS_SELECTOR, self.__form_fields.format("card")
        DriverEX.send_keys_auto(driver=self.driver, by=locator, input_text=card)
        return self

    def set_month(self, month: str):
        locator = By.CSS_SELECTOR, self.__form_fields.format("month")
        DriverEX.send_keys_auto(driver=self.driver, by=locator, input_text=month)
        return self

    def set_year(self, year: str):
        locator = By.CSS_SELECTOR, self.__form_fields.format("year")
        DriverEX.send_keys_auto(driver=self.driver, by=locator, input_text=year)
        return self

    def click_on_purchase_btn(self):
        DriverEX.force_click(driver=self.driver, by=self.purchase_btn)
        return self

    def place_order_pipe(self, name: str, country: str, city: str,
                         card: str, month: str, year: str):
        self.set_name(name)
        self.set_country(country)
        self.set_city(city)
        self.set_credit_card(card)
        self.set_month(month)
        self.set_year(year)
        self.click_on_purchase_btn()
        return self
