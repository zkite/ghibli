from config import Config
import logging
from pythonjsonlogger import jsonlogger


def get_logger(name):
    log = logging.getLogger(name)
    if not log.handlers:
        handler = logging.StreamHandler()
        log_level = Config.LOG_LEVEL
        log_format = Config.LOG_FORMAT
        handler.setFormatter(jsonlogger.JsonFormatter(log_format))
        handler.setLevel(log_level)
        log.addHandler(handler)
        log.setLevel(log_level)

    def _pass():
        pass

    log.close_on_exec = _pass

    return log


class LoggerWrapper:
    def __getattr__(self, item):
        log = get_logger(__name__)
        if hasattr(log, item):
            return getattr(log, item)
        else:
            raise AttributeError("Logger doesn't have attribute {}".format(item))


logger = LoggerWrapper()
