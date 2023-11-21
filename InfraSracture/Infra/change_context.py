from InfraSracture.Objects.collection_page import CollectionPage
from InfraSracture.Objects.customer_login_page import CustomerLoginPage
from InfraSracture.Objects.luma_home_page import LumaHomePage
from selenium import webdriver


class ChangeContext:
    def __init__(self, driver: webdriver):
        self.driver = driver

    def luma_home_page(self):
        return LumaHomePage(self.driver)

    def collection_page(self):
        return CollectionPage(self.driver)

    def customer_login_page(self):
        return CustomerLoginPage(self.driver)
