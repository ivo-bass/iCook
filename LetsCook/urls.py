from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from LetsCook.recipes.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('recipe/', include('LetsCook.recipes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
