from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django_resized import ResizedImageField

from LetsCook.core.validators import validate_digits_not_in_string


UserModel = get_user_model()


class MealType(models.Model):
    name = models.CharField(
        max_length=20,
        choices=(
            ('breakfast', 'breakfast'),
            ('salad', 'salad'),
            ('soup', 'soup'),
            ('appetizer', 'appetizer'),
            ('main', 'main'),
            ('dessert', 'dessert'),
        )
    )

    def __str__(self):
        return self.name


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

    meal_type = models.ForeignKey(
        MealType,
        on_delete=models.PROTECT,
        null=True,
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
    )

    measure = models.CharField(
        max_length=20,
        blank=True,
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
