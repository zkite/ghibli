import ujson
from asynctest import patch

from common.client_registry import CachedClient
from service.tests import BaseTestCase, from_json, get_file_path


class TestClient(BaseTestCase):
    @patch("common.client_registry.BaseApiClient.make_http_request")
    def test_client_success(self, http_request_mock, *args):
        return_value = from_json(get_file_path("films.json"))
        http_request_mock.return_value = (return_value, 200)
        redis_mock = self.redis_mock()
        client = CachedClient(redis_mock)
        response = self.loop.run_until_complete(client.get("films"))
        self.assertTrue(response)
        redis_mock.retrieve_cached_data.assert_called_once_with(url="films", params="", headers={})
        http_request_mock.assert_called_once_with("GET", headers={}, url="films")
        redis_mock.cache_data.assert_called_once_with(
            60, url="films", params="", headers={}, data=ujson.dumps(return_value)
        )
