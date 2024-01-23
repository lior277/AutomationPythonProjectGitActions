import pytest

from InfraSracture.Infra.dal.container.dependency_container import Container
from InfraSracture.Infra.dal.mongo_db.mongo_db_access import MongoDbAccess
from InfraSracture.objects.data_classes.product_data import Product
from Tests.TestSuitBase import TestSuitBase


class TestCheckupProcessPlayWright(TestSuitBase):
    container = Container()
    demo_blaze_url = "www.demoblaze.com"
    add_item_to_chart = "https://www.demoblaze.com/prod.html?idp_=1#"
    product_name = "Samsung galaxy s6"
    customer_name = "jones"
    customer_country = "israel"
    customer_city = "tel aviv"
    customer_credit = "1111"
    order_month = "11"
    order_year = "2023"
    page = None;

    @pytest.fixture(scope="function")
    def setup(self, request):

        def _setup(browser):
            page = self.get_driver_playwright(browser_name=browser)
            page.goto(self.demo_blaze_url)

        yield _setup
        request.addfinalizer(self.driver_dispose(page=page))

    def tear_down(self):
        if hasattr(self, 'page'):
            self.page.close()

    @pytest.mark.xdist_group(name="group1")
    @pytest.mark.regression
    @pytest.mark.parametrize("browsers", ["chrome", "firefox"])
    @pytest.mark.asyncio
    async def test_checkup_process_playwright(self, setup, browsers):
        setup(browsers)
        home_page_ui = self.container.home_page_ui(driver=self.driver)
        product_page_ui = self.container.product_page_ui(driver=self.driver)
        upper_menu_ui = self.container.upper_menu_ui(driver=self.driver)
        chart_page_ui = self.container.chart_page_ui(driver=self.driver)
        place_order_page_ui = self.container.place_order_page_ui(driver=self.driver)
        product_page_api = self.container.product_page_api()
        signup_page_api = self.container.signup_page_api()
        signup_page_api.get_items("https://artlist.io/_next/data/F7ewnojrCY1FzxtJVYlwc/en/royalty-free-music.json")
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
