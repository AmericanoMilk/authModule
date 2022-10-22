from tenant_app.models import Tenant as tenant_model


class TenantManagerHelper:
    def search_tenant(self, tenant, be_search_tenant=None, all_results=False):
        if tenant.is_admin:
            if be_search_tenant:
                tenant_list = tenant_model.objects.filter(tenant=be_search_tenant)
            else:
                tenant_list = tenant_model.objects.all()
        elif tenant.tenant == be_search_tenant:
            # 自己查自己
            tenant_list = tenant_model.objects.filter(tenant=tenant.tenant, status=tenant_model.NORMAL)
        else:
            tenant_list = tenant_model.objects.none()
        return tenant_list


tenant_manger_helper = TenantManagerHelper()
