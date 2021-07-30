from django.contrib import admin
from LetsCook.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
