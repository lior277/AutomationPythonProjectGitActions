import pytest
import os
import logging
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver


def pytest_configure(config):
    """
    Configure pytest options and set up test environment.
    """
    # Create base test results directory
    results_dir = os.path.join(os.getcwd(), 'test-results')
    logs_dir = os.path.join(results_dir, 'logs')

    # Create all necessary directories
    for directory in [results_dir, logs_dir]:
        os.makedirs(directory, exist_ok=True)

    # Configure pytest-html report
    config.option.htmlpath = os.path.join(results_dir, 'report.html')
    config.option.self_contained_html = True

    # Create file handlers
    execution_handler = logging.FileHandler(os.path.join(logs_dir, 'pytest_execution.log'))
    execution_handler.setLevel(logging.INFO)

    debug_handler = logging.FileHandler(os.path.join(logs_dir, 'pytest_debug.log'))
    debug_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    execution_handler.setFormatter(formatter)
    debug_handler.setFormatter(formatter)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(execution_handler)
    root_logger.addHandler(debug_handler)
    root_logger.addHandler(logging.StreamHandler())  # Console output


@pytest.fixture(scope='session', autouse=True)
def configure_grid():
    """Configure Selenium Grid settings."""
    from tests.test_suite_Base import TestSuiteBase

    TestSuiteBase.SELENIUM_GRID_URL = os.getenv('SELENIUM_GRID_URL', 'http://selenium-hub:4444/wd/hub')
    TestSuiteBase.RUN_LOCALLY = os.getenv('RUN_LOCALLY', 'false').lower() == 'true'


@pytest.fixture(scope='function')
def driver_fixture() -> Generator[WebDriver, None, None]:
    """Provides a WebDriver instance for each test function."""
    from tests.test_suite_Base import TestSuiteBase

    logging.info("Setting up WebDriver for test...")
    driver = None

    try:
        driver = TestSuiteBase.get_driver()
        logging.info("WebDriver setup completed successfully")
        yield driver

    except Exception as e:
        logging.error(f"Error during WebDriver setup: {str(e)}")
        raise

    finally:
        if driver:
            logging.info("Cleaning up WebDriver...")
            TestSuiteBase.driver_dispose(driver)


def pytest_sessionfinish(session, exitstatus):
    """Cleanup after all tests are done."""
    logging.info(f"Test session completed with exit status: {exitstatus}")

    # Log test session summary
    passed = session.testscollected - session.testsfailed
    logging.info(f"Total tests: {session.testscollected}")
    logging.info(f"Passed: {passed}")
    logging.info(f"Failed: {session.testsfailed}")
    logging.info(f"Skipped: {len(session.skipped)}")

    # Close all handlers to prevent resource warnings
    for handler in logging.getLogger().handlers[:]:
        handler.close()
        logging.getLogger().removeHandler(handler)