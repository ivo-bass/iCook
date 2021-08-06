from django.test import TestCase

from LetsCook.core.constants import MEASURES
from LetsCook.recipes.models import Recipe
from tests.base.create_ingredient_objects import create_ingredient_with_all_fields, create_ingredient_with_name_only


class IngredientModelTest(TestCase):
    def test_ingredientInit_withAllFieldsFilled(self):
        ingredient = create_ingredient_with_all_fields()
        recipe = Recipe.objects.first()
        self.assertEqual(recipe, ingredient.recipe)
        self.assertEqual('test name', ingredient.name)
        self.assertEqual(1, ingredient.quantity)
        self.assertEqual(MEASURES[0][0], ingredient.measure)

    def test_ingredientInit_withNameOnly_shouldAutoFill(self):
        ingredient = create_ingredient_with_name_only()
        self.assertEqual(0, ingredient.quantity)
        self.assertEqual('by taste', ingredient.measure)