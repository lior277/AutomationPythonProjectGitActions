import pytest

from InfraSracture.Objects.ObjectsApi.product_page_api import ProductPage


class TestSecond:
    url = "https://www.demoblaze.com/prod.html?idp_=1#"

    @pytest.mark.sanity
    def test_add_to_chart(self):
        ProductPage.add_item_to_chart(self, TestSecond.url)
