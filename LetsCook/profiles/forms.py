from cloudinary.forms import CloudinaryFileField
from django import forms
from django.contrib.auth import get_user_model

from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.core.utils import delete_previous_image
from LetsCook.profiles.models import Profile

UserModel = get_user_model()


class ProfileUpdateForm(AddBootstrapFormControlMixin, forms.ModelForm):
    """
    Profile is created on user creation. This form is for update.
    Takes care of profile image - crops it and stores it in 'profile'
    folder in Cloudinary.
    On save tries to delete previous image if such exists.
    """
    image = CloudinaryFileField(
        required=False,
        options={
            'crop': 'fill',
            'gravity': 'center',
            'width': 200,
            'height': 200,
            'folder': 'profiles',
        },
    )

    def save(self, commit=True):
        delete_previous_image(self, Profile)
        return super().save(commit=commit)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'first_name', 'last_name', 'dark_theme']
        widgets = {
            'dark_theme': forms.NullBooleanSelect(),
        }
