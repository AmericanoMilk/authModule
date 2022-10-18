from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

import backends.backends
from common.account.token import token_util
from common.account.utils import account_utils


# Create your views here.

class TokenObtainPairIoTSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['version'] = user.token_version
        token_util.upload_token(instance=user, token=token)
        return token

    def validate(self, attrs):
        try:
            pass
        except Exception:
            pass
        finally:
            return super().validate(attrs=attrs)


class TokenObtainPairIoTView(TokenObtainPairView):
    serializer_class = TokenObtainPairIoTSerializer
    # permission_classes = [backends.backends.RBACRbacBackends]
