import asyncio

from urllib.parse import urlencode, urljoin

import aiohttp
import ujson

from common.exceptions import ClientNotFound, CacheError, UnexpectedResponseException
from common.logger import logger
from config import Config


class ClientRegistry:
    _clients = {}
    _active = {}

    @classmethod
    def register(cls, name, rest_cls) -> None:
        cls._clients[name] = rest_cls

    @classmethod
    def get(cls, name: str):
        if name not in cls._active:
            raise ClientNotFound(f"Client {name} not found in active clients")
        return cls._active.get(name)

    @classmethod
    def get_cached(cls, name: str):
        name = f"cached_{name}"
        if name not in cls._active:
            raise ClientNotFound(f"Client {name} not found in active clients")
        return cls._active.get(name)

    @classmethod
    def init(cls, cache_manager=None) -> None:
        for name, client_cls in cls._clients.items():
            if issubclass(client_cls, CachedClient) and cache_manager:
                cls._active[f"cached_{name}"] = client_cls(cache_manager=cache_manager)
            cls._active[name] = client_cls()


class BaseApiClient:
    REQUEST_TIMEOUT = 0
    client_url = Config.CLIENT_URL

    # TODO: retry
    async def make_http_request(self, request_method, url, headers=None, data=None):
        data = data if data else {}
        headers = headers if headers else {}

        request_url = urljoin(self.client_url, url)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=request_method, url=request_url, data=data, headers=headers, timeout=self.REQUEST_TIMEOUT
            ) as response:
                try:
                    request_json = await response.json()
                except aiohttp.client_exceptions.ContentTypeError:
                    return response.content, response.status

                try:
                    data = request_json["data"]
                    return data, response.status
                except (KeyError, TypeError):
                    return request_json, response.status

    async def get(self, path, headers=None, **args):
        params = urlencode(args, True)
        url = f"{path}?{params}" if params else f"{path}"
        data, status_code = await self.make_http_request("GET", url=url, headers=headers)
        return data, status_code


class CachedClient(BaseApiClient):
    name = "base"

    def __init__(self, cache_manager=None, number_of_retries=3, retry_sleep_time=1):
        self.cache_manager = cache_manager
        self.number_of_retries = number_of_retries
        self.retry_sleep_time = retry_sleep_time

    async def check_cache(self, **kwargs):
        try:
            if not self.cache_manager:
                logger.debug(f"No cache manager specified for the client. {self.name}")
                return
            return await self.cache_manager.retrieve_cached_data(**kwargs)
        except AttributeError as e:
            logger.debug(e)
        except CacheError as e:
            logger.error(f"Cache error {e}")

    async def cache_response(self, cache_ttl, **kwargs):
        try:
            if not self.cache_manager:
                logger.debug(f"No cache manager specified for the client. {self.name}")
                return
            await self.cache_manager.cache_data(cache_ttl, **kwargs)
        except AttributeError as e:
            logger.debug(e)
        except CacheError as e:
            logger.error(f"Cache error {e}")

    async def get(self, path, headers=None, cache_ttl=Config.CACHE_TTL, **args):
        headers = headers if headers else {}
        params = urlencode(args, True)

        cached_data = await self.check_cache(url=path, params=params, headers=headers)
        if cached_data:
            return ujson.loads(cached_data.decode("utf8"))

        url = "{path}?{params}".format(path=path, params=params) if params else "{path}".format(path=path)

        data = None
        for _ in range(self.number_of_retries):
            data, status_code = await self.make_http_request("GET", url=url, headers=headers)
            if status_code == 200:
                logger.debug(f"Successfully retrieved data: {data}")
                break
            logger.debug(f"Could not retrieve data. Response status code: {status_code}")
            await asyncio.sleep(self.retry_sleep_time)
        else:
            logger.warning(f"Could not retrieve data from {self.name}. Response status code: {status_code}")
            raise UnexpectedResponseException(data, status_code)

        if data:
            await self.cache_response(cache_ttl, url=path, params=params, headers=headers, data=ujson.dumps(data))

        return data
