import string
import pytest
import self
from parameterized import parameterized_class
from InfraSracture.Infra.change_context import ChangeContext as ChangeContext
from Tests.TestSuitBase import TestSuitBase


class TestFirst(TestSuitBase):
    TestSuitBase.get_browser("chrome")

    luma_url = "https://magento.softwaretestingboard.com/what-is-new.html"

    @classmethod
    def setup_class(cls):
        cls.driver = cls.get_driver(self)
        cls.driver.get(TestFirst.luma_url)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.mark.xdist_group(name="group1")
    @pytest.mark.regression
    def test_negative_cases(self):

        # click on shop new button
        (ChangeContext(self.driver)
         .luma_home_page()
         .click_on_shop_new_yoga_btn())

        (ChangeContext(self.driver)
         .collection_page()
         .click_on_item_in_collection("Echo Fit Compression Short"))
