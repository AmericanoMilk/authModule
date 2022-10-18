# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta

import jwt


class JwtUtils(object):
    def __init__(self, key):
        self.key = key

    def encode(self, payload, expire=60 * 60 * 2):
        """
        获取token
        :param expires:  过期时间
        :param payload: dict
        :return: str
        """

        # 使用utc时间
        if expire == -1:
            pass
        elif expire:
            payload["exp"] = int(time.time()) + expire
        else:
            raise ValueError("jwt encode need expire time")

        return jwt.encode(payload=payload, key=self.key, algorithm="HS256")

    def decode(self, token):
        """
        验证并解析token
        :param token: str
        :return:  dict
        """

        return jwt.decode(jwt=token, key=self.key, algorithms="HS256")


if __name__ == "__main__":
    jwtu = JwtUtils(key="django-insecure-2d*-92w0w_hp3aa_u8@y62sn)1zp5rqq%m*#(qy3t%on-0lgnn")
    c = jwtu.encode({"tenant": "aaa", "name": "John Doe", "iat": 1516239022})
    print(jwtu.decode(c.encode()))
