from django.urls import path


from LetsCook.profiles import views


urlpatterns = [
    path('home/', views.home, name='home'),

    path('sign-in/', views.SignInView.as_view(), name='sign-in'),

    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),

    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),

    path('my-profile/', views.my_profile, name='my-profile'),

    path('my-recipes/', views.my_recipes, name='my-recipes'),
]


from ..core.signals import *
