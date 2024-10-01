import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


from company.models import Company
from libs.models import BaseModel

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, BaseModel):
    user_id = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250)
    position = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(max_length=100)
    company = models.ForeignKey(
        Company, null=True, blank=True, on_delete=models.SET_NULL
    )
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Module(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Module")
        verbose_name_plural = _("Modules")


class Role(BaseModel):
    role_id = models.CharField(max_length=250)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


class RoleAccess(BaseModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Module)

    class Meta:
        verbose_name = _("RoleAccess")
        verbose_name_plural = _("RoleAccesses")


class UserRole(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("UserRole")
        verbose_name_plural = _("UserRoles")


class Division(BaseModel):
    division_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    description = models.TextField()
    is_active = models.BooleanField()

    class Meta:
        verbose_name = _("Division")
        verbose_name_plural = _("Divisions")


class AuthToken(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    device_id = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = _("Auth Token")
        verbose_name_plural = _("Auth Tokens")
