import json
from datetime import datetime

from redis import Redis



class RedisDict:
    client: Redis

    def hdelete(self, name, *key):
        return self.client.hdel(name, *key)

    def set_hash(self, name, key, value) -> None:
        self.client.hset(name=name, key=key, value=value)

    def get_hash(self, name, key):
        return self.client.hget(name=name, key=key)

    def get_all_hash(self, name):
        return self.client.hgetall(name=name)

    def set_hmdict(self, name, body: dict):
        for k, v in body.items():
            if isinstance(v, datetime):
                body[k] = datetime_to_str(v)
            elif isinstance(v, bool):
                body[k] = "true" if v else "false"
            elif isinstance(v, dict) or isinstance(v, list):
                body[k] = json.dumps(v)
            elif v is None:
                body[k] = ""
        self.client.hmset(name, body)
