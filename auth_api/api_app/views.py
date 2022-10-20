from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase, TokenVerifyView

from api_app.serializer import TokenObtainPairIoTSerializer, TokenRefreshIoTSerializer
from common.generic.response import Response
from common.vail import parsed_calibration_params


# Create your views here.


class TokenObtainPairIoTView(TokenObtainPairView):
    serializer_class = TokenObtainPairIoTSerializer

    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        return super(TokenObtainPairIoTView, self).post(request, *args, **kwargs)


class TokenRefreshIoTView(TokenViewBase):
    serializer_class = TokenRefreshIoTSerializer

    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        return super(TokenRefreshIoTView, self).post(request, *args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class


class TokenVerifyIoTView(TokenVerifyView):

    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        r = super(TokenVerifyIoTView, self).post(request, *args, **kwargs)
        if r.status_code == 200:
            return Response()
        return r
