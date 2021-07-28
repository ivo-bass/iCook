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

    @property
    def rang(self):
        rang = 'Beginner'
        likes = self.user.like_set.count()
        comments = self.user.comment_set.count()
        recipes = self.user.recipe_set.count()
        if likes and comments and recipes:
            rang = 'Intermediate'
        if likes > 10 and comments > 10 and recipes > 3:
            rang = 'Advanced'
        elif likes > 20 and comments > 20 and recipes > 10:
            rang = 'Expert'
        elif likes > 30 and comments > 30 and recipes > 20:
            rang = 'All Star'
        return rang
