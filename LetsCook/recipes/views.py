from django.shortcuts import render

from LetsCook.recipes.forms import RecipeForm, IngredientFormSet
from LetsCook.recipes.models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    # recipe = RecipeForm(instance=r)
    # form = IngredientFormSet(instance=r)
    context = {
        'recipes': recipes,
    }
    return render(request, 'index.html', context)


def details_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    ingredients = recipe.ingredients.split(', ')
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipes/details.html', context)
