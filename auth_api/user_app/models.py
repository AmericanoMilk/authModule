from django.contrib.auth.models import PermissionsMixin, AbstractUser
from shortuuid import uuid
from shortuuid.django_fields import ShortUUIDField

from common.enum.tenant import TenantStatusChoice
from common_modules.api.deprecation import CallableFalse, CallableTrue
from common_modules.api.model import AbstractBaseModel
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from tenant_app.models import Tenant


# Create your models here.
class AbsCustomUser(AbstractBaseModel):
    __rbac_backend = None
    USERNAME_FIELD = None
    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    @property
    def is_anonymous(self):
        """
        always False
        :return:
        """
        return CallableFalse

    def get_all_roles(self):
        raise NotImplementedError("Subclasses must define how they should be return QuerySet")

    def get_all_permissions(self):
        raise NotImplementedError("Subclasses must define how they should be return QuerySet")

    def has_perm(self, perm_list, obj=None):
        raise NotImplementedError("Subclasses must define how they should be return QuerySet")

    def has_module_perms(self, app_label):
        raise NotImplementedError("Subclasses must define how they should be return QuerySet")


class UserManager(BaseUserManager):
    def create_user(self, user, password, name=None):
        if not user:
            raise ValueError("User must have User filed")
        user = self.model(user=user, password=password, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user, password, name=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(user=user, password=password, name=name)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class AuthUser(AbsCustomUser, AbstractUser, PermissionsMixin):
    """
    替换原生User
    """

    __rbac_backend = None
    first_name = None
    last_name = None
    email = None
    date_joined = None

    USERNAME_FIELD = "user"
    REQUIRED_FIELDS = ("password", "fk_tenant_id")
    objects = UserManager()

    user = models.CharField(null=False, blank=False, help_text="用户名", max_length=32, unique=True)
    password = models.CharField(null=False, blank=False, help_text="密码", max_length=128)
    token_version = ShortUUIDField(null=True, max_length=64, help_text="版本", unique=True, default=uuid())

    status = models.CharField(choices=TenantStatusChoice.choices, default=TenantStatusChoice.NORMAL, max_length=24)
    fk_tenant_id = models.OneToOneField(Tenant, on_delete=models.CASCADE, help_text="租户")

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_("Designates that this user has all permissions without" "explicitly assigning them."),
        db_column="is_superuser",
    )

    class Meta:
        verbose_name = "用户表"
        db_table = "auth_user"
        unique_together = ("user", "fk_tenant_id")
        """Due to limitations of Django’s dynamic dependency feature for swappable models, the model referenced by 
        AUTH_USER_MODEL must be created in the first migration of its app (usually called 0001_initial); otherwise, 
        you’ll have dependency issues. """
        swappable = "AUTH_USER_MODEL"
        # app_label = "user"

    def get_all_roles(self):
        pass
        # return Role.object.filter()

    def get_all_permissions(self, obj=None):
        if not self.__rbac_backend:
            from backends.backends import RBACRbacBackends

            self.__rbac_backend = RBACRbacBackends()
        return self.__rbac_backend.get_all_permission(self)

    @property
    def is_anonymous(self):
        return CallableFalse

    @property
    def is_authenticated(self):
        return CallableTrue

    @property
    def is_normal(self):
        return self.is_active

    @property
    def is_admin(self):
        return self.is_superuser

    def has_perm(self, perm_list, obj=None):
        pass

    def has_module_perms(self, app_label):
        pass
