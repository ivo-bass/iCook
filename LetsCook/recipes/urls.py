from django.urls import path

from LetsCook.recipes import views


urlpatterns = [
    path('details/<int:pk>', views.details_recipe, name='details-recipe'),

    path('create/', views.RecipeCreate.as_view(), name='create-recipe'),

    path('all-recipes/', views.AllRecipesView.as_view(), name='all-recipes'),
]