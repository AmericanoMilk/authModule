from rest_framework_simplejwt.authentication import JWTAuthentication

from redis_module.redis_client import RedisClient

redis_client = RedisClient()


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

        return self.get_user(validated_token), validated_token
