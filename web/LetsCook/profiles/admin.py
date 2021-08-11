from django.contrib import admin
from LetsCook.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    user field should not be changed
    """
    readonly_fields = ('user',)
