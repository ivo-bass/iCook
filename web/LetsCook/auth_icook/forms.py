from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, \
    SetPasswordForm
from django.core.exceptions import ValidationError

from LetsCook.core.mixins import AddBootstrapFormControlMixin


# get the user_model defined in settings
UserModel = get_user_model()


class SignUpForm(AddBootstrapFormControlMixin, UserCreationForm):
    """
    Custom sign-up form that ignores the username
    with added bootstrap for all of the fields
    """
    class Meta:
        model = UserModel
        fields = ('email', )


class SignInForm(AddBootstrapFormControlMixin, AuthenticationForm):
    """
    Custom sign-in form that takes the 'username' data
    which is an email and uses it to authenticate the user.
    Bootstrap added.
    """
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
    """
    Updates the user credentials using bootstrap
    """
    class Meta:
        model = UserModel
        fields = ('email', )


class BootstrapChangePasswordForm(AddBootstrapFormControlMixin, PasswordChangeForm):
    pass


class BootstrapResetPasswordForm(AddBootstrapFormControlMixin, PasswordResetForm):
    pass


class BootstrapSetPasswordForm(AddBootstrapFormControlMixin, SetPasswordForm):
    pass