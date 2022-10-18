import json
from dataclasses import field, dataclass

from django.http import JsonResponse
from rest_framework.response import Response


@dataclass()
class Results:
    code: int = 200
    msg: str = ""
    data: dict = field(default_factory=dict)

    def to_dict(self):
        return self.__dict__


@dataclass
class PageTypeResults:
    page: int = 1
    size: int = 1
    totalPage: int = 1
    result: list = field(default_factory=list)


def get_error_response(exception):
    code = 400
    response = Results(code=code, msg=str(exception))
    return response, code
