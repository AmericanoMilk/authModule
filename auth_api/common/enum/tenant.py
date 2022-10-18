import typing
from dataclasses import dataclass
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class TenantStatusChoice(models.TextChoices):
    FORBIDDEN = "FORBIDDEN", _("FORBIDDEN")
    NORMAL = "NORMAL", _("NORMAL")


if __name__ == '__main__':
    pass
