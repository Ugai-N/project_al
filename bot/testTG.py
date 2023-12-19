import os
from json import JSONDecodeError
import aiohttp

TELEGRAM_URL = 'https://api.telegram.org/bot'


class TGClientError(Exception):
    pass


class TGClient:
    API_PATH = TELEGRAM_URL

    def __init__(self, token):
        self.token = token

    def get_base_path(self):
        return f'{self.API_PATH}{self.token}'

    async def _handle_response(self, resp):
        if resp.status != 200:
            raise TGClientError
        try:
            return await resp.json()
        except JSONDecodeError:
            raise TGClientError

    async def get_me(self) -> dict:
        url = self.get_base_path() + 'get_me'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await self._handle_response(resp)

    async def get_updates(self, offset, timeout) -> dict:
        url = self.get_base_path() + '/getUpdates'
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await self._handle_response(resp)

    async def send_message(self, chat_id, text):
        """отправки уведомления в телеграм"""
        url = self.get_base_path() + '/sendMessage'
        params = {}
        if chat_id:
            params['chat_id'] = chat_id
        if text:
            params['text'] = text
        async with aiohttp.ClientSession() as session:
            async with session.post(url, params=params) as resp:
                return await self._handle_response(resp)


