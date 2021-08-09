from LetsCook.common.models import Like
from tests.base.testing_utils.create_recipe_objects import create_public_recipe


def create_like():
    recipe = create_public_recipe()
    user = recipe.author
    like = Like.objects.create(
        recipe=recipe,
        user=user,
    )
    return like