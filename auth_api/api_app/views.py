from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import exceptions, serializers
from common.account.token import token_util
from common.vail import parsed_calibration_params
from utc_tools import get_utc


# Create your views here.

class TokenObtainPairIoTSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if not data.get("tenant", None):
            raise serializers.ValidationError(detail={"tenant": "This field is required."}, code="required")
        self.fields['tenant'] = serializers.CharField()
        super(TokenObtainPairIoTSerializer, self).__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['version'] = user.token_version
        token_util.upload_token(instance=user, token=str(token.access_token))
        return token

    def validate(self, attrs):
        try:
            data = {}
            authenticate_kwargs = {
                self.username_field: attrs[self.username_field],
                "password": attrs["password"],
                "tenant": attrs["tenant"]
            }
            self.user = authenticate(**authenticate_kwargs)
            refresh = self.get_token(self.user)

            data["access_token"] = str(refresh.access_token)
            data["refresh_token"] = str(refresh)
            data['user'] = self.user.user
            data["currentTime"] = int(refresh.current_time.timestamp())
            data['expireTime'] = refresh.payload['exp']
            data['tokenType'] = refresh.token_type

            if not api_settings.USER_AUTHENTICATION_RULE(self.user):
                raise exceptions.AuthenticationFailed(
                    self.error_messages["no_active_account"],
                    "no_active_account",
                )

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, self.user)
            return data

        except Exception as e:
            raise serializers.ValidationError(e)


class TokenObtainPairIoTView(TokenObtainPairView):
    serializer_class = TokenObtainPairIoTSerializer

    @parsed_calibration_params
    def post(self, request, *args, **kwargs):
        return super(TokenObtainPairIoTView, self).post(request, *args, **kwargs)
