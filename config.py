import logging
import os

from common.constants import DEFAULT_SERVICE_NAME, DEFAULT_CLIENT_URL


class Config:
    SERVICE_NAME = os.environ.get("SERVICE_NAME", DEFAULT_SERVICE_NAME)
    CACHE_TTL = os.environ.get("CACHE_TTL", 60)
    DEBUG = os.environ.get("DEBUG", True)
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
    CLIENT_URL = os.environ.get("CLIENT_URL", DEFAULT_CLIENT_URL)
    LOG_FORMAT = "%(asctime)s %(levelname)8s %(message)s "
    LOG_DATEFMT = "%Y-%m-%dT%H:%M:%S"
    LOG_LEVEL = logging.DEBUG
