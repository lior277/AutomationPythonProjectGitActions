import pytest

from tests.test_suit_Base import TestSuitBase  # Assuming TestSuitBase is in this module


@pytest.fixture(scope='function')
def driver_fixture():
    """
    Fixture for setting up and tearing down the WebDriver instance.
    Provides a WebDriver instance to the test and ensures cleanup after the test.
    """
    print("Setup: Initializing WebDriver instance.")
    driver = TestSuitBase.get_driver()

    yield driver  # This provides the WebDriver instance to the test.

    print("Teardown: Cleaning up WebDriver instance.")
    TestSuitBase.driver_dispose(driver=driver)
