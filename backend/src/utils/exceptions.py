from rest_framework.exceptions import APIException as _APIException


class APIException(_APIException):

    def __init__(self, status: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status_code = status
