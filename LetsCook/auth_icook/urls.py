from django.urls import path

from LetsCook.auth_icook import views

urlpatterns = [
    path('sign-in/', views.SignInView.as_view(), name='sign-in'),

    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),

    path('sign-out/', views.SignOutView.as_view(), name='sign-out'),

    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='delete-user'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('change-password/', views.change_password, name='change-password'),

    path('reset-password/', views.CustomPasswordResetView.as_view(), name='reset_password'),

    path('reset-password-sent/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('reset-password-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

from ..core.signals import *
