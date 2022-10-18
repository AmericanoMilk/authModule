from django.conf import settings

from common.account.utils import account_utils
from common_modules.redis_module.redis_client import RedisClient
from common_modules.constant import TOKEN_EXPIRES_TIME, REDIS_TOKEN_KEY
from common_modules.utc_tools import get_utc

redis_client = RedisClient()


class TokenUtil:
    def upload_token(self, instance, token, expire=TOKEN_EXPIRES_TIME):
        # ttt -> tenant_token:token_value
        ttt = str(REDIS_TOKEN_KEY + token)
        redis_client.client.set(name=ttt, value=account_utils.get_account_key(instance), ex=expire)
        return True

    def get_token_version(self, instance):
        return instance.version


token_util = TokenUtil()
