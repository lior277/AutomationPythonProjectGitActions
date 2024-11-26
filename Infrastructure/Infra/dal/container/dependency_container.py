# container.py

from dependency_injector import containers, providers

from Infrastructure.Infra.dal.api_access.api_accsess import ApiAccess
from Infrastructure.objects.objects_api.product_page_api import ProductPageApi
from Infrastructure.objects.objects_api.signup_page_api import SignupPageApi
from Infrastructure.objects.objects_ui.chart_page_ui import ChartPageUi
from Infrastructure.objects.objects_ui.home_page_ui import HomePageUi
from Infrastructure.objects.objects_ui.place_order_form_ui import PlaceOrderPageUi
from Infrastructure.objects.objects_ui.product_page_ui import ProductPageUi
from Infrastructure.objects.objects_ui.upper_menu_ui import UpperMenuUi


class Container(containers.DeclarativeContainer):
    driver = providers.Object(lambda: None)
    home_page_ui = providers.Factory(HomePageUi, driver=driver)
    product_page_ui: providers.Factory = providers.Factory(ProductPageUi, driver=driver)
    chart_page_ui = providers.Factory(ChartPageUi, driver=driver)
    upper_menu_ui = providers.Factory(UpperMenuUi, driver=driver)
    place_order_page_ui = providers.Factory(PlaceOrderPageUi, driver=driver)
    api_access = providers.Factory(ApiAccess)
    product_page_api = providers.Factory(ProductPageApi, api_access=api_access)
    signup_page_api = providers.Factory(SignupPageApi, api_access=api_access)
