from threading import Thread

import redis
import json

from common_modules.logger import logger


class RedisChannel:
    client: redis.Redis

    def subscribe(self, channel):
        # 订阅
        pub = self.client.pubsub()
        pub.subscribe(channel)
        pub.parse_response()
        return pub

    def publish(self, channel, message):
        # 发布
        if isinstance(message, dict):
            message = json.dumps(message)
        elif isinstance(message, list):
            message = json.dumps(message)
        self.client.publish(channel, message)

    def _sub(self, channel, call_back):
        meaaag = self.subscribe(channel)
        while True:
            meaaage = meaaag.parse_response()
            call_back(meaaage)

    def listen(self, chanel, call_back):
        if not self.thread:
            self.thread = Thread(
                target=self._sub,
                name=chanel,
                args=(
                    chanel,
                    call_back,
                ),
                daemon=True,
            )
            self.thread.start()
            self._thread_id = self.thread.ident
        else:
            raise ValueError("instance already exists thread ")

    def unsubscribe(self):
        if hasattr(self, "thread"):
            try:
                self._async_raise(self._thread_id, SystemExit)
            except Exception as e:
                logger.info("redis sub kill thread error", str(e))
        else:
            raise ValueError("Cancel an unsubscribed instance")
