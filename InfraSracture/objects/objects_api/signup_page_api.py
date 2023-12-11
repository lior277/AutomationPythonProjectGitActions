import string
from InfraSracture.Infra.dal.api_accsess import ApiAccess
from InfraSracture.objects.data_classes.post_signup_request import PostSignupRequest


class SignupPageApi:

    def __init__(self, api_access: ApiAccess):
        self.api_access = api_access

    def add_item_to_chart(self, url: string):
        post_signup = PostSignupRequest(
            username="lior277",
            password="TGlvcmg5NjM=")

        self.api_access.execute_post_request(self, url, post_signup)
        return self
