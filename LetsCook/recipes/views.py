from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from LetsCook.common.forms import CommentForm
from LetsCook.common.models import Like
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
    recipe.likes_count = recipe.like_set.count()
    ingredients = recipe.ingredients.split(', ')
    is_owner = recipe.author == request.user
    is_liked_by_user = recipe.like_set.filter(user_id=request.user.id).exists()
    context = {
        'recipe': recipe,
        'ingredients': ingredients,
        'comments': recipe.comment_set.all(),
        'comment_form': CommentForm(
            initial={'recipe_pk': pk}
        ),
        'is_owner': is_owner,
        'is_liked': is_liked_by_user,
    }
    return render(request, 'recipes/details.html', context)


def all_recipes(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
    }
    return render(request, 'recipes/../../templates/recipes/recipes.html', context)


@login_required
def comment_recipe(request, pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.save()

    return redirect('details-recipe', pk)


@login_required
def like_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    like_object_by_user = recipe.like_set.filter(user_id=request.user.id).first()
    if like_object_by_user:
        like_object_by_user.delete()
    else:
        like = Like(
            recipe=recipe,
            user=request.user,
        )
        like.save()
    return redirect('details-recipe', recipe.pk)


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
            form.instance.author = self.request.user
            self.object = form.save()
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(RecipeCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details-recipe', kwargs={'pk': self.object.pk})
