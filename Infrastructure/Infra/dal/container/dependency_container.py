from selenium import webdriver

from injector import singleton, Binder, Module

from Infrastructure.Infra.dal.api_access.api_accsess import ApiAccess
from Infrastructure.objects.objects_api.product_page_api import ProductPageApi
from Infrastructure.objects.objects_api.signup_page_api import SignupPageApi
from Infrastructure.objects.objects_ui.chart_page_ui import ChartPageUi
from Infrastructure.objects.objects_ui.home_page_ui import HomePageUi
from Infrastructure.objects.objects_ui.place_order_form_ui import PlaceOrderPageUi
from Infrastructure.objects.objects_ui.product_page_ui import ProductPageUi
from Infrastructure.objects.objects_ui.upper_menu_ui import UpperMenuUi
from tests.test_suit_Base import TestSuitBase


class AppModule(Module):  # Inherit from Module
    """Module for binding dependencies."""

    def configure(self, binder: Binder):
        # Bind WebDriver as a singleton, leveraging TestSuitBase.get_driver
        binder.bind(
            webdriver.Chrome,
            to=lambda: TestSuitBase.get_driver("chrome"),
            scope=singleton
        )

        # Bind other components as singletons or as needed
        binder.bind(ApiAccess, to=ApiAccess, scope=singleton)
        binder.bind(HomePageUi, to=HomePageUi, scope=singleton)
        binder.bind(ProductPageUi, to=ProductPageUi, scope=singleton)
        binder.bind(ChartPageUi, to=ChartPageUi, scope=singleton)
        binder.bind(UpperMenuUi, to=UpperMenuUi, scope=singleton)
        binder.bind(PlaceOrderPageUi, to=PlaceOrderPageUi, scope=singleton)
        binder.bind(ProductPageApi, to=ProductPageApi, scope=singleton)
        binder.bind(SignupPageApi, to=SignupPageApi, scope=singleton)
