from sanic.exceptions import SanicException


class ApplicationError(SanicException):
    pass


class CacheError(ApplicationError):
    pass


class UnexpectedResponseException(ApplicationError):
    pass


class ClientNotFound(ApplicationError):
    pass
