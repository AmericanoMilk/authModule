from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from user_app import models as user_models


class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = UntypedToken(attrs["token"])

        user_id = token.payload['user_id']
        user_obj = user_models.AuthUser.objects.get(id=user_id)
        if int(user_obj.token_version) != int(token.payload["version"]):
            raise ValidationError(detail="Token is invalid or expired", code='token_not_valid')

        if (
                api_settings.BLACKLIST_AFTER_ROTATION
                and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        return {}
