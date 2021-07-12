from django.urls import path

from LetsCook.recipes.views import details_recipe, RecipeCreate, list_recipes

urlpatterns = [
    path('details/<int:pk>', details_recipe, name='details-recipe'),
    path('create', RecipeCreate.as_view(), name='create-recipe'),
    path('list/', list_recipes, name='list-recipes'),
]