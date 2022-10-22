from __future__ import print_function, unicode_literals
from django.db import connection, models, transaction
from shortuuid.django_fields import ShortUUIDField
from shortuuid import uuid


class AbstractBaseModel(models.Model):
    creationTime = models.DateTimeField(editable=False, auto_now_add=True)
    updatedTime = models.DateTimeField(editable=False, auto_now=True)
    uuid = ShortUUIDField(null=True, max_length=64, help_text="数据uuid", unique=True, default=uuid())

    class Meta:
        abstract = True
