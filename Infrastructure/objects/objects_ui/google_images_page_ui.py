from datetime import datetime
from tkinter import Image
from PIL import Image
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX



class GoogleImagesPageUi:
    def __init__(self, driver: webdriver) -> None:
        self.driver = driver

    # locators
        self.__images = By.CSS_SELECTOR, "div[data-q] g-img.mNsIhb"
        self.__image_details = "div a img[alt*='{0}'][aria-hidden='false']"
        self.__self_image = By.CSS_SELECTOR, "img"


    def __calcuate_image_position(self, character_id: int) -> int:
        """Helper function to calculate the position of the image by character ID."""
        id_str = str(character_id)
        if len(id_str) == 3:
            position = int(id_str[0]) + int(id_str[2])
        elif len(id_str) == 2:
            position = int(id_str[0]) + int(id_str[1])
        else:
            position = int(id_str[0])
        return position

    def click_on_image_by_character_id(self, character_id: int):
        position = self.__calcuate_image_position(character_id)
        image_elements = DriverEX.search_elements(driver=self.driver, by=self.__images)

        if len(image_elements) >= position > 0:
            image_element = image_elements[position - 1]
            DriverEX.force_click(self, driver=self.driver, by=image_element)
        else:
            print(f"Invalid position: {position}. There are only {len(image_elements)} images.")

        return self

    def navigate_to_image_by_url(self, url: str):
        DriverEX.navigate_to_url(driver=self.driver, url=url)
        return self

    def capture_image_from_image_details(self, character_name: str, character_id: int):
        locator = By.CSS_SELECTOR, self.__image_details.format(character_name.split()[0])
        image_element = DriverEX.search_element(driver=self.driver, by=locator)
        location = image_element.location
        size = image_element.size

        # Calculate the position to crop the image (left, top, right, bottom)
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']

        # Capture the screenshot of the entire page
        screenshot_path = "screenshot.png"
        self.driver.save_screenshot(screenshot_path)

        # Open the screenshot using PIL (Python Imaging Library)
        img = Image.open(screenshot_path)
        img_cropped = img.crop((left, top, right, bottom))

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"{character_name}_{character_id}-{timestamp}.jpg"
        img_cropped.save(screenshot_filename)

        print(f"Screenshot saved as {screenshot_filename}")
        return self

    def capture_image(self, character_name: str, character_id: int):
        image_element = DriverEX.search_element(driver=self.driver, by=self.__self_image)
        location = image_element.location
        size = image_element.size
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        screenshot_path =  "screenshot.png"
        self.driver.save_screenshot(screenshot_path)
        img = Image.open(screenshot_path)
        img_cropped = img.crop((left, top, right, bottom))
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_filename = f"{character_name}_{character_id}-{timestamp}.jpg"
        img_cropped.save(screenshot_filename)

        print(f"Screenshot saved as {screenshot_filename}")
        return self



