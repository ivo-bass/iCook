from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from LetsCook.core.constants import VALID_IMAGE_EXTENSIONS
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.core.utils import delete_previous_image
from LetsCook.profiles.models import Profile, Choice

UserModel = get_user_model()


class ProfileUpdateForm(AddBootstrapFormControlMixin, forms.ModelForm):

    def save(self, commit=True):
        delete_previous_image(self, commit, Profile, 'profile-default.jpg')
        return super().save(commit=commit)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'first_name', 'last_name', 'dark_theme']
        widgets = {
            'image': forms.FileInput(),
            'dark_theme': forms.NullBooleanSelect(),
        }

    def clean_image(self):
        image = self.cleaned_data['image']
        if image.name:
            ext = image.name.split('.')[-1]
            if ext not in VALID_IMAGE_EXTENSIONS:
                raise ValidationError('Unsupported file extension.')
        return image