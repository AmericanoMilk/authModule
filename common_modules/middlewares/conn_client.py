from common_modules.redis_module.redis_client import RedisClient


class ConnClient:
    __instance = None
    _redis_client = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    @property
    def redis_client(self):
        if not self._redis_client:
            self._redis_client = RedisClient()
        return self._redis_client


if __name__ == '__main__':
    pass