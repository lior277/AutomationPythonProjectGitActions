import pytest

from Infrastructure.objects.objects_api.product_page_api import ProductPageApi


class TestSecond:
    url = "https://www.demoblaze.com/prod.html?idp_=1#"

    @pytest.mark.sanity
    def test_add_to_chart(self):
        ProductPageApi.add_item_to_chart(self, TestSecond.url)
