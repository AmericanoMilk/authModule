import redis

from common_modules.config import config
from redis_module.utility.redis_channel import RedisChannel
from redis_module.utility.redis_dict import RedisDict
from redis_module.utility.redis_list import RedisList
from redis_module.utility.redis_str import RedisStr
from redis_module.utility.redis_tools import RedisCommonTools

redis_conf = config["redis"]


class AbstractRedis(RedisList, RedisDict, RedisChannel, RedisStr, RedisCommonTools):
    pass


class AbsRedis(AbstractRedis):
    def __connect(self, host, db, password, port=6379, user=None, **kw):
        g_host = "host" + host
        g_host = g_host.replace(".", "d")
        if hasattr(self, f"{g_host}_client_dict"):
            if hasattr(hasattr(self, f"{g_host}_client_dict"), db):
                self.connect_pool = getattr(getattr(self, f"{g_host}_client_dict"), db)
            else:
                self.connect_pool = redis.ConnectionPool(
                    host=host, port=port, password=password, db=db, decode_responses=True
                )
                setattr(getattr(self, f"{g_host}_client_dict"), db, self.connect_pool)

        else:
            setattr(self, f"{g_host}_client_dict", {})
            self.connect_pool = redis.ConnectionPool(
                host=host, port=port, password=password, db=db, decode_responses=True
            )
            ghost_dict = getattr(self, f"{g_host}_client_dict")
            ghost_dict[db] = self.connect_pool
            # setattr(ghost_dict, str(db), self.connect_pool)

    def __init__(
            self, db=0, *args, host=redis_conf["host"], port=redis_conf["port"], password=redis_conf["password"], **kw
    ):
        self.__connect(host=host, port=port, password=password, db=db, kw=kw)

    @property
    def client(self):
        return redis.StrictRedis(connection_pool=self.connect_pool, charset="utf8-mb4")
