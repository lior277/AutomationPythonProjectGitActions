from typing import Any, List

from selenium.common import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException, \
    ElementNotVisibleException, ElementNotSelectableException, InvalidSelectorException, NoSuchFrameException, \
    WebDriverException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from time import sleep

from Infrastructure.Infra.dal.string_extentions.string_extentions import is_null_or_empty


def ignore_exception_types():
    return [
        NoSuchElementException,
        ElementNotInteractableException,
        ElementNotVisibleException,
        ElementNotSelectableException,
        InvalidSelectorException,
        NoSuchFrameException,
        WebDriverException
    ]

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

class NavigateToUrl(object):
    def __init__(self, url: str):
        self.url = url

    def __call__(self, driver: webdriver) -> None:
        try:
            driver.get(self.url)
        except StaleElementReferenceException:
            sleep(0.3)

        return None

class SearchElements(object):
    def __init__(self, by: tuple):
        self.by = by

    def __call__(self, driver: webdriver) -> Any:
        try:
            elements = driver.find_elements(*self.by)
            return elements

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
        except ElementNotInteractableException as e:
            ScrollToElement(self.by)(driver)
            return None

class ForceClick(object):
    def __init__(self, by: tuple):
        self.by = by

    def __call__(self, driver: WebDriver) -> WebElement:
        try:
            if isinstance(self.by, tuple):
                element = driver.find_element(*self.by)

            elif isinstance(self.by, WebElement):
                element = self.by
            else:
                raise ValueError("Argument 'by' should be a tuple or WebElement.")

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
            new_text = GetElementText(self.by)(driver)

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

                return str(result) if result else ""

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
    def navigate_to_url(driver: webdriver, url: str) -> WebElement:
        return (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
                .until(NavigateToUrl(url)))

    @staticmethod
    def search_elements(driver: webdriver, by: tuple) -> List[WebElement]:
        return (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
                .until(SearchElements(by)))

    @staticmethod
    def force_click(driver: WebDriver, by) -> None:
        force_click = ForceClick(by)
        WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types()) \
            .until(force_click)

    @staticmethod
    def get_element_text(driver: webdriver, by: tuple) -> str:
        return (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
                .until(GetElementText(by=by)))

    @staticmethod
    def send_keys_auto(driver: webdriver, by: tuple, input_text: str) -> None:
        (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
         .until(SendsKeysAuto(by=by, input_text=input_text)))
