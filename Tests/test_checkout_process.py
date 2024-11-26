from typing import Any, List

import pytest

from Infrastructure.Infra.dal.container.dependency_container import Container
from Infrastructure.Infra.dal.mongo_db.mongo_db_access import MongoDbAccess
from Infrastructure.objects.data_classes.product_data import Product
from Tests.TestSuitBase import TestSuitBase


class TestCheckupProcess(TestSuitBase):
    driver = None
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

    @pytest.fixture(scope="function")
    def setup(self):

        def _setup(browser):
            self.driver = TestSuitBase.get_driver(browser_name=browser)
            # self.container.driver.override(self.driver)
            self.driver.get(self.demo_blaze_url)

        yield _setup
        self.driver.close()
        self.driver.quit()

    @pytest.mark.xdist_group(name="group1")
    @pytest.mark.regression
    @pytest.mark.parametrize("browsers", ["chrome"])
    def test_checkup_process(self, setup, browsers):
        setup(browsers)
        home_page_ui = self.container.home_page_ui(driver=self.driver)
        product_page_ui = self.container.product_page_ui(driver=self.driver)
        upper_menu_ui = self.container.upper_menu_ui(driver=self.driver)
        chart_page_ui = self.container.chart_page_ui(driver=self.driver)
        place_order_page_ui = self.container.place_order_page_ui(driver=self.driver)
        product_page_api = self.container.product_page_api()
        signup_page_api = self.container.signup_page_api()

        actual_products = (MongoDbAccess.select_all_documents_from_table_as_class(table_name="Products", T=Product))
        actual_product = next((product for product in actual_products if product.title == self.product_name))

        product_page_api.add_item_to_chart(self.add_item_to_chart)

        # click on shop new button
        home_page_ui.click_on_item_from_home_store(product_name=self.product_name)

        # click on add to chart button
        product_page_ui.click_on_add_to_chart_btn()

        # click on  chart menu item
        upper_menu_ui.click_on_chart_menu_item()

        # click on place order button
        chart_page_ui.click_on_place_order_btn()

        # fill place order form
        place_order_page_ui.place_order_pipe(
            self.customer_name,
            self.customer_country,
            self.customer_city,
            self.customer_credit,
            self.order_month,
            self.order_year)
