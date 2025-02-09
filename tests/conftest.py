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
    screenshots_dir = os.path.join(results_dir, 'screenshots')

    # Create all necessary directories
    for directory in [results_dir, logs_dir, screenshots_dir]:
        os.makedirs(directory, exist_ok=True)

    # Configure pytest-html report
    config.option.htmlpath = os.path.join(results_dir, 'report.html')
    config.option.self_contained_html = True

    # Set up logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(logs_dir, 'pytest_execution.log')),
            logging.FileHandler(os.path.join(logs_dir, 'pytest_debug.log'), level=logging.DEBUG)
        ]
    )


@pytest.fixture(scope='session', autouse=True)
def configure_grid():
    """
    Configure Selenium Grid settings from environment variables.
    """
    from tests.test_suite_Base import TestSuiteBase

    grid_url = os.getenv('SELENIUM_GRID_URL', 'http://selenium-hub:4444/wd/hub')
    run_locally = os.getenv('RUN_LOCALLY', 'false').lower() == 'true'

    TestSuiteBase.SELENIUM_GRID_URL = grid_url
    TestSuiteBase.RUN_LOCALLY = run_locally

    logging.info(f"Configured TestSuiteBase with GRID_URL: {grid_url}, RUN_LOCALLY: {run_locally}")


@pytest.fixture(scope='function')
def driver_fixture() -> Generator[WebDriver, None, None]:
    """
    Provides a WebDriver instance for each test function.
    Handles setup and teardown of the WebDriver.
    """
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


@pytest.fixture(autouse=True)
def test_logger(request):
    """
    Provides logging for each test case execution.
    """
    logging.info(f"Starting test: {request.node.name}")
    yield
    logging.info(f"Finished test: {request.node.name}")


def pytest_exception_interact(node, call, report):
    """
    Handles test failures by capturing screenshots and logging additional information.
    """
    if report.failed:
        from tests.test_suite_Base import TestSuiteBase

        try:
            driver = node.funcargs.get('driver_fixture')
            if driver:
                screenshot_dir = os.path.join('test-results', 'screenshots')
                screenshot_path = os.path.join(screenshot_dir, f"failure_{node.name}.png")

                driver.save_screenshot(screenshot_path)
                logging.error(f"Test failed: {node.name}")
                logging.error(f"Screenshot saved: {screenshot_path}")

                # Log additional browser information
                logging.error(f"Current URL: {driver.current_url}")
                logging.error(f"Page title: {driver.title}")

        except Exception as e:
            logging.error(f"Failed to capture failure information: {str(e)}")


def pytest_sessionfinish(session, exitstatus):
    """
    Performs cleanup and logging at the end of the test session.
    """
    logging.info(f"Test session completed with exit status: {exitstatus}")

    # Log test session summary
    passed = session.testscollected - session.testsfailed
    logging.info(f"Total tests: {session.testscollected}")
    logging.info(f"Passed: {passed}")
    logging.info(f"Failed: {session.testsfailed}")
    logging.info(f"Skipped: {len(session.skipped)}")