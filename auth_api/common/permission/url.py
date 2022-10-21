import json

from rest_framework import permissions
from rest_framework.request import Request

from common_modules.redis_module.redis_client import RedisClient
from constant import REDIS_TENANT_KEY


class HasUrlPermission(permissions.BasePermission):

    def __init__(self):
        self.redis_client = RedisClient()

    def has_permission(self, request: Request, view):
        name = REDIS_TENANT_KEY + request.user
        role = self.redis_client.client.hget(name, "role")
        args = None
        kw = {}
        if not role:
            return False
        try:
            role = json.loads(role)
        except Exception:
            pass
        if isinstance(role, list):
            for r in role:
                name = REDIS_ROLE_URI_KEY + r + REDIS_SPLIT + "URI" + REDIS_SPLIT + method.upper()
                permission_list = self.redis_client.client.smembers(name)
                for p in permission_list:
                    co = self.get_re_compile(p)
                    if not co:
                        continue
                    match, args, kwargs = self.match(url, co)
                    if match:
                        return match, args, kwargs
            else:
                kw['msg'] = f"all url cannot found {url}"
                return False, args, kw
        else:
            return False, args, kw


def has_object_permission(self, request, view, obj):
    pass
