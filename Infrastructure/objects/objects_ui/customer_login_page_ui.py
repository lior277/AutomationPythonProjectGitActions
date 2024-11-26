import string

from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX


class CustomerLoginPageUi:
    def __init__(self, driver):
        self.driver = driver

    # locators
        self.user_name = By.CSS_SELECTOR, "input[id='email']"
        self.password = By.CSS_SELECTOR, "input[id='pass']"
        self.sign_in_btn = By.CSS_SELECTOR, "button[id='send2']"

    def navigate_to_url(self, url: string):
        self.driver.get(url)
        return self

    def set_user_name(self, password="lior277@gmail.com"):
        element = DriverEX.search_element(self.driver, self.user_name)
        element.send_keys(password)
        return self

    def set_password(self, user_name="Liorh963"):
        element = DriverEX.search_element(self.driver, self.password)
        element.send_keys(user_name)
        return self

    def click_on_login_btn(self):
        DriverEX.force_click(self.driver, self.sign_in_btn)
        return self
