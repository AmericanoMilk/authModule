from django.db import models

from common_modules.api.model import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


# Create your models here.

class APIPermission(AbstractBaseModel):
    class Meta:
        verbose_name = "权限"
        db_table = "permission"

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True, verbose_name=_("Description"))
    # type = models.CharField(choices=PERMISSION_TYPE, max_length=128)


