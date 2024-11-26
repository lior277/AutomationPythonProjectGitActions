import string
from typing import TypeVar

from selenium.webdriver.common.by import By

from Infrastructure.Infra.dal.mongo_db.mongo_db_access import MongoDbAccess
from Infrastructure.Infra.dal.web_driver_extention.web_driver_extension import DriverEX
from Infrastructure.objects.data_classes.product_data import Product


class ProductPageUi:
    T = TypeVar('T')

    def __init__(self, driver):
        self.driver = driver

        # locators
        self.add_to_chart_btn = By.CSS_SELECTOR, "a[onclick*='addToCart']"

    def click_on_add_to_chart_btn(self):
        DriverEX.force_click(self.driver, self.add_to_chart_btn)
        return self

    def get_product_by_title_from_mongodb(self, product_title: string, table_name: string) -> Product:
        self.all_product = MongoDbAccess.select_all_documents_from_table_as_class(table_name=table_name)
        return next(filter(lambda x: x.title == product_title, self.all_product), None)
