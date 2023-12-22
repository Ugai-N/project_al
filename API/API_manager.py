from json import JSONDecodeError

import aiohttp
import requests

from db.models import Problem


class APIError(Exception):
    pass


class APIresponse:
    """   """
    # def check_connection(self) -> int:
    #     """функция для проверки статус-кода при работе с API"""
    #     response = requests.get('https://codeforces.com/api/problemset.problems?tags=implementation')
    #     print(response.status_code)
    #     return response.status_code

    def _handle_response(self, api_response):
        print(api_response.status_code)
        if api_response.status_code != 200:
            raise APIError
        try:
            json_response = api_response.json()
            # print(type(json_response))
            # print(json_response['status'])
            # print(json_response['result']['problems'][110])
            # print(json_response['result']['problemStatistics'][110])
            # return api_response.json()
            return Problem.problem_init_handler(json_response)
        except JSONDecodeError:
            raise APIError

    # def get_problems(self) -> list:
    #     """обращается к API и выгружает список вакансии согласно запросу search_query"""
    #     data = []
    #     raw_data = requests.get('https://codeforces.com/api/problemset.problems?tags=implementation').json()
    #     print(type(raw_data))
    #     print(raw_data['status'])
    #     print(raw_data['result']['problems'][110])
    #     print(raw_data['result']['problemStatistics'][110])
    #     # data.extend(raw_data['items'])
    #    return data

    def get_problems(self, api_url):
        """обращается к API и проводит результат запроса через обработчик _handle_response"""
        api_response = requests.get(api_url)
        return self._handle_response(api_response)




