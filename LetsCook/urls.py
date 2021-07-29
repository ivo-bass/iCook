from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('LetsCook.common.urls')),

    path('recipe/', include('LetsCook.recipes.urls')),

    path('profile/', include('LetsCook.profiles.urls')),

    path('auth/', include('LetsCook.auth_icook.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
