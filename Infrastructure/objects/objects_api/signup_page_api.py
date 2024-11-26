import string
from Infrastructure.Infra.dal.api_access.api_accsess import ApiAccess
from Infrastructure.objects.data_classes.post_signup_request import PostSignupRequest


class SignupPageApi:

    def __init__(self, api_access: ApiAccess):
        self.api_access = api_access

    def get_items(self, url: string):
        self.api_access.execute_get_request(self, url)
        return self
