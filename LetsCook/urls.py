from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from LetsCook.recipes.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
