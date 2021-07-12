from django.urls import path


from LetsCook.users import views


urlpatterns = [
    path('', views.home, name='home'),

    path('sign-in/', views.sign_in, name='sign-in'),

    path('sign-up/', views.sign_up, name='sign-up'),

    path('sign-out/', views.sign_out, name='sign-out'),

    path('show/', views.show_profile, name='show-profile'),

    path('my-recipes/', views.my_recipes, name='my-recipes'),
]