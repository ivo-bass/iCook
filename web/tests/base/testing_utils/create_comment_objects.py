from LetsCook.common.models import Comment
from tests.base.testing_utils.create_recipe_objects import create_public_recipe


def create_comment():
    recipe = create_public_recipe()
    user = recipe.author
    comment = Comment.objects.create(
        recipe=recipe,
        user=user,
        text='test text'
    )
    return comment