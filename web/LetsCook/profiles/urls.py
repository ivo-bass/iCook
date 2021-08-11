from django.urls import path


from LetsCook.profiles import views


urlpatterns = [
    path('home/', views.home, name='home'),

    path('suggest/', views.SuggestView.as_view(), name='suggest'),

    path('history/', views.HistoryView.as_view(), name='history'),

    path('update/', views.profile_and_user_update, name='update-profile'),

    path('my-recipes/', views.UserRecipesListView.as_view(), name='my-recipes'),

    path('liked-recipes/', views.UserLikedRecipesListView.as_view(), name='liked-recipes'),

    path('show/<int:pk>', views.ProfileShowView.as_view(), name='show-profile'),
]
