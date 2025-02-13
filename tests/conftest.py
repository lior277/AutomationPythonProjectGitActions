import pytest
import os
import logging
from datetime import datetime
from typing import Generator
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener


class WebDriverListener(AbstractEventListener):
    """Custom WebDriver event listener for logging and screenshots."""

    def before_navigate_to(self, url, driver):
        logging.info(f"Navigating to {url}")

    def before_click(self, element, driver):
        logging.info(f"Clicking element {element.tag_name}")

    def on_exception(self, exception, driver):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(
            os.getenv('TEST_RESULTS_DIR', 'test-results'),
            'screenshots',
            f'error_{timestamp}.png'
        )
        driver.get_screenshot_as_file(screenshot_path)
        logging.error(f"Screenshot saved to {screenshot_path}")


def pytest_configure(config):
    """Configure test environment, directories, and logging."""
    results_dir = os.path.join(os.getcwd(), os.getenv('TEST_RESULTS_DIR', 'test-results'))
    for subdir in ['logs', 'screenshots', 'reports']:
        os.makedirs(os.path.join(results_dir, subdir), exist_ok=True)

    config.option.htmlpath = os.path.join(results_dir, 'reports/report.html')
    config.option.self_contained_html = True

    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    handlers = [
        (logging.INFO, 'execution.log'),
        (logging.DEBUG, 'debug.log'),
        (logging.ERROR, 'error.log')
    ]

    for level, filename in handlers:
        handler = logging.FileHandler(os.path.join(results_dir, 'logs', filename))
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(handler)

    logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture(scope='session', autouse=True)
def configure_grid():
    """Configure Selenium Grid settings for the test session."""
    from tests.test_suite_Base import TestSuiteBase
    TestSuiteBase.SELENIUM_GRID_URL = os.getenv('SELENIUM_GRID_URL', 'http://selenium-hub:4444/wd/hub')
    TestSuiteBase.RUN_LOCALLY = os.getenv('RUN_LOCALLY', 'false').lower() == 'true'


@pytest.fixture(scope='function')
def driver_fixture() -> Generator[WebDriver, None, None]:
    """Provide a WebDriver instance for each test function."""
    from tests.test_suite_Base import TestSuiteBase

    logging.info("Setting up WebDriver")
    driver = None

    try:
        base_driver = TestSuiteBase.get_driver()

        # Instead of maximize_window(), set specific window size
        base_driver.set_window_size(1920, 1080)

        driver = EventFiringWebDriver(base_driver, WebDriverListener())

        yield driver

    except Exception as e:
        logging.error(f"WebDriver setup failed: {str(e)}")
        if driver:
            try:
                screenshot_path = os.path.join(
                    os.getenv('TEST_RESULTS_DIR', 'test-results'),
                    'screenshots',
                    'setup_failure.png'
                )
                driver.get_screenshot_as_file(screenshot_path)
            except Exception:
                pass
        raise

    finally:
        if driver:
            logging.info("Cleaning up WebDriver")
            try:
                TestSuiteBase.driver_dispose(driver.wrapped_driver)
            except Exception as e:
                logging.error(f"Error during WebDriver cleanup: {str(e)}")


def pytest_sessionfinish(session, exitstatus):
    """Generate test session summary and clean up resources."""
    try:
        # Get test report statistics
        stats = session.config._reports if hasattr(session.config, '_reports') else {}
        passed = len([r for r in stats.get('passed', [])])
        failed = len([r for r in stats.get('failed', [])])
        skipped = len([r for r in stats.get('skipped', [])])
        total = session.testscollected if hasattr(session, 'testscollected') else 0

        # Log summary
        logging.info("Test Session Summary:")
        logging.info(f"Total tests: {total}")
        logging.info(f"Passed: {passed}")
        logging.info(f"Failed: {failed}")
        logging.info(f"Skipped: {skipped}")
        logging.info(f"Exit status: {exitstatus}")

    except Exception as e:
        logging.error(f"Error generating test summary: {str(e)}")

    finally:
        # Clean up logging handlers
        for handler in logging.getLogger().handlers[:]:
            try:
                handler.close()
                logging.getLogger().removeHandler(handler)
            except Exception as e:
                print(f"Error cleaning up logging handler: {str(e)}")