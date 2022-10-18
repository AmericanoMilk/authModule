from rest_framework.exceptions import NotFound

from common.constant import TENANT_SPLIT
from common.enum.tenant import NORMAL
from common.permission.uri_auth_helper import url_auth_helper
from common.account.utils import split_tenant_user, AccountUtils
from constant import REDIS_TENANT_KEY
from exception.api import NotFoundPage
from user_app import models as user_model
from tenant_app import models as tenant_model

from common_modules.redis_module.redis_client import RedisClient

redis_client = RedisClient()


class RBACRbacBackends:
    # def has_perm(self, user_obj, perm, obj=None):
    #     if user_obj.is_anonymous:
    #         return False
    #
    # def get_all_permission(self, obj):
    #     # 获取当前模型的所有权限
    #     """"""

    def authenticate(self, request, user=None, password=None, tenant=None, **kwargs):
        if user:
            if TENANT_SPLIT in user:
                tenant, user = split_tenant_user(user)
        elif tenant and user:
            pass
        else:
            tenant = tenant
            user = None

        tenant_info_key = REDIS_TENANT_KEY + tenant
        tenant_account = redis_client.get_hash(tenant_info_key, "tenant")

        try:
            if all([tenant, user]):
                # 用户
                # tenant_obj = tenant_model.Tenant.objects.get(tenant=tenant, status=NORMAL)
                auth_obj = user_model.User.objects.get(user=user, status=NORMAL, fk_tenant_id__tenant=tenant_account)
                user_account = auth_obj.user
                # sync_user_helper.user_info(tenant=tenant, user_obj=auth_obj)
            elif tenant:
                # tenant_obj = tenant_model.Tenant.objects.get(tenant=tenant, status=NORMAL)
                user_account = None
                auth_obj = tenant_model.Tenant.objects.get(tenant=tenant, status=NORMAL)
            else:
                ret = {"code": 404, "msg": "", "result": None}
                raise NotFound(ret)
        except Exception as e:
            raise NotFound(e)

        kw = {"tenant": tenant_account, "user": user_account}
        AccountUtils().get_tenant_and_user(request, kw)
        status, args, kwargs = url_auth_helper.has_url_permission(
            tenant=tenant, url=request.path, method=request.method
        )
        try:
            if url_auth_helper.is_whitelist(path=request.path, method=request.method):
                white_status = True
            else:
                white_status = False
            if white_status:
                return auth_obj
            url_auth_helper.has_permission(status=status, kwargs=kwargs, request=request)
        except NotFoundPage:
            raise NotFound()

        return auth_obj
