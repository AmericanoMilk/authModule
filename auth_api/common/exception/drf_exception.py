from dataclasses import asdict
from django.http import JsonResponse
from common.response import get_error_response
from common_modules.logger import logger


def response_exception_handler(exc, context):
    if exc:
        logger.debug("校验错误", exc, context)
        response, status = get_error_response(exception=exc)
        return JsonResponse(data=asdict(response), status=status)
