import pytest

from InfraSracture.Infra.dal.container.dependency_container import Container
from InfraSracture.objects.data_classes.product_data import Product
from Tests.TestSuitBase import TestSuitBase


class TestCheckupProcess(TestSuitBase):
    container = Container()
    demo_blaze_url = "https://www.demoblaze.com/index.html"
    add_item_to_chart = "https://www.demoblaze.com/prod.html?idp_=1#"
    product_name = "Samsung galaxy s6"
    customer_name = "jones"
    customer_country = "israel"
    customer_city = "tel aviv"
    customer_credit = "1111"
    order_month = "11"
    order_year = "2023"
    driver = None
    home_page_ui = None
    product_page_ui = None
    upper_menu_ui = None
    chart_page_ui = None
    place_order_page_ui = None
    product_page_api = None
    signup_page_api = None

    @pytest.fixture(scope="function")
    def setup(self):
        def _setup(browser):
            self.driver = TestSuitBase.get_driver(self, browser_name=browser)
            self.container.driver.override(self.driver)
            self.home_page_ui = self.container.home_page_ui(driver=self.driver)
            self.product_page_ui = self.container.product_page_ui(driver=self.driver)
            self.upper_menu_ui = self.container.upper_menu_ui(driver=self.driver)
            self.chart_page_ui = self.container.chart_page_ui(driver=self.driver)
            self.place_order_page_ui = self.container.place_order_page_ui(driver=self.driver)
            self.product_page_api = self.container.product_page_api()
            self.signup_page_api = self.container.signup_page_api()
            self.driver.get(self.demo_blaze_url)

        yield _setup
        self.driver.close()
        self.driver.quit()

    @pytest.mark.xdist_group(name="group1")
    @pytest.mark.regression
    @pytest.mark.parametrize("browsers", ["chrome"])
    def test_checkup_process(self, setup, browsers):
        setup(browsers)

        actual_product = self.product_page_ui.get_product_by_title_from_mongodb("Nokia lumia 1520", "Products", Product)
        title = actual_product.title
        self.product_page_api.add_item_to_chart(self.add_item_to_chart)

        # click on shop new button
        self.home_page_ui.click_on_item_from_home_store(product_name=self.product_name)

        # click on add to chart button
        self.product_page_ui.click_on_add_to_chart_btn()

        # click on  chart menu item
        self.upper_menu_ui.click_on_chart_menu_item()

        # click on place order button
        self.chart_page_ui.click_on_place_order_btn()

        # fill place order form
        self.place_order_page_ui.place_order_pipe(
            self.customer_name,
            self.customer_country,
            self.customer_city,
            self.customer_credit,
            self.order_month,
            self.order_year)
