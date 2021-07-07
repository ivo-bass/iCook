from django.shortcuts import render

from LetsCook.recipes.forms import RecipeForm, IngredientFormSet
from LetsCook.recipes.models import Recipe


def index(request):
    r = Recipe.objects.first()
    recipe = RecipeForm(instance=r)
    form = IngredientFormSet(instance=r)
    context = {
        'r': r,
        'recipe': recipe,
        'form': form,
    }
    pass
    return render(request, 'index.html', context)
