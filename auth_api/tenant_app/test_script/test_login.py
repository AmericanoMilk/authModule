from django.test import TestCase
from tenant_app.models import Tenant
from django.test import Client


class TenantLogin(TestCase):
    c = Client()
    tenant = Tenant.objects.first()
    response = c.post("/v1/tenant/login", {
        "tenant": tenant.tenant,
        "password": tenant.password
    })
    print(response.content)

if __name__ == '__main__':
    TenantLogin()
