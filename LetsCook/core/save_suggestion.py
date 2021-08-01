from LetsCook.profiles.models import Choice
from LetsCook.recipes.models import Recipe


def save_suggestion(request):
    recipe_pk = request.POST.get('recipe-pk')
    recipe = Recipe.objects.get(pk=recipe_pk)
    user = request.user
    choice_made = Choice(
        recipe=recipe,
        user=user,
    )
    if request.POST.get('date'):
        choice_made.date = request.POST.get('date')
    choice_made.save()