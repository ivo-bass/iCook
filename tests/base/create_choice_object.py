from LetsCook.profiles.models import Choice
from tests.base.create_recipe_objects import create_public_recipe


def create_choice():
    recipe = create_public_recipe()
    choice = Choice.objects.create(
        user=recipe.author,
        recipe=recipe
    )
    return choice
