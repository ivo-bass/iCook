from django.urls import path

from LetsCook.common import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('search/', views.search, name='search'),

    path('like/<int:pk>', views.like_recipe, name='like-recipe'),

    path('comment/<int:pk>', views.comment_recipe, name='comment-recipe'),
]
