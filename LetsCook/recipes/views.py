from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from LetsCook.recipes.forms import RecipeForm, IngredientFormSet
from LetsCook.recipes.models import Recipe, MealType


def index(request):
    context = {
    }
    return render(request, 'index.html', context)


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched'].lower()
        in_title = Recipe.objects.filter(
            title__icontains=searched,
            public=True,
        )
        in_description = Recipe.objects.filter(
            description__icontains=searched,
            public=True,
        )
        in_ingredients = Recipe.objects.filter(
            ingredient__name__icontains=searched,
            public=True,
        )
        recipes = set(in_title | in_description | in_ingredients)
        context = {
            'searched': searched,
            'recipes': recipes,
        }
        return render(request, 'recipes/search.html', context)
    return render(request, 'recipes/search.html')


def details_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    ingredients = recipe.ingredients.split(', ')
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
    }
    return render(request, 'recipes/details.html', context)


def all_recipes(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/../../templates/recipes/recipes.html', context)


class RecipeCreate(LoginRequiredMixin, CreateView):
    login_url = 'sign-in'
    # redirect_field_name = '/recipe/create'
    model = Recipe
    template_name = 'recipes/create.html'
    form_class = RecipeForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(RecipeCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ingredients'] = IngredientFormSet(self.request.POST)
        else:
            data['ingredients'] = IngredientFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['ingredients']
        with transaction.atomic():
            # form.instance.created_by = self.request.user
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(RecipeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details-recipe', kwargs={'pk': self.object.pk})
