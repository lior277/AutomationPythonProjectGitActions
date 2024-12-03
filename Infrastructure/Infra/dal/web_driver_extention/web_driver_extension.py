from time import sleep
from typing import Any

from selenium.common import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException, \
    ElementNotVisibleException, ElementNotSelectableException, InvalidSelectorException, NoSuchFrameException, \
    WebDriverException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

from Infrastructure.Infra.dal.string_extentions.string_extentions import is_null_or_empty


def ignore_exception_types():
    ignore_exception = [NoSuchElementException,
                        ElementNotInteractableException,
                        ElementNotVisibleException,
                        ElementNotSelectableException,
                        InvalidSelectorException,
                        NoSuchFrameException,
                        ElementNotInteractableException,
                        WebDriverException]

    return ignore_exception


class SearchElement(object):
    def __init__(self, by: tuple):
        self.by = by

    def __call__(self, driver: webdriver) -> Any:
        try:
            element = driver.find_element(*self.by)
            return element

        except StaleElementReferenceException:
            sleep(0.3)
            return None


class ScrollToElement(object):
    def __init__(self, by: tuple):
        self.by = by

    def __call__(self, driver: webdriver) -> Any:
        try:
            element = driver.find_element(*self.by)
            driver.execute_script("arguments[0]" + ".scrollIntoView(alignToTop = false);", element)
            sleep(0.5)
            return element
        except StaleElementReferenceException:
            sleep(0.3)
            return None


class ForceClick(object):
    def __init__(self, by: tuple):
        self.by = by

    def __call__(self, driver: webdriver) -> Any:
        try:
            element = driver.find_element(*self.by)

            if element.is_enabled():
                element.click()

            return element
        except StaleElementReferenceException:
            sleep(0.3)
            return None
        except ElementNotInteractableException as e:
            ScrollToElement(self.by)
            return None


class SendsKeysAuto(object):
    def __init__(self, by: tuple, input_text: str):
        self.by = by
        self.input_text = input_text

    def __call__(self, driver: webdriver) -> bool:
        try:
            element = driver.find_element(*self.by)
            new_text = DriverEX.get_element_text(driver=driver, by=self.by)

            if self.input_text != new_text:
                element.clear()
                sleep(0.01)
                element.send_keys(self.input_text)
                return False
            else:
                return True

        except StaleElementReferenceException:
            sleep(0.3)
            return False


class GetElementText(object):
    def __init__(self, by: tuple):
        self.by = by

    def __call__(self, driver: webdriver) -> str:
        try:
            element = driver.find_element(*self.by)
            new_string = element.get_attribute("innerText")

            if is_null_or_empty(new_string):
                new_string = element.get_attribute("value")
                result = new_string or "Default Value"
                return str(result)

            return str(new_string)

        except StaleElementReferenceException:
            sleep(0.3)
            return None


class DriverEX:

    @staticmethod
    def search_element(driver: webdriver, by: tuple) -> WebElement:
        return (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
                .until(SearchElement(by)))

    @staticmethod
    def force_click(driver: webdriver, by: tuple) -> None:
        (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
         .until(ForceClick(by)))

    @staticmethod
    def get_element_text(driver: webdriver, by: tuple) -> str:
        return (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
                .until(GetElementText(by=by)))

    @staticmethod
    def send_keys_auto(driver: webdriver, by: tuple, input_text: str) -> None:
        (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
         .until(SendsKeysAuto(by=by, input_text=input_text)))
