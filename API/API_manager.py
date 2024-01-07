from json import JSONDecodeError

import requests


class APIError(Exception):
    pass


class APIresponse:
    """class for handling API response"""

    def _handle_response(self, api_response):
        """check the status of the request"""
        print(api_response.status_code)
        if api_response.status_code != 200:
            raise APIError
        try:
            json_response = api_response.json()
            return json_response
        except JSONDecodeError:
            raise APIError

    def get_problems(self, api_url):
        """ requests API url and returns the result via '_handle_response' """
        api_response = requests.get(api_url)
        return self._handle_response(api_response)
