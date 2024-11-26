import string
from Infrastructure.Infra.dal.api_access.api_accsess import ApiAccess
from Infrastructure.objects.data_classes.post_add_to_chart_request import PostAddToChartRequest


class ProductPageApi:

    def __init__(self, api_access: ApiAccess):
        self.api_access = api_access

    def add_item_to_chart(self, url: string):
        post_add_to_chart = PostAddToChartRequest(
            id="9ce32f57-a86b-6fc6-945b-f47e1c3974e1",
            cookie="user=d5592657-a5d3-e061-f746-1e2a7595da7f",
            prod_id=1,
            flag=False)

        self.api_access.execute_post_request(self, url, post_add_to_chart)

        return self
