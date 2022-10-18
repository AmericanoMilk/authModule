from common_modules.redis_module.utility.redis_util import AbsRedis


class RedisClient(AbsRedis):
    def __init__(self, *args, **kwargs):
        super(RedisClient, self).__init__(*args, **kwargs)
        self.thread = None
        self._thread_id = None
