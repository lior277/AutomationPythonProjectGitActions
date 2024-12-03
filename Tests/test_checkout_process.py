import pytest
from injector import Injector

from Infrastructure.Infra.dal.mongo_db.mongo_db_access import MongoDbAccess
from Infrastructure.objects.data_classes.product_data import Product
from Infrastructure.objects.objects_api.product_page_api import ProductPageApi
from Infrastructure.objects.objects_ui.chart_page_ui import ChartPageUi
from Infrastructure.objects.objects_ui.home_page_ui import HomePageUi
from Infrastructure.objects.objects_ui.place_order_form_ui import PlaceOrderPageUi
from Infrastructure.objects.objects_ui.product_page_ui import ProductPageUi
from Infrastructure.objects.objects_ui.upper_menu_ui import UpperMenuUi
from Tests import TestSuitBase


class TestCheckupProcess:
    """Integration test for end-to-end checkup process."""

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
        """Setup and teardown for browser driver."""
        def _setup(browser):
            self.driver = TestSuitBase.get_driver(browser_name=browser)
            self.driver.get(self.demo_blaze_url)

        yield _setup
        if self.driver:
            self.driver.close()
            self.driver.quit()

    @pytest.mark.skip
    @pytest.mark.parametrize("browsers", ["chrome"])
    @pytest.mark.regression
    def test_checkup_process(self, setup, browsers, injector: Injector):
        """Main test method for checkup process."""
        # Setup the browser
        setup(browsers)

        # Inject dependencies
        home_page_ui = injector.get(HomePageUi)
        product_page_ui = injector.get(ProductPageUi)
        upper_menu_ui = injector.get(UpperMenuUi)
        chart_page_ui = injector.get(ChartPageUi)
        place_order_page_ui = injector.get(PlaceOrderPageUi)
        product_page_api = injector.get(ProductPageApi)
        mongo_db_access = injector.get(MongoDbAccess)

        # Validate database records
        actual_products = mongo_db_access.select_all_documents_from_table_as_class(table_name="Products", T=Product)
        assert actual_products, "No products found in the database"
        actual_product = next((product for product in actual_products if product.title == self.product_name), None)
        assert actual_product, f"Product '{self.product_name}' not found in the database"

        # Perform API call
        response = product_page_api.add_item_to_chart(self.add_item_to_chart)
        assert response.status_code == 200, f"API call failed with status: {response.status_code}"

        # Perform UI interactions
        home_page_ui.click_on_item_from_home_store(product_name=self.product_name)
        product_page_ui.click_on_add_to_chart_btn()
        upper_menu_ui.click_on_chart_menu_item()
        chart_page_ui.click_on_place_order_btn()

        place_order_page_ui.place_order_pipe(
            self.customer_name,
            self.customer_country,
            self.customer_city,
            self.customer_credit,
            self.order_month,
            self.order_year
        )