import json
import re

from django.http import HttpResponseNotFound
from common_modules.redis_module.redis_client import RedisClient
from common_modules.constant import REDIS_TENANT_KEY

redis_client = RedisClient()


class URLAuthHelper:
    compile = dict()

    def __init__(self):
        self.redis_client = redis_client

    def has_url_permission(self, tenant, method, url, *args, **kwargs):
        # 先获取角色

        # 判断角色有无权限
        name = REDIS_TENANT_KEY + tenant
        role = self.redis_client.client.hget(name, "role")
        args = None
        kw = {}
        if not role:
            return False, args, kwargs
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

    def match(self, path, regex):
        match = regex.search(path)
        if match:
            kwargs = match.groupdict()
            args = () if kwargs else match.groups()
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            if match.start() != 0:
                return None, None, None
            return True, args, kwargs
        else:
            return None, None, None

    def get_re_compile(self, pp):
        results = []
        if pp in self.compile:
            return self.compile[pp]
        for i in pp.split("/"):
            match = re.search(r"{.*}", i)
            if match:
                params = i[match.start() + 1: match.end() - 1]
                results.append("(?P<parameter>.*)".replace("parameter", params))
            else:
                results.append(i)

        try:
            co = re.compile("/".join(results))
            self.compile[pp] = co
            return co
        except Exception as e:
            logger.debug(str(e))
            return None

    def is_whitelist(self, path, method):
        name = REDIS_WHITE_LIST + method
        results = self.redis_client.client.smembers(name)
        for i in results:
            co = self.get_re_compile(i)
            match, args, kw = self.match(path, co)
            if match:
                return True
        else:
            return False

    def tenant_is_right(self, kw_tenant, url_tenant):
        return True

    def has_permission(self, status, kwargs, request):
        if status:
            tenant = kwargs.get("tenant", None)
            if tenant is not None:
                if request.tenant.is_admin:
                    if not redis_client.client.sismember(REDIS_TENANT_LIST_KEY, tenant):
                        logger.info(
                            "not match url",
                            request.path,
                            f"reason: {tenant} not found",
                        )

                        raise NotFoundPage()
                elif request.tenant_account != tenant:
                    logger.info(
                        "not match url",
                        request.path,
                        f"reason: tenant not match {kwargs.get('msg', None) if isinstance(kwargs, dict) else None}",
                    )
                    raise NotFoundPage()
        else:
            logger.info(
                "not match url",
                request.path,
                f"reason:{kwargs.get('msg', None) if isinstance(kwargs, dict) else None}",
            )
            raise NotFoundPage()


url_auth_helper = URLAuthHelper()
