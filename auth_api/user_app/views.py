from django.shortcuts import render
from rest_framework.views import APIView

from common.generic.response import Response
from common.vail import parsed_calibration_params


# Create your views here.

class UserRegisterView(APIView):
    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        response = Response()
        tenant = request.tenant
        return response


class UserInfoView(APIView):
    @parsed_calibration_params
    def get(self, request, *args, **kwargs):
        response = Response()
        return response
