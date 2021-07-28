from django.urls import path


from LetsCook.profiles import views


urlpatterns = [
    path('home/', views.home, name='home'),

    path('sign-in/', views.SignInView.as_view(), name='sign-in'),

    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),

    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),

    path('update/', views.ProfileUpdateView.as_view(), name='update-profile'),

    path('my-recipes/', views.UserRecipesListView.as_view(), name='my-recipes'),

    path('liked-recipes/', views.UserLikedRecipesListView.as_view(), name='liked-recipes'),

    path('show/<int:pk>', views.ProfileShowView.as_view(), name='show-profile'),

    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='delete-user'),
]


from ..core.signals import *
