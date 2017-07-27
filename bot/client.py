import logging
from urllib.parse import urljoin

import aiohttp
import async_timeout

from config import config
from exceptions import BadHttpException


class BaseComponentClient:

    def __init__(self):
        self.log = logging.getLogger(__name__ + '.' + str(self.__class__))

    def make_url(self, path):
        return urljoin(config.URL, path)

    async def process_request(self, method, url, data=None, headers=None):
        request_url = self.make_url(url)

        with async_timeout.timeout(config.HTTP_TIMEOUT):
            async with aiohttp.ClientSession(headers=headers) as session:
                request_method = getattr(session, method)

                async with request_method(request_url, data=data) as response:
                    code = response.status
                    data = await response.json()

                    if 200 <= code < 300:
                        return data
                    else:
                        self.log.error('Http exception was occurred. Code {}. '
                                       'Response data: {}'.format(code, data))
                        raise BadHttpException


class Users(BaseComponentClient):
    URL_SUFFIX = '/users/'

    async def create_user(self, *args, **kwargs):
        user = await self.process_request(
            'post', self.URL_SUFFIX, *args, **kwargs
        )
        user['password'] = kwargs['data']['password']
        return user

    async def login(self, *args, **kwargs):
        return (
            await self.process_request('post', '/auth/login/', *args, **kwargs)
        )['token']


class Posts(BaseComponentClient):
    URL_SUFFIX = '/posts/'

    async def create_post(self, *args, **kwargs):
        return await self.process_request(
            'post', self.URL_SUFFIX, *args, **kwargs
        )

    async def like_post(self, pk, *args, **kwargs):
        return await self.process_request(
            'post', self.URL_SUFFIX + '{}/like/'.format(pk), *args, **kwargs
        )
