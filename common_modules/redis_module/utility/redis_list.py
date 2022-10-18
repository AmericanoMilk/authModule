from redis.client import Redis


class RedisList:
    client: Redis

    def append(self):
        raise AttributeError("method not implemented")
        pass

    def header_append(self):
        # self.client.lpush()
        raise AttributeError("method not implemented")
        pass
