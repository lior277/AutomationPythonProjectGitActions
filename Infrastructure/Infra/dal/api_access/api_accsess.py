import dataclasses
import string
import requests


class ApiAccess:

    @staticmethod
    def execute_get_request(self, url: string) -> string:
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"error code is {response.status}")
        return response

    @staticmethod
    def execute_post_request(self, url: string, body: object):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        body_dict = dataclasses.asdict(body)
        response = requests.post(url, json=body_dict, headers=headers)
        if response.status_code != 200:
            raise Exception(f"error code is {response.status}")

