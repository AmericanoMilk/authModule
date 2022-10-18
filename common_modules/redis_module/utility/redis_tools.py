from redis.client import Redis

from common_modules.loggers import logger
import ctypes
import inspect
import json


from common_modules.loggers import logger


class RedisCommonTools:
    client: Redis

    def get_all_members(self, key):
        # 无视对象类型 todo待实现
        key_type = self.client.type(key)
        pass

    def set_expire(self, key, seconds):
        try:
            self.client.expire(key, seconds)
        except Exception as Err:
            logger.error("set redis expire error", str(Err))

    def exists(self, key):
        return self.client.exists(key)

    def delete(self, key):
        self.client.delete(key)

    def _async_raise(self, tid, exctype):

        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)

        if not inspect.isclass(exctype):
            exctype = type(exctype)

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))

        if res == 0:

            raise ValueError("invalid thread id")

        elif res != 1:

            # """if it returns a number greater than one, you're in trouble,

            # and you should call it again with exc=NULL to revert the effect"""

            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)

            raise SystemError("PyThreadState_SetAsyncExc failed")
