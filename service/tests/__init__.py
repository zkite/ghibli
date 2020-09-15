import ujson
import os

from asynctest import CoroutineMock, MagicMock, TestCase
from service.app import app


def CM(mock):
    return CoroutineMock(return_value=mock)


def get_file_path(fixture_file_name):
    return os.path.join(os.path.join(os.path.dirname(__file__), "fixtures"), fixture_file_name)


def from_json(file):
    with open(file) as json_file:
        return ujson.load(json_file)


class BaseTestCase(TestCase):
    @staticmethod
    def redis_mock(cached_data=None):
        redis_mock = MagicMock()
        redis_mock.retrieve_cached_data = CoroutineMock(return_value=cached_data)
        redis_mock.cache_data = CoroutineMock()
        return redis_mock

    @property
    def app(self):
        return app
