from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import MultipleObjectMixin

from LetsCook.common.forms import CommentForm
from LetsCook.common.models import Like
from LetsCook.recipes.forms import RecipeForm, IngredientFormSet, RecipeUpdateForm
from LetsCook.recipes.models import Recipe, MealType


def details_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    # increase views count if not own recipe
    if not recipe.author.id == request.user.id:
        recipe.recipe_views = recipe.recipe_views + 1
        recipe.save()
    # get other data
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


# class RecipeDetailView(DetailView):
#     model = Recipe
#     template_name = 'recipes/details.html'
#     context_object_name = 'recipes'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         recipe = Recipe.objects.get(pk=pk)
#         recipe.likes_count = recipe.like_set.count()
#         ingredients = recipe.ingredients.split(', ')
#         is_owner = recipe.author == request.user
#         is_liked_by_user = recipe.like_set.filter(user_id=request.user.id).exists()
#         context = {
#             'recipe': recipe,
#             'ingredients': ingredients,
#             'comments': recipe.comment_set.all(),
#             'comment_form': CommentForm(
#                 initial={'recipe_pk': pk}
#             ),
#             'is_owner': is_owner,
#             'is_liked': is_liked_by_user,
#         }
#         return context


class AllRecipesView(ListView):
    model = Recipe
    template_name = 'recipes/all-recipes.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        categories = MealType.objects.all()
        context['categories'] = categories
        return context

    def get_queryset(self):
        all_public_recipes = Recipe.objects.filter(public=True)
        category_name = self.request.GET.get('category')
        category = None
        if not category_name in ('', 'All') and category_name is not None:
            category = MealType.objects.get(name=category_name)
        if not category == '' and category is not None:
            all_public_recipes = all_public_recipes.filter(public=True, meal_type=category.id)
        return all_public_recipes


class RecipeCreate(LoginRequiredMixin, CreateView):
    login_url = 'sign-in'
    model = Recipe
    template_name = 'recipes/create.html'
    form_class = RecipeForm

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


class RecipeUpdate(LoginRequiredMixin, UpdateView):
    login_url = 'sign-in'
    model = Recipe
    template_name = 'recipes/update.html'
    form_class = RecipeUpdateForm

    def get_context_data(self, **kwargs):
        data = super(RecipeUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['ingredients'] = IngredientFormSet(self.request.POST, instance=self.object)
        else:
            data['ingredients'] = IngredientFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        ingredients = context['ingredients']
        with transaction.atomic():
            if ingredients.is_valid():
                ingredients.instance = self.object
                ingredients.save()
        return super(RecipeUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details-recipe', kwargs={'pk': self.object.pk})


class RecipeDelete(LoginRequiredMixin, DeleteView):
    login_url = 'sign-in'
    model = Recipe
    template_name = 'recipes/delete.html'

    def get_success_url(self):
        return reverse('my-recipes')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect('details-recipe', kwargs['pk'])
        return super().post(request, *args, **kwargs)
