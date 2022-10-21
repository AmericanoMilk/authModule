import redis

from common_modules.config import config
from common_modules.redis_module.utility.redis_channel import RedisChannel
from common_modules.redis_module.utility.redis_dict import RedisDict
from common_modules.redis_module.utility.redis_list import RedisList
from common_modules.redis_module.utility.redis_str import RedisStr
from common_modules.redis_module.utility.redis_tools import RedisCommonTools

redis_conf = config.redis


class AbstractRedis(RedisList, RedisDict, RedisChannel, RedisStr, RedisCommonTools):
    pass


class AbsRedis(AbstractRedis):
    def __get_client_obj(self, host, db, password, port=6379, user=None, **kw) -> None:
        g_host = "host" + host
        g_host = g_host.replace(".", "d")
        if not hasattr(self, f"{g_host}_client_dict"):
            setattr(self, f"{g_host}_client_dict", {})

        getattr(self, f"{g_host}_client_dict").setdefault(str(db), {})

        self.connect_pool: dict = getattr(self, f"{g_host}_client_dict")

        db_client = self.connect_pool.get(db, None)
        if db_client:
            self.connect_obj = db_client
            return
        else:
            self.connect_obj = redis.ConnectionPool(
                host=host, port=port, password=password, db=db, decode_responses=True
            )
            self.connect_pool[db] = self.connect_pool
            return


    def __init__(
            self, db=0, *args, host=redis_conf.host, port=redis_conf.port, password=redis_conf.password, **kw
    ):
        self.connect_pool = dict()
        self.__get_client_obj(host=host, port=port, password=password, db=db, kw=kw)
