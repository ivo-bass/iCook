from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):
    context = {

    }
    return render(request, 'users/home.html', context)


def sign_in(request):
    user = authenticate(username='ivo_bass', password='7878')
    login(request, user)
    return redirect('home')


def sign_out(request):
    logout(request)
    return redirect('index')


def sign_up(request):
    context = {

    }
    return render(request, 'users/sign-up.html', context)


def show_profile(request):
    context = {

    }
    return render(request, 'users/show-profile.html', context)


def my_recipes(request):
    context = {

    }
    return render(request, 'users/my-recipes.html', context)
