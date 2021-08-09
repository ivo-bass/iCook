from django.contrib.auth import get_user_model
from django.test import TestCase

from LetsCook.recipes.models import Recipe
from tests.base.testing_utils.create_choice_object import create_choice

UserModel = get_user_model()


class ChoiceModelTest(TestCase):
    def test_choiceInit(self):
        choice = create_choice()
        user = UserModel.objects.first()
        recipe = Recipe.objects.first()
        self.assertEqual(choice.user_id, user.id)
        self.assertEqual(choice.recipe_id, recipe.id)
        self.assertIsNotNone(choice.date)