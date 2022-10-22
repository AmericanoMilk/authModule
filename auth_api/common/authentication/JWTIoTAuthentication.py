from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from tenant_app.models import Tenant as tenant_model


class JWTIoTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token: bytes = self.get_raw_token(header)
        if raw_token is None:
            return None

        str_token = raw_token.decode("utf8")

        validated_token = self.get_validated_token(raw_token)
        payload = validated_token.payload
        instanceType = payload.get("instanceType")
        if not instanceType:
            return None

        if instanceType == "tenant":
            tenant = self.get_tenant(validated_token)
            request.tenant = tenant
            request.user = AnonymousUser()
            return tenant, validated_token
        else:
            user = self.get_user(validated_token)
            request.tenant = None
            request.user = user
            return user, validated_token

    def get_tenant(self, validated_token):
        try:
            tenant_id = validated_token.payload.get("id")
        except Exception as e:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            tenant = tenant_model.objects.get(uuid=tenant_id)
        except tenant_model:
            raise AuthenticationFailed(_("Tenant not found"), code="user_not_found")

        if not tenant.is_active:
            raise AuthenticationFailed(_("Tenant is inactive"), code="user_inactive")

        return tenant
