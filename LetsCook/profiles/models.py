from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User
from django.db import models
from django.utils import timezone

from LetsCook.recipes.models import Recipe


UserModel = get_user_model()


class Profile(models.Model):
    """
    User profile model related to the user by on-to-one relation,
    deleted on user deletion.
    """
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    username = models.CharField(
        max_length=20,
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
    )

    last_name = models.CharField(
        max_length=30,
        blank=True,
    )

    image = CloudinaryField(
        'image',
    )

    dark_theme = models.BooleanField(
        default=False,
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

    @property
    def progress(self):
        username = 25 if self.username else 0
        first_name = 25 if self.first_name else 0
        last_name = 25 if self.last_name else 0
        image = 25 if not None else 0
        value = username + first_name + last_name + image
        return value


class Choice(models.Model):
    """
    Choice made by user with a recipe for a given date
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    date = models.DateField(
        default=timezone.now
    )
