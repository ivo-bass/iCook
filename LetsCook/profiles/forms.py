from django import forms
from django.contrib.auth import get_user_model

from LetsCook.core.delete_previos_image import delete_previous_image
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.profiles.models import Profile

UserModel = get_user_model()


class ProfileUpdateForm(AddBootstrapFormControlMixin, forms.ModelForm):

    def save(self, commit=True):
        delete_previous_image(self, commit, model=Profile, file_name='profile-default.jpg')
        return super().save(commit=commit)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'first_name', 'last_name', 'dark_theme',]
        widgets = {
            'image': forms.FileInput(),
            'dark_theme': forms.NullBooleanSelect(),
        }
