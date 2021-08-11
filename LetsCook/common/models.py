from django.contrib.auth import get_user_model
from django.db import models

from LetsCook.recipes.models import Recipe

UserModel = get_user_model()


class Comment(models.Model):
    text = models.TextField(
        max_length=300,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )
    time = models.DateTimeField(
        auto_now_add=True,
    )


class Like(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )