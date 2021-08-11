from LetsCook.core.constants import CATEGORIES
from LetsCook.recipes.models import Recipe
from tests.base.testing_utils.create_user_objects import create_regular_active_user


def create_public_recipe():
    user = create_regular_active_user()
    recipe = Recipe.objects.create(
        author=user,
        title='test title',
        meal_type=CATEGORIES[0],
        description='test description',
        preparation='test preparation',
        time=1,
        servings=1,
        image=None,
    )
    return recipe


def create_private_recipe():
    user = create_regular_active_user()
    recipe = Recipe.objects.create(
        author=user,
        title='test title',
        meal_type=CATEGORIES[0],
        description='test description',
        preparation='test preparation',
        time=1,
        servings=1,
        image=None,
        public=False,
    )
    return recipe
