import pytest
from tests import test_suit_Base  # Assuming TestSuitBase is in this module

@pytest.fixture(scope='function')
def setup_and_teardown(request):
    # Setup code here (run before each test)
    print("Setup: This will run before each test")
    driver = test_suit_Base.TestSuitBase.get_driver()
    driver.maximize_window()
    yield driver
    print("Teardown: This will run after each test")

    if driver:
        test_suit_Base.TestSuitBase.driver_dispose(driver=driver)
