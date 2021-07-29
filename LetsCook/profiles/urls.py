from django.urls import path


from LetsCook.profiles import views


urlpatterns = [
    path('home/', views.home, name='home'),

    path('update/', views.ProfileUpdateView.as_view(), name='update-profile'),

    path('my-recipes/', views.UserRecipesListView.as_view(), name='my-recipes'),

    path('liked-recipes/', views.UserLikedRecipesListView.as_view(), name='liked-recipes'),

    path('show/<int:pk>', views.ProfileShowView.as_view(), name='show-profile'),
]
