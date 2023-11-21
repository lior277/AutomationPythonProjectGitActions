import string

from selenium.webdriver.common.by import By
from InfraSracture.Infra.WebDriverExtention.web_driver_extension import WebDriver


class CustomerLoginPage:
    def __init__(self, driver):
        self.driver = driver

    # locators
    user_name = By.CSS_SELECTOR, "input[id='email']"
    password = By.CSS_SELECTOR, "input[id='pass']"
    sign_in_btn = By.CSS_SELECTOR, "button[id='send2']"

    def navigate_to_url(self, url: string):
        self.driver.get(url)
        return self

    def set_user_name(self, password="lior277@gmail.com"):
        element = WebDriver.search_element(self.driver, CustomerLoginPage.user_name)
        element.send_keys(password)
        return self

    def set_password(self, user_name="Liorh963"):
        element = WebDriver.search_element(self.driver, CustomerLoginPage.password)
        element.send_keys(user_name)
        return self

    def click_on_login_btn(self):
        WebDriver.force_click(self.driver, CustomerLoginPage.sign_in_btn)
        return self
