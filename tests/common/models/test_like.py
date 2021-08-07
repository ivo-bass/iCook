from django.contrib.auth import get_user_model
from django.test import TestCase

from LetsCook.recipes.models import Recipe
from tests.base.create_like_object import create_like

UserModel = get_user_model()


class LikeModelTest(TestCase):
    def test_like_init(self):
        like = create_like()
        user = UserModel.objects.first()
        recipe = Recipe.objects.first()
        self.assertEqual(user.id, like.user_id)
        self.assertEqual(recipe.id, like.recipe_id)
