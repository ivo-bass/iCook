from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from LetsCook.core.mixins import AddBootstrapFormControlMixin

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
