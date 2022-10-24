from dataclasses import asdict
from django.http import JsonResponse, HttpResponse, Http404
from django.utils.deprecation import MiddlewareMixin
import json

from common.response import Results
from common_modules.logger import logger


def record_log(request, response=None):
    """
    日志记录
    :param request:
    :param response:
    :return:
    """
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")

    method = request.method
    path = request.path
    args = json.dumps(request.GET) if request.GET else ""
    try:
        body = json.dumps(json.loads(request.body)) if request.body else ""
    except Exception as e:
        logger.exception(e)
        body = request.body
        # return True
    if response:
        if isinstance(response, Http404):
            content = ""
        else:
            try:
                content = json.dumps(json.loads(response.content))

            except Exception as e:
                pass
                content = response.content
        logger.info("process_response", ip, method, path, args, body, content)
    else:
        logger.info("process_request", ip, method, path, args, body)


class RecordMiddleware(MiddlewareMixin):
    def process_request(self, request):
        result = record_log(request)

        if result:
            results = Results()
            results.describe = "error data  " + str(request.body)
            results.code = 400
            return JsonResponse(asdict(results), status=results.code)

    def process_exception(self, request, exception):
        logger.exception(exception)
        return HttpResponse(exception, status=500)

    def process_response(self, request, response):
        result = record_log(request, response)
        # try:
        #     if response.status_code < 300:
        #         record_operation(request)
        # except Exception as e:
        #     logger.exception(e)
        # if result:
        #     results = Results()
        #     results.describe = 'error data  ' + str(request.body)
        #     results.code = REQUEST_ERROR_CODE
        #     return JsonResponse({}, status=results.code)
        # if response.status_code == 404:
        #     ret = {"code": 404, "msg": "", "result": None}
        #     notfound = JsonResponse(ret)
        #     notfound.headers = {"Content-Type": "application/json"}
        #     notfound.status_code = 404
        #     return notfound
        return response
