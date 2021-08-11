from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
                  path('admin/', admin.site.urls, name='admin-site'),

                  path('', include('LetsCook.common.urls')),

                  path('recipe/', include('LetsCook.recipes.urls')),

                  path('profile/', include('LetsCook.profiles.urls')),

                  path('auth/', include('LetsCook.auth_icook.urls')),

                  path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("images/favicon.ico"))),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
