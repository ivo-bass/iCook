from django.urls import path

from LetsCook.recipes import views
from LetsCook.recipes.views import like_recipe, comment_recipe

urlpatterns = [
    path('details/<int:pk>', views.details_recipe, name='details-recipe'),

    path('create', views.RecipeCreate.as_view(), name='create-recipe'),

    path('all-recipes/', views.all_recipes, name='all-recipes'),

    path('search/', views.search, name='search'),

    path('like/<int:pk>', like_recipe, name='like-recipe'),

    path('comment/<int:pk>', comment_recipe, name='comment-recipe'),
]