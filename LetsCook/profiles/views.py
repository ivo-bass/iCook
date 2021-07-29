from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from LetsCook.auth_icook.forms import UserUpdateForm
from LetsCook.profiles.forms import ProfileUpdateForm

UserModel = get_user_model()


@login_required(login_url=reverse_lazy('sign-in'))
def home(request):
    context = {

    }
    return render(request, 'profiles/home.html', context)




class ProfileShowView(LoginRequiredMixin, SingleObjectMixin, ListView):
    login_url = 'sign-in'
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
    login_url = 'sign-in'
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
    login_url = 'sign-in'
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
    login_url = 'sign-in'
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