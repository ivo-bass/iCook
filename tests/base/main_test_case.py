from django.contrib.auth import get_user_model
from django.test import TestCase

from LetsCook.common.models import Comment, Like
from LetsCook.core.constants import CATEGORIES, MEASURES
from LetsCook.profiles.models import Choice
from LetsCook.recipes.models import Recipe, Ingredient

UserModel = get_user_model()


class MainTestCase(TestCase):
    EMAIL = 'test@test.test'
    PASSWORD = 'qwe987qwe987'

    def setUp(self):
        self.user = UserModel.objects.create_user(
            email=MainTestCase.EMAIL,
            password=MainTestCase.PASSWORD,
        )
        self.user.is_active = True
        self.user.save()

    def create_new_user(self):
        self.new_user = UserModel.objects.create_user(
            email='new@new.new',
            password=MainTestCase.PASSWORD,
        )
        self.new_user.is_active = True
        self.new_user.save()

    def create_recipe(self):
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='test title',
            meal_type=CATEGORIES[0],
            description='test description',
            preparation='test preparation',
            time=1,
            servings=1,
            image=None,
        )

    def create_ingredient(self):
        self.ingredient = Ingredient.objects.create(
            recipe=self.recipe,
            name='test name',
            quantity=1.0,
            measure=MEASURES[0][0]
        )

    def create_choice(self):
        self.choice = Choice.objects.create(
            user=self.user,
            recipe=self.recipe
        )

    def create_comment(self):
        self.comment = Comment.objects.create(
            recipe=self.recipe,
            user=self.user,
            text='test text'
        )

    def create_like(self):
        self.like = Like.objects.create(
            recipe=self.recipe,
            user=self.user,
        )
