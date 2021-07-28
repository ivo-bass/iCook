import os.path

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from LetsCook.core.mixins import AddBootstrapFormControlMixin
from LetsCook.profiles.models import Profile

UserModel = get_user_model()


class SignUpForm(AddBootstrapFormControlMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class SignInForm(AddBootstrapFormControlMixin, AuthenticationForm):
    user = None

    def clean_password(self):
        super().clean()
        self.user = authenticate(
            email=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
        )

        if not self.user:
            raise ValidationError('Email and/or password incorrect')

    def save(self):
        return self.user


class UserUpdateForm(AddBootstrapFormControlMixin, forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('email',)


class ProfileUpdateForm(AddBootstrapFormControlMixin, forms.ModelForm):
    def save(self, commit=True):
        # delete previous image - works only on frontend
        db_profile = Profile.objects.get(pk=self.instance.pk)
        new_image = self.files.get('image')
        old_image = str(db_profile.image)
        old_image_path = os.path.join(settings.MEDIA_ROOT, old_image)
        if commit and new_image and old_image and not old_image == 'profile-default.jpg':
            os.remove(old_image_path)
        return super().save(commit=commit)

    class Meta:
        model = Profile
        fields = ['image', 'username', 'first_name', 'last_name']
        widgets = {
            'image': forms.FileInput()
        }
