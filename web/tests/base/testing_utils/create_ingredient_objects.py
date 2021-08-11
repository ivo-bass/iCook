from LetsCook.core.constants import MEASURES
from LetsCook.recipes.models import Ingredient
from tests.base.testing_utils.create_recipe_objects import create_public_recipe


def create_ingredient_with_all_fields():
    recipe = create_public_recipe()
    ingredient = Ingredient.objects.create(
        recipe=recipe,
        name='test name',
        quantity=1.0,
        measure=MEASURES[0][0]
    )
    return ingredient


def create_ingredient_with_name_only():
    recipe = create_public_recipe()
    ingredient = Ingredient.objects.create(
        recipe=recipe,
        name='test name',
    )
    return ingredient