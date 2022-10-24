import json

from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request


class AuthInterceptorMiddleware(MiddlewareMixin):
    def process_response(self, request: Request, response):
        if isinstance(request.user, AnonymousUser):
            return HttpResponse(json.dumps(dict(code=401, msg="invalid token", data={})),
                                content_type="application/json")
        return response
