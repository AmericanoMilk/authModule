from django.conf import settings

from common_modules.redis_module.redis_client import RedisClient
from common_modules.constant import TOKEN_EXPIRES_TIME
from common_modules.utc_tools import get_utc

redis_client = RedisClient()


class TokenUtil:
    def generate_token(
            self,
            instance,
            expire=TOKEN_EXPIRES_TIME,
    ):
        """
        在服务端设置加密的 key 时，为每个用户生成唯一的 key，失效则改变该 key。
        :param tenant_id:
        :param user_id:
        :param tenant:
        :param user:
        :param expire:
        :return:
        """
        version = self.get_token_version(instance=instance)
        token = settings.JWT_UTILS.encode(
            {
                "id": instance.uuid,
                "version": version,
                "time": get_utc()
            },
            expire=expire,
        )
        return token

    def upload_token(self, name, token, expire=TOKEN_EXPIRES_TIME):
        # ttt -> tenant_token:token_value
        ttt = str(REDIS_TOKEN_KEY + token)
        redis_client.client.set(name=ttt, value=name, ex=expire)
        return True

    def get_token_version(self, instance):
        return instance.version


token_util = TokenUtil()
