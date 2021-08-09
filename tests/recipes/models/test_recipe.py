from django.contrib.auth import get_user_model
from django.test import TestCase

from LetsCook.core.constants import CATEGORIES
from tests.base.testing_utils.create_recipe_objects import create_public_recipe

"""
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

    image = CloudinaryField(
        'image',
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

    @property
    def likes_count(self):
        return self.like_set.count()

    @property
    def comments_count(self):
        return self.comment_set.count()

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
"""

UserModel = get_user_model()


class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = create_public_recipe()

    def test_recipe_init(self):
        user = UserModel.objects.first()
        self.assertEqual(user.id, self.recipe.author_id)
        self.assertEqual('test title', self.recipe.title)
        self.assertEqual('test description', self.recipe.description)
        self.assertEqual('test preparation', self.recipe.preparation)
        self.assertEqual(CATEGORIES[0], self.recipe.meal_type)
        self.assertEqual(1, self.recipe.time)
        self.assertEqual(1, self.recipe.servings)
        self.assertFalse(self.recipe.vegetarian)
        self.assertTrue(self.recipe.public)
        self.assertEqual(0, self.recipe.recipe_views)
        self.assertEqual(0, self.recipe.likes_count)
        self.assertEqual(0, self.recipe.comments_count)

    def test_recipeTitleOnSave_isLower(self):
        is_lowercase = self.recipe.title.islower()
        self.assertTrue(is_lowercase)