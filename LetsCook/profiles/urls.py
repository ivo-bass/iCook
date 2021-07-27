from django.urls import path


from LetsCook.profiles import views


urlpatterns = [
    path('home/', views.home, name='home'),

    path('sign-in/', views.SignInView.as_view(), name='sign-in'),

    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),

    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),

    path('my-profile/', views.show_profile, name='my-profile'),

    path('my-recipes/', views.UserRecipesListView.as_view(), name='my-recipes'),

    path('liked-recipes/', views.UserLikedRecipesListView.as_view(), name='liked-recipes'),

    path('update/', views.ProfileUpdateView.as_view(), name='update-profile'),
]


from ..core.signals import *
