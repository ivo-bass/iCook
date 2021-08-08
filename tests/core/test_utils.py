import datetime

import requests
from django.test import TestCase

from LetsCook.core.utils import get_recipes_for_day
from LetsCook.profiles.models import Choice
from tests.base.create_choice_object import create_choice

"""
def get_recipes_for_day(request, day):
    user = request.user
    choices_for_day = user.choice_set.filter(date=day)
    recipes = []
    if choices_for_day:
        recipes = [ch.recipe for ch in choices_for_day]
    return recipes
"""


class RecipeForADayTest(TestCase):
    def test_recipeForToday_shouldReturnRecipe(self):
        today = datetime.datetime.today()
        choice = create_choice()
        choice.date = today
        user = choice.user
        recipe = choice.recipe
        request = requests.Request
        request.user = user
        got_recipes = get_recipes_for_day(request, today)
        self.assertIn(recipe, got_recipes)


# all other functions are tested with views testing