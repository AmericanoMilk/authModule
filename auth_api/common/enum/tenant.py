import enum

from django.db import models
from django.utils.translation import gettext_lazy as _

FORBIDDEN = "FORBIDDEN"
NORMAL = "NORMAL"
DELETE = "DELETE"
TenantStatusChoices = ((FORBIDDEN, _(FORBIDDEN)), (NORMAL, _(NORMAL)), (DELETE, _(DELETE)))
