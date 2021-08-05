from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from LetsCook.common.forms import CommentForm
from LetsCook.core.constants import CATEGORIES
from LetsCook.core.utils import save_suggestion
from LetsCook.recipes.forms import RecipeForm, IngredientFormSet, RecipeUpdateForm
from LetsCook.recipes.models import Recipe


def details_recipe(request, pk):
    """
    This view shows the recipe for the given pk.
    Has a vary basic view count.
    """
    if request.method == 'POST':
        save_suggestion(request)
        return redirect('home')
    recipe = Recipe.objects.get(pk=pk)
    # increase views count if not own recipe
    if not recipe.author.id == request.user.id:
        recipe.recipe_views = recipe.recipe_views + 1
        recipe.save()
    # get other data
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


class AllRecipesView(ListView):
    """
    This view shows all public recipes
    and provides filtering by meal_type/category
    """
    model = Recipe
    template_name = 'recipes/all-recipes.html'
    context_object_name = 'recipes'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['categories'] = CATEGORIES
        return context

    def get_queryset(self):
        public_recipes = Recipe.objects.filter(public=True)
        category_name = self.request.GET.get('category')
        if not category_name == '' and not category_name == 'All' and category_name is not None:
            public_recipes = public_recipes.filter(meal_type=category_name)
        return public_recipes


class RecipeCreate(LoginRequiredMixin, CreateView):
    """
    This view shows recipe creation form with ingredients inline formset.
    On success redirects to recipe details view
    """
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
        """
        If recipe form is valid validates the ingredients formset
        """
        context = self.get_context_data()
        ingredients = context['ingredients']
        # .atomic() - If there is an exception, the changes are rolled back.
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
    """
    Updates the recipe and all of the ingredients
    """
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
    """
    Confirmation view for recipe deletion.
    """
    model = Recipe
    template_name = 'recipes/delete.html'

    def get_success_url(self):
        return reverse('my-recipes')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect('details-recipe', kwargs['pk'])
        return super().post(request, *args, **kwargs)
