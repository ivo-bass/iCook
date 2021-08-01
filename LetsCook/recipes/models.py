from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django_resized import ResizedImageField

from LetsCook.core.constants import MEAL_TYPES
from LetsCook.core.validators import validate_digits_not_in_string

UserModel = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            validate_digits_not_in_string,
        ],
    )

    meal_type = models.CharField(
        max_length=20,
        choices=(
            MEAL_TYPES
        )
    )

    # 1920 / 1080
    # 340 / 191
    # 680 / 382
    image = ResizedImageField(
        size=[680, 382],
        crop=['middle', 'center'],
        default='food-default.png',
        upload_to='recipes',
        blank=True,
    )

    description = models.CharField(
        max_length=100,
    )

    time = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    servings = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ]
    )

    preparation = models.TextField(
        max_length=1000,
    )
    vegetarian = models.BooleanField(
        default=False,
    )
    public = models.BooleanField(
        default=True,
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    recipe_views = models.IntegerField(
        default=0,
    )

    def __str__(self):
        return self.title

    @property
    def ingredients(self):
        return ', '.join(str(i) for i in self.ingredient_set.all())

    class Meta:
        ordering = ['-id']


class Ingredient(models.Model):
    name = models.CharField(
        max_length=30
    )

    quantity = models.FloatField(
        blank=True,
        default=0.0,
    )

    measure = models.CharField(
        max_length=20,
        blank=True,
        default='by taste',
        choices=(
            ('g', 'g'),
            ('kg', 'kg'),
            ('ml', 'ml'),
            ('l', 'l'),
            ('tsp', 'tsp'),
            ('tbsp', 'tbsp'),
            ('cup', 'cup'),
            ('pcs', 'pcs'),
        )
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.measure}"
