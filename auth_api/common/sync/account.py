from threading import Lock

from django.forms import model_to_dict

from common.forms import model_to_dict_uncheck_editable_attr
from common_modules.redis_module.redis_client import RedisClient
from constant import REDIS_ACCOUNT_LIST, REDIS_ACCOUNT_KEY

redis_client = RedisClient()


class SyncAccount:
    def __init__(self):
        self.lock = Lock()

    def create(self, obj):
        # 先根据版本
        account_info = model_to_dict_uncheck_editable_attr(obj)
        account = self.__get_account_key(obj)
        redis_name = REDIS_ACCOUNT_KEY + account
        redis_client.set_hmdict(redis_name, account_info)
        redis_client.client.sadd(REDIS_ACCOUNT_LIST, account)

    def delete(self, obj):
        pass

    def __get_account_key(self, obj):
        if hasattr(obj, "fk_tenant_id"):
            return "" + "" + ""

        else:
            return ""
