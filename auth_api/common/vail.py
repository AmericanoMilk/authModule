from dataclasses import asdict
from functools import wraps

from django.http import JsonResponse

from common.response import get_error_response


def parsed_calibration_params(decorator):
    @wraps(decorator)
    def wrapper(*args, **kwargs):
        try:
            response = decorator(*args, **kwargs)
            status = 200
        except Exception as e:
            response, status = get_error_response(exception=e)
        return JsonResponse(data=asdict(response), status=status)

    return wrapper
