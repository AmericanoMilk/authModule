import redis


class RedisStr:
    client: redis.Redis

    def pull(self, name):
        return self.client.get(name)



    def push_str(self, key, msg):
        self.client.set(key, msg)
