from django.http import HttpRequest

from iot_utils.constant import GATEWAY_TENANT, ADMIN_TENANT
from tenants_app.views import TenantManagerView
from user_app.user_register_view import UserRegisterView
from tenants_app import models as  tenant_models

class TenantNewEvent:
    def create_by_gateway(self, gatewayId, tenant):
        request = HttpRequest()

        data = {
            "tenant": tenant,
            "name": gatewayId,
            "user": gatewayId,
            "password": f"{gatewayId}123..",
        }

        request.data = data
        request.tenant_account = tenant
        results = UserRegisterView().post(request, tenant=tenant)
        request = HttpRequest()
        request.GET['tenant'] = tenant
        request.tenant = tenant_models.Tenant.objects.get(tenant=ADMIN_TENANT)
        TenantManagerView().delete(request)
