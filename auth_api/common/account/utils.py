from common.constant import TENANT_SPLIT
from tenant_app import models as tenant_model
from user_app import models as user_model

user_obj_dict = {}
tenant_obj_dict = {}


class AccountUtils:
    def _get_tenant_obj(self, tenant):
        return tenant_model.Tenant.objects.get(tenant=tenant)

    def _get_user_obj(self, user):
        return user_model.User.objects.get(user=user)

    def get_tenant_and_user(self, request, kw):
        tenant = kw.get("tenant")
        user = kw.get("user")

        if tenant:
            request.tenant_account = tenant
            if tenant in tenant_obj_dict:
                request.tenant = tenant_obj_dict[tenant]
            else:
                tenant_obj = self._get_tenant_obj(tenant)
                tenant_obj_dict[tenant] = tenant_obj
                request.tenant = tenant_obj_dict[tenant]

        if user:
            request.user_account = user
            if user in user_obj_dict:
                request.user = user_obj_dict[user]
            else:
                user_obj = self._get_user_obj(user)
                user_obj_dict[user] = user_obj
                request.user = user_obj_dict[user]

        # if not tenant and not user:
        #     raise TenantEmptyError("tenant cannot be null")

    def split_tenant_user(self, user):
        return user.split(TENANT_SPLIT)
