from django.urls import path

from LetsCook.recipes.views import details_recipe

urlpatterns = [
    path('details/<int:pk>', details_recipe, name='details-recipe'),
]