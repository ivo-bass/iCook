from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from LetsCook.core.constants import VALID_IMAGE_EXTENSIONS
from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.core.utils import delete_previous_image
from LetsCook.profiles.models import Profile, Choice

UserModel = get_user_model()


class ProfileUpdateForm(AddBootstrapFormControlMixin, forms.ModelForm):
    image = CloudinaryFileField(
        options={
            'crop': 'thumb',
            'gravity': 'face',
            'width': 200,
            'height': 200,
            'folder': 'profiles'
        },
    )

    def save(self, commit=True):
        delete_previous_image(self, commit, Profile, 'profile-default.jpg')
        return super().save(commit=commit)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'first_name', 'last_name', 'dark_theme']
        widgets = {
            'dark_theme': forms.NullBooleanSelect(),
        }
