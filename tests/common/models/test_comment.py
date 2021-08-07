from django.contrib.auth import get_user_model
from django.test import TestCase

from LetsCook.recipes.models import Recipe
from tests.base.create_comment_objects import create_comment

UserModel = get_user_model()


class CommentModelTest(TestCase):
    def test_commentInit(self):
        comment = create_comment()
        user = UserModel.objects.first()
        recipe = Recipe.objects.first()
        self.assertEqual(user.id, comment.user_id)
        self.assertEqual(recipe.id, comment.recipe_id)
        self.assertEqual('test text', comment.text)