import datetime
from random import choice

from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from LetsCook.auth_icook.forms import UserUpdateForm
from LetsCook.core.constants import CATEGORIES
from LetsCook.core.save_suggestion import save_suggestion
from LetsCook.profiles.forms import ProfileUpdateForm
from LetsCook.profiles.models import Choice
from LetsCook.recipes.models import Recipe

UserModel = get_user_model()


def get_recipes_for_day(request, day):
    user = request.user
    choices_for_day = user.choice_set.filter(date=day)
    recipes = []
    if choices_for_day:
        recipes = [ch.recipe for ch in choices_for_day]
    return recipes


def get_top_recipes(request):
    all_public_recipes = Recipe.objects.filter(public=True)
    most_views = Recipe.objects.filter(public=True).order_by('recipe_views').last()
    most_likes = list(sorted(all_public_recipes, key=lambda obj: -obj.likes_count))[0]
    most_comments = list(sorted(all_public_recipes, key=lambda obj: -obj.comments_count))[0]
    return most_views, most_likes, most_comments


@login_required(login_url=reverse_lazy('sign-in'))
def home(request):
    today = datetime.date.today()
    recipes_today = get_recipes_for_day(request, today)

    yesterday = today - datetime.timedelta(days=1)
    recipes_yesterday = get_recipes_for_day(request, yesterday)

    tomorrow = today + datetime.timedelta(days=1)
    recipes_tomorrow = get_recipes_for_day(request, tomorrow)

    most_views, most_likes, most_comments = get_top_recipes(request)

    context = {
        'recipes_for_today': recipes_today,
        'recipes_for_yesterday': recipes_yesterday,
        'recipes_for_tomorrow': recipes_tomorrow,
        'most_views': most_views,
        'most_likes': most_likes,
        'most_comments': most_comments,
    }
    return render(request, 'profiles/home.html', context)


class SuggestView(LoginRequiredMixin, View):
    def get(self, request):
        categories = CATEGORIES
        recipe = None
        public_recipes = Recipe.objects.filter(public=True)
        category_name = request.GET.get('category')
        if not category_name == '' and not category_name == 'Random' and category_name is not None:
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


class HistoryView(LoginRequiredMixin, ListView):
    model = Choice
    template_name = 'profiles/history.html'
    paginate_by = 3
    ordering = None
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        return super().get(request, *args, **kwargs)

    # Todo: filter history by date
    # def post(self, request, *args, **kwargs):
    #     pass

    def get_queryset(self):
        """
        :return: all choices for the session user ordered by date
        """
        related_choices = self.object.choice_set.order_by('-date')
        return related_choices


class ProfileShowView(LoginRequiredMixin, SingleObjectMixin, ListView):
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


class ProfileUpdateView(LoginRequiredMixin, View):
    redirect_field_name = 'profile'

    @staticmethod
    def get(request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'profiles/update-profile.html', context)

    @staticmethod
    def post(request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Success')
            update_session_auth_hash(request, request.user)
            return redirect('update-profile')


class UserRecipesListView(LoginRequiredMixin, SingleObjectMixin, ListView):
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
