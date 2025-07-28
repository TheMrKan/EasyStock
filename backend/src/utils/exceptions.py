from rest_framework.exceptions import APIException as _APIException
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and hasattr(exc, 'get_full_details'):
        response.data = exc.get_full_details()
    return response


class APIException(_APIException):

    def __init__(self, status: int, message: str, code: str):
        super().__init__(detail=message, code=code)
        self.status_code = status


class DomainError(Exception):
    message: str
    code: str

    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
