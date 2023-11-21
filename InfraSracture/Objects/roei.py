from time import sleep

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as ec

# constants
DEFAULT_TIMEOUT = 15
ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)


class WebDriverExtensions:
    def __init__(self, driver: WebDriver):
        """
        Creates a new instance of this WebDriverExtensions component.

        Args:

        """

        self.driver = driver

    def get_driver(self) -> WebDriver:
        """
        Gets the WebDriver under this context.

        Returns:
            This WebDriver instance (the original instance created by the user)
        """

        return self.driver

    def as_select(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> Select:
        """
        Returns a select element wrapping the element found by a given strategy and locator.
        This method will wait until element exists or until timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            element = e_driver.as_select(By.ID, 'foo')
            element = e_driver.as_select(By.ID, 'foo', 3)

        Returns:
            A select element allows selection by designated functions.

        Raises
            UnexpectedTagNameException: When element is not a SELECT tag.
        """

        element = self.__get_exists(by, timeout)
        return Select(element)

    def force_clear(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Clears the text if it's a text entry element. This method will wait until element exists or until
        timeout reached. The actual clear will be done by sending <BACKSPACE> sequence into the text element.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            e_driver.force_clear(By.ID, 'foo')
            e_driver.force_clear(By.ID, 'foo', 3)

            # can be chained
            e_driver.force_clear(By.ID, 'foo').send_keys('new value')

        Returns:
            WebElement instance (if found).

        Notes:
            Use this method in a very rare cases where 'element.clear()' or even 'execute_script' will not
            clear the element text. There is a 50 milliseconds silent wait between each <BACKSPACE>.
        """

        # get element
        element = self.__get_exists(by, timeout)
        element.send_keys(Keys.END)
        value = element.get_attribute("value")

        # iterate
        for i in range(len(value)):
            element.send_keys(Keys.BACK_SPACE)
            sleep(0.050)

        # return updated element state
        return element

    def force_click(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebDriver:
        """
        Clicks the element. This method will wait until element exists or until
        timeout reached. The element state will be ignored, which means it will be clicked even if it is not
        visible or enabled.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            e_driver.force_click(By.ID, 'foo')
            e_driver.force_click(By.ID, 'foo', 3)

        Returns:
            This WebDriver instance (the driver used to initialize this object).
        """

        element = self.__get_exists(by, timeout)
        self.driver.execute_script("arguments[0].click();", element)
        return self.driver

    def get_actions(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> ActionChains:
        """
        Creates a new ActionChains. This method will wait until element exists or until
        timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Returns:
            A new ActionChains instance.

        Notes:
            You do not need to use 'move_to_element' action when you call this method.
        """

        element = self.__get_exists(by, timeout)
        return ActionChains(self.driver).move_to_element(element)

    def get_element(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Find an element by a given strategy and locator. This method will wait until element exists or until
        timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            element = e_driver.get_element(By.ID, 'foo')
            element = e_driver.get_element(By.ID, 'foo', 3)

        Returns:
            WebElement instance (if found).
        """

        return self.__get_exists(by, timeout)

    def get_elements(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> [WebElement]:
        """
        Find all elements by a given strategy and locator. This method will wait until elements exists or until
        timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            elements = e_driver.get_elements(By.ID, 'foo')
            elements = e_driver.get_elements(By.ID, 'foo', 3)

        Returns:
            A collection of all elements found.
        """

        return WebDriverWait(self.driver, timeout).until(ec.presence_of_all_elements_located(by))

    def get_enabled_element(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Find an element by a given strategy and locator. This method will wait until element is enabled or until
        timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            element = e_driver.get_enabled_element(By.ID, 'foo')
            element = e_driver.get_enabled_element(By.ID, 'foo', 3)

        Returns:
            WebElement instance (if found).
        """

        return self.__get_enabled(by, timeout)

    def get_visible_element(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Find an element by a given strategy and locator. This method will wait until element is visible or until
        timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            element = e_driver.get_visible_element(By.ID, 'foo')
            element = e_driver.get_visible_element(By.ID, 'foo', 3)

        Returns:
            WebElement instance (if found).
        """

        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(by))

    def get_visible_elements(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> [WebElement]:
        """
        Find all elements by a given strategy and locator. This method will wait until elements are visible or until
        timeout reached.

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            elements = e_driver.get_visible_elements(By.ID, 'foo')
            elements = e_driver.get_visible_elements(By.ID, 'foo', 3)

        Returns:
            A collection of all elements found.
        """

        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_all_elements_located(by))

    def until_not_exists_or_hidden(self, by: tuple, timeout: int = DEFAULT_TIMEOUT):
        # setup
        intervals = 1
        state = False

        # initial wait (fixed)
        sleep(1)

        # execute
        while not state and intervals < timeout:
            try:
                element = self.driver.find_element(by=by)
                state = element is not None

                self.logger.debug(f'waiting for element state')
                sleep(1)
                intervals = intervals + 1
            except Exception as e:
                state = True
                self.logger.debug(f'state found [{e.args}]')

    def until_visible(self, by: tuple, timeout: int = DEFAULT_TIMEOUT):
        # setup
        intervals = 1
        state = False

        # initial wait (fixed)
        sleep(1)

        # execute
        while not state and intervals < timeout:
            try:
                is_state = self.driver.find_element(by=by.__getitem__(1), value=by.__getitem__(2)).is_displayed()
                if is_state:
                    return

                self.logger.debug('state found')
            except Exception as e:
                state = False
                self.logger.debug(f'waiting for element state [{e.args}]')

                sleep(1)
                intervals = intervals + 1

    def go_to_url(self, url: str):
        """
        Loads a web page in the current browser session and maximizing the page.

        Args:
            url: URL to load in the current browser session.

        Returns:
            This WebDriver instance (the driver used to initialize this object).
        """

        self.driver.get(url)
        self.driver.maximize_window()
        return self

    def send_keys_with_interval(
            self, by: tuple, value: str, interval: float = 100, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Simulates typing into the element. This method will wait until element exists or until
        timeout reached. The text will be typed into the element using a pace dictated by the interval argument.

        Args:
            by:       Locator strategy to use for finding the element.
            value:    A string for typing, or setting form fields. For setting file inputs,
                      this could be a local file path.
            interval: The time to wait between each character.
            timeout:  Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            e_driver.send_keys_with_interval(By.ID, 'foo')
            e_driver.send_keys_with_interval(By.ID, 'foo', 500)
            e_driver.send_keys_with_interval(By.ID, 'foo', 500, 3)

        Returns:
            WebElement instance (if found).
        """

        element = self.__get_exists(by, timeout)
        for x in value:
            element.send_keys(x)
            sleep(interval / 1000)
        return element

    def send_random_keys(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        """
        Simulates typing into the element. This method will wait until element exists or until
        timeout reached. The text will be typed into the element using a pace dictated by the interval argument.

        Args:
            by:       Locator strategy to use for finding the element.
            timeout:  Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            e_driver.send_keys_with_interval((By.ID, 'foo'))
            e_driver.send_keys_with_interval((By.ID, 'foo'), 3)

        Returns:
            WebElement instance (if found).
        """

        element = self.__get_exists(by, timeout)
        element.send_keys(" ")
        return element

    def submit_form(self, by: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebDriver:
        """
        Submits the form (same as clicking the Submit button).

        Args:
            by:      Locator strategy to use for finding the element.
            timeout: Time to wait before throwing exception for not finding the element (default is 15 seconds).

        Examples:
            e_driver.submit_form(By.ID, 'foo')
            e_driver.submit_form(By.ID, 'foo', 3)

        Returns:
            This WebDriver instance (the driver used to initialize this object).
        """

        # get element
        element = self.__get_exists(by, timeout)

        # verify
        if not element.tag_name == "FORM":
            return self.driver

        # submit
        self.driver.execute_script("arguments[0].submit();", element)
        return self.driver

    def submit_form_by_index(self, index: int = 0) -> WebDriver:
        """
        Submits the form (same as clicking the Submit button).

        Args:
            index: The form zero based index, if there are more than one form.

        Examples:
            e_driver.submit_form_by_index(2)

        Returns:
            This WebDriver instance (the driver used to initialize this object).
        """

        script = "document.forms[{}].submit();".format(index)
        self.driver.execute_script(script)
        return self.driver

    def vertical_window_scroll(self, y_coord: int) -> WebDriver:
        """
        Scrolls the window to a particular place in the document.

        Args:
            y_coord: Pixel along the vertical axis of the document that you want displayed in the upper left.

        Examples:
            e_driver.vertical_window_scroll(1000)

        Returns:
            This WebDriver instance (the driver used to initialize this object).
        """

        script = f'window.scroll(0,{y_coord})'
        self.driver.execute_script(script=script)
        return self.driver

    def refresh_until_exists(self, by: tuple, timeout: int = DEFAULT_TIMEOUT):
        # setup
        intervals = 1
        state = False

        # initial wait (fixed)
        sleep(1)

        # execute
        while not state and intervals < timeout:
            try:
                element = self.driver.find_element(by=by)
                state = element is not None
                if state:
                    break

                # refresh
                self.driver.refresh()

                # set
                self.logger.debug(f'waiting for element state')
                sleep(1)
                intervals = intervals + 1
            except Exception as e:
                state = False
                self.logger.debug(f'state not found [{e.args}]')

        # timeout
        if intervals >= timeout:
            raise TimeoutError("Refresh until element exists, timed out.")

    # private utilities
    def __get_enabled(self, by: tuple, timeout: int) -> WebElement:
        return (WebDriverWait(self.driver, timeout, ignored_exceptions)
                .until(ec.element_to_be_clickable(by)))

    def __get_exists(self, by: tuple, timeout: int) -> WebElement:
        return (WebDriverWait(self.driver, timeout, ignored_exceptions)
                .until(ec.presence_of_element_located(by)))
