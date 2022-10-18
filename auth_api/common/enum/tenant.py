import typing
from dataclasses import dataclass
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountStatusChoice(models.TextChoices):
    FORBIDDEN = "FORBIDDEN", _("FORBIDDEN")
    NORMAL = "NORMAL", _("NORMAL")


@dataclass()
class AccountType:
    TENANT: str = "TENANT"
    USER: str = "USER"


if __name__ == '__main__':
    pass
