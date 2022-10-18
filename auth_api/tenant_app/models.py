from django.core.validators import MinLengthValidator
from django.db import models
from shortuuid import uuid
from shortuuid.django_fields import ShortUUIDField

from common.enum.tenant import TenantStatusChoice
from django.utils.translation import gettext_lazy as _

from common_modules.api.model import AbstractBaseModel


# Create your models here.


class Tenant(AbstractBaseModel):
    FORBIDDEN = "FORBIDDEN"
    NORMAL = "NORMAL"
    DELETE = "DELETE"
    tenant = models.CharField(null=False, help_text="租户用户名", max_length=32, unique=True)
    name = models.CharField(null=True, help_text="租户名称", max_length=32, blank=True)
    password = models.CharField(null=False, help_text="密码", max_length=32, blank=False)

    status = models.CharField(choices=TenantStatusChoice.choices, default=TenantStatusChoice.NORMAL, max_length=24)
    is_superuser = models.BooleanField(default=False, help_text="是否超级管理员")
    last_login = models.DateTimeField(auto_now=True, help_text="最后登录", editable=True, db_column="last_login")

    token_version = ShortUUIDField(null=False, max_length=64, help_text="版本", default=uuid())

    class Meta:
        verbose_name = "租户表"
        db_table = "tenant"
        # app_label = "tenant"

    @property
    def is_normal(self):
        return self.status == TenantStatusChoice.NORMAL

    @property
    def is_admin(self):
        return self.is_superuser
