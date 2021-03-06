from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from LetsCook.core.managers import ICookUserManager


class ICookUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model. Overrides AbstractBaseUser
    changing the username field to email.
    """
    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'email'

    objects = ICookUserManager()
