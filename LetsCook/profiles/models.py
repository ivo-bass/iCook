from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from django.db import models
from django_resized import ResizedImageField

from LetsCook.core.managers import ICookUserManager


class ICookUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    USERNAME_FIELD = 'email'

    objects = ICookUserManager()


class Profile(models.Model):
    user = models.OneToOneField(
        ICookUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    username = models.CharField(
        max_length=20,
        blank=True,
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
    )

    image = ResizedImageField(
        size=[200, 200],
        crop=['middle', 'center'],
        default='profile-default.jpg',
        upload_to='profiles',
        blank=True,
    )

    dark_theme = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.user.email
