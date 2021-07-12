from django.urls import path

from LetsCook.recipes import views

urlpatterns = [
    path('details/<int:pk>', views.details_recipe, name='details-recipe'),

    path('create', views.RecipeCreate.as_view(), name='create-recipe'),

    path('list/', views.list_recipes, name='list-recipes'),
]