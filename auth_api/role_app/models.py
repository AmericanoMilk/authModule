from django.db import models

# Create your models here.


class Role(models.Model):
    class Meta:
        verbose_name = "租户表"
        db_table = "role"