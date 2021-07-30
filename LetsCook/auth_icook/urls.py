from django.urls import path

from LetsCook.auth_icook import views

urlpatterns = [
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),

    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),

    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),

    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='delete-user'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

from ..core.signals import *