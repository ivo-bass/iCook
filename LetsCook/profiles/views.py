from urllib.parse import quote_from_bytes

from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, RedirectView

from LetsCook.profiles.forms import SignUpForm, SignInForm

UserModel = get_user_model()


@login_required(login_url=reverse_lazy('sign-in'))
def home(request):
    context = {

    }
    return render(request, 'profiles/home.html', context)


class SignUpView(CreateView):
    template_name = 'profiles/sign-up.html'
    model = UserModel
    form_class = SignUpForm
    success_url = reverse_lazy('sign-in')


class SignInView(LoginView):
    template_name = 'profiles/sign-in.html'
    form_class = SignInForm

    def get_success_url(self):
        # if self.request.GET.get('next'):
        #     url = self.request.GET.get('next')
        #     return redirect(url)
        return reverse('home')


class SignOutView(LoginRequiredMixin, View):
    login_url = 'sign-in'

    @staticmethod
    def get(request):
        logout(request)
        return redirect('index')


@login_required(login_url=reverse_lazy('sign-in'))
def my_profile(request):
    context = {

    }
    return render(request, 'profiles/show-profile.html', context)


@login_required(login_url=reverse_lazy('sign-in'))
def my_recipes(request):
    context = {

    }
    return render(request, 'profiles/my-recipes.html', context)