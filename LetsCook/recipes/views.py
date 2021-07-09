from django.shortcuts import render, redirect

from LetsCook.recipes.forms import RecipeForm, IngredientFormSet
from LetsCook.recipes.models import Recipe, MealType


def home(request):
    if request.method == 'POST':
        r_form = RecipeForm(request.POST, request.FILES)
        if r_form.is_valid():
            r_form.save()
            return redirect('home')
        r_form = RecipeForm(request.POST, request.FILES)
        i_form = IngredientFormSet()
        meal_types = MealType.objects.all()
        context = {
            # 'recipes': recipes,
            'r_form': r_form,
            'i_form': i_form,
            'meal_types': meal_types,
        }
        return render(request, 'home.html', context)
    else:
        # recipes = Recipe.objects.all()
        r_form = RecipeForm()
        i_form = IngredientFormSet()
        meal_types = MealType.objects.all()
        context = {
            # 'recipes': recipes,
            'r_form': r_form,
            'i_form': i_form,
            'meal_types': meal_types,
        }
        return render(request, 'home.html', context)


def details_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    ingredients = recipe.ingredients.split(', ')
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipes/details.html', context)
