from django.conf import settings

from common.account.utils import account_utils
from common_modules.constant import TOKEN_EXPIRES_TIME, REDIS_TOKEN_KEY
from common_modules.utc_tools import get_utc
from middlewares.conn_client import ConnClient

redis_client = ConnClient().redis_client


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

    def upload_token(self, instance, token, expire=TOKEN_EXPIRES_TIME):
        # ttt -> tenant_token:token_value
        ttt = str(REDIS_TOKEN_KEY + token)
        redis_client.client.set(name=ttt, value=account_utils.get_account_key(instance), ex=expire)
        return True

    def get_token_version(self, instance):
        return instance.token_version


token_util = TokenUtil()
