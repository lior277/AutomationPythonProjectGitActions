from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX
from Infrastructure.objects.objects_ui.google_search_image_page_ui import GoogleSearchImagePageUi


class GoogleHomePageUi:
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    # locators
        self.__images_link = By.CSS_SELECTOR, "a[aria-label='Search for Images ']"

    def click_on_images_link(self)-> GoogleSearchImagePageUi:
        DriverEX.force_click(driver=self.driver, by=self.__images_link)
        return GoogleSearchImagePageUi(self.driver)

