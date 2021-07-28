from django.urls import path

from LetsCook.recipes import views

urlpatterns = [
    path('create/', views.RecipeCreate.as_view(), name='create-recipe'),

    path('details/<int:pk>', views.details_recipe, name='details-recipe'),

    path('update/<int:pk>', views.RecipeUpdate.as_view(), name='update-recipe'),

    path('delete/<int:pk>', views.RecipeDelete.as_view(), name='delete-recipe'),

    path('all-recipes/', views.AllRecipesView.as_view(), name='all-recipes'),
]
