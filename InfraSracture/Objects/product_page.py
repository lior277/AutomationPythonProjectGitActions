import string
from InfraSracture.Infra.dal.api_accsess import ApiAccess
from InfraSracture.Objects.Dtos.post_add_to_chart_request import PostAddToChartRequest


class ProductPage:
    def __init__(self):
        pass

    def add_item_to_chart(self, url: string):
        post_add_to_chart = PostAddToChartRequest(
            id="9ce32f57-a86b-6fc6-945b-f47e1c3974e1",
            cookie="user=d5592657-a5d3-e061-f746-1e2a7595da7f",
            prod_id=1,
            flag=False)

        ApiAccess.execute_post_request(self, url, post_add_to_chart)
        return self
