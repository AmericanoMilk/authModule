from tenant_app import models as tenant_model
from tenant_app.models import Tenant


class TenantManagerHelper:
    def search_tenant(self, tenant, be_search_tenant=None, all_results=False):
        if tenant.is_admin:
            if be_search_tenant:
                tenant_list = tenant_model.Tenant.objects.filter(tenant=be_search_tenant)
            else:
                tenant_list = tenant_model.Tenant.objects.all()
        elif tenant == be_search_tenant:
            # 自己查自己
            tenant_list = tenant_model.Tenant.objects.filter(tenant=tenant, status=Tenant.NORMAL)
        else:
            tenant_list = []
        return tenant_list


tenant_manger_helper = TenantManagerHelper()
