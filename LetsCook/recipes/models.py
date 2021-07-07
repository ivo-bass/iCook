from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from LetsCook.core.validators import validate_digits_not_in_string


class Recipe(models.Model):
    # author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            validate_digits_not_in_string,
        ],
    )
    image = models.ImageField(
        upload_to='recipes',
        blank=True,
    )
    description = models.CharField(
        max_length=200,
        blank=True,
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

    upload_time = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title

    @property
    def ingredients(self):
        return ', '.join(str(i) for i in self.ingredient_set.all())


class Ingredient(models.Model):
    name = models.CharField(
        max_length=30
    )
    quantity = models.FloatField()
    measure = models.CharField(
        max_length=20,
        choices=(
            ('gr', 'gr'),
            ('kg', 'kg'),
            ('ml', 'ml'),
            ('l', 'l'),
            ('tea spoon', 'tea spoon'),
            ('table spoon', 'table spoon'),
            ('cup', 'cup'),
        )
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.quantity}{self.measure}"