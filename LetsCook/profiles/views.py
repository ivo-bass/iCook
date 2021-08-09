import random
from random import choice

from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from LetsCook.auth_icook.forms import UserUpdateForm
from LetsCook.core.constants import CATEGORIES, FUN_FACTS
from LetsCook.core.utils import get_top_recipes, get_recipes_for_current_days, save_suggestion
from LetsCook.profiles.forms import ProfileUpdateForm
from LetsCook.profiles.models import Choice
from LetsCook.recipes.models import Recipe

UserModel = get_user_model()


def generate_fun_fact():
    return random.choice(FUN_FACTS)


@login_required(login_url=reverse_lazy('sign-in'))
def home(request):
    """
    Home View which shows current days history for the user
    and the top public recipes in the db
    """
    recipes_today, recipes_yesterday, recipes_tomorrow = get_recipes_for_current_days(request)
    top_recipes = get_top_recipes()
    most_views, most_likes, most_comments = top_recipes
    from randfacts import get_fact
    fun_fact = get_fact()
    context = {
        'recipes_for_today': recipes_today,
        'recipes_for_yesterday': recipes_yesterday,
        'recipes_for_tomorrow': recipes_tomorrow,
        'most_views': most_views,
        'most_likes': most_likes,
        'most_comments': most_comments,
        'fun_fact': fun_fact,
    }
    return render(request, 'profiles/home.html', context)


class HistoryView(LoginRequiredMixin, ListView):
    """
    This view shows all choices made by the authenticated user
    """
    model = Choice
    template_name = 'profiles/history.html'
    paginate_by = 3
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """
        Retrns all choices for the session user ordered by date
        """
        related_choices = self.object.choice_set.order_by('-date')
        return related_choices


class ProfileShowView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    This view shows foreign profile information with all
    public recipes created by the given user
    """
    model = UserModel
    template_name = 'profiles/show-profile.html'
    paginate_by = 3
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.model.objects.get(pk=self.kwargs["pk"])
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        return context

    def get_queryset(self):
        public_recipes = self.object.recipe_set.filter(public=True)
        return public_recipes


def profile_and_user_update(request):
    """
    This view updates user and profile information altogether
    """
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # should update the session with the new email if changed
            update_session_auth_hash(request, request.user)
            # return redirect('update-profile')
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profiles/update-profile.html', context)


class UserRecipesListView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for recipes created by the current user
    """
    model = UserModel
    template_name = 'profiles/my-recipes.html'
    object = None
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        return context

    def get_queryset(self):
        return self.object.recipe_set.all()


class UserLikedRecipesListView(LoginRequiredMixin, SingleObjectMixin, ListView):
    """
    View for recipes liked by the current user
    """
    model = UserModel
    template_name = 'profiles/liked-recipes.html'
    object = None
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        return context

    def get_queryset(self):
        return self.object.like_set.all()


class SuggestView(LoginRequiredMixin, View):
    """
    This view renders a suggestion for a recipe,
    filtered by meal_type/category
    """

    def get(self, request):
        categories = CATEGORIES
        recipe = None
        public_recipes = Recipe.objects.filter(public=True)
        category_name = request.GET.get('category')
        if not category_name == '' \
                and not category_name == 'Random' \
                and category_name is not None:
            public_recipes = public_recipes.filter(meal_type=category_name)
        if public_recipes:
            recipe = choice(public_recipes)
        context = {
            'recipe': recipe,
            'categories': categories
        }
        return render(request, 'profiles/suggest.html', context)

    def post(self, request):
        save_suggestion(request)
        return redirect('home')
