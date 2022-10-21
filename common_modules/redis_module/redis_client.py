import threading

import redis

from common_modules.redis_module.utility.redis_util import AbsRedis


class RedisClient(AbsRedis, object):

    def __init__(self, *args, **kwargs):
        super(RedisClient, self).__init__(*args, **kwargs)
        self.thread = None
        self._thread_id = None
        self.__connect()

    def __connect(self):
        self.client_obj = redis.StrictRedis(connection_pool=self.connect_obj, charset="utf8-mb4")
        return self.client_obj

    @property
    def client(self):
        if hasattr(self, "client_obj"):
            return self.client_obj
        else:
            return RuntimeError("client not connect success")

    _instance_lock = threading.Lock()


if __name__ == '__main__':
    r1 = RedisClient()
    r2 = RedisClient()
    r3 = RedisClient(db=1)
    print(id(r1), id(r2), id(r3))
