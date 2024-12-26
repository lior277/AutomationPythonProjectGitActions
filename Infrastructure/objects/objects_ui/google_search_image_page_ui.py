from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX
from Infrastructure.objects.objects_ui.google_images_page_ui import GoogleImagesPageUi


class GoogleSearchImagePageUi:
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    # locators
        self.__search_for_images_text_box = By.CSS_SELECTOR, "textarea[name='q']"

        self.__search_images_button = (By.CSS_SELECTOR,
                            "button[type='submit'][aria-label='Google Search']")

    def set_image_name(self, name: str):
        DriverEX.send_keys_auto(driver=self.driver,
                                by=self.__search_for_images_text_box, input_text=name)
        return self

    def click_on_search_images_button(self) -> GoogleImagesPageUi:
        DriverEX.force_click(self, driver=self.driver, by=self.__search_images_button)
        return GoogleImagesPageUi(self.driver)
