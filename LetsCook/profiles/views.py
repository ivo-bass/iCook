from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('sign-in'))
def home(request):
    context = {

    }
    return render(request, 'profiles/home.html', context)


def sign_in(request):
    user = authenticate(email='admin@admin.bg', password='85.abuza')
    login(request, user)
    return redirect('home')


@login_required(login_url=reverse_lazy('sign-in'))
def sign_out(request):
    logout(request)
    return redirect('index')


def sign_up(request):
    context = {

    }
    return render(request, 'profiles/sign-up.html', context)


@login_required(login_url=reverse_lazy('sign-in'))
def show_profile(request):
    context = {

    }
    return render(request, 'profiles/show-profile.html', context)


@login_required(login_url=reverse_lazy('sign-in'))
def my_recipes(request):
    context = {

    }
    return render(request, 'profiles/my-recipes.html', context)