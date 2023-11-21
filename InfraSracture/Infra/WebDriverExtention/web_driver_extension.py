from time import sleep
from selenium.common import StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException, \
    ElementNotVisibleException, ElementNotSelectableException, InvalidSelectorException, NoSuchFrameException, \
    WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement


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
    def __init__(self, by: By):
        self.by = by

    def __call__(self, driver: webdriver) -> WebElement:
        try:
            element = driver.find_element(*self.by)
            return element
        except StaleElementReferenceException:
            return None


class ScrollToElement(object):
    def __init__(self, by: By):
        self.by = by

    def __call__(self, driver: webdriver) -> WebElement:
        try:
            element = driver.find_element(*self.by)
            driver.execute_script("arguments[0]" + ".scrollIntoView(alignToTop = false);", element)
            sleep(0.5)
            return element
        except StaleElementReferenceException:
            return None


class ForceClick(object):
    def __init__(self, by: By):
        self.by = by

    def __call__(self, driver: webdriver) -> WebElement:
        try:
            element = driver.find_element(*self.by)

            if element.is_enabled():
                element.click()

            return element
        except StaleElementReferenceException:
            return None
        except ElementNotInteractableException as e:
            ScrollToElement(by=By)
            return None


class WebDriver:

    @staticmethod
    def search_element(driver: webdriver, by: By):
        return (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
                .until(SearchElement(by)))

    @staticmethod
    def force_click(driver: webdriver, by: By):
        (WebDriverWait(driver=driver, timeout=30, ignored_exceptions=ignore_exception_types())
         .until(ForceClick(by)))

#     def __call__(self):
#         try:
#             element = self.driver.find_element(self.by)
#             return element
#
#         except StaleElementReferenceException as e:
#             sleep(0.4)
#             return None
#
#
#
#
# class ScrollToView(object):
#     def __init__(self, by):
#         self.by = by
#
#     def __call__(self, driver):
#         try:
#             element = driver.find_element(self.by)
#             driver.execute_script(
#                 "arguments[0]" + ".scrollIntoView(alignToTop = false);", element)
#
#             sleep(0.5)
#             return element
#
#         except StaleElementReferenceException as e:
#             sleep(0.4)
#             return None
#
#
# def wait_for_scroll(by, timeout=30):
#     return (WebDriverWait(driver=driver, timeout=timeout, ignored_exceptions=ignore_exception_types())
#             .until(ScrollToView(by)))
#
#
# class ForceClick(object):
#     def __init__(self, by, driver):
#         self.by = by
#         self.driver = driver
#
#     def __call__(self):
#         try:
#             element = self.driver.find_element(self.by)
#             if element.is_enabled():
#                 element.click()
#
#             return element
#
#         except StaleElementReferenceException as e:
#             sleep(0.4)
#             return None
#         except ElementNotInteractableException as e:
#             wait_for_scroll(by=By)
#             return None
#
#
# def wait_for_search_element(by, timeout=30):
#     return (WebDriverWait(driver=driver, timeout=timeout, ignored_exceptions=ignore_exception_types())
#             .until(SearchElement(by)))
#
#
# def wait_for_click(driver: driver, by: By, timeout: timeout = 300):
#     return (WebDriverWait(driver=driver, timeout=timeout, poll_frequency=0.5, ignored_exceptions=ignore_exception_types())
#             .until(ForceClick(by, driver)))
#
#
# class ElementHasCssClass(object):
#
#     def __init__(self, locator):
#         self.locator = locator
#
#     def __call__(self, driver):
#         element = driver.find_element(*self.locator)
#
#         if element is not None:
#             return element
#         else:
#             return False
#
#
# wait = WebDriverWait(driver, 10)
# element = wait.until(ElementHasCssClass((By.ID, 'myNewInput')))
