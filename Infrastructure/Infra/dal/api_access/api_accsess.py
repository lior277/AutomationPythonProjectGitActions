import dataclasses
import requests

class ApiAccess:
    @staticmethod
    def execute_get_request(url: str) -> str:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Error: Received status code {response.status_code} for GET request to {url}")

        return response.text

    @staticmethod
    def execute_post_request(url: str, body: object) -> dict:
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # Serialize the dataclass instance into a dictionary
        try:
            body_dict = dataclasses.asdict(body)

        except TypeError:
            raise ValueError("The body must be a dataclass instance")

        response = requests.post(url, json=body_dict, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error: Received status code {response.status_code} for POST request to {url}")

        try:
            return response.json()
        except requests.JSONDecodeError:
            # Handle non-JSON responses gracefully
            print("Warning: Response is not in JSON format")

            return response.text
