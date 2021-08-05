from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DeleteView

from LetsCook.auth_icook.forms import SignUpForm, SignInForm, BootstrapChangePasswordForm, BootstrapResetPasswordForm, \
    BootstrapSetPasswordForm

UserModel = get_user_model()


class SignUpView(CreateView):
    """
    Overrides CreateView to register the user,
    loads custom user creation form and
    sends activation email
    """
    template_name = 'auth/sign-up.html'
    model = UserModel
    form_class = SignUpForm

    def form_valid(self, form):
        """
        Sets the user to inactive and sends activation email
        :param form:
        :return: activation template
        """
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        message = render_to_string('auth/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(self.request, 'auth/activation_needed.html')


class SignInView(LoginView):
    """
    User login view rendering the sign-in form.
    If the view is called by unauthorized url
    it redirects back to it on success.
    """
    template_name = 'auth/sign-in.html'
    form_class = SignInForm
    redirect_field_name = 'next'


class SignOutView(LoginRequiredMixin, View):
    """
    Simply signs out the user and redirects to index
    """
    def get(self, request):
        logout(request)
        return redirect('index')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Simple confirmation view for user deletion.
    """
    model = UserModel
    template_name = 'auth/delete-user.html'

    def get_success_url(self):
        """
        Cleans the session on success
        :return: index url
        """
        logout(self.request)
        return reverse('index')

    def post(self, request, *args, **kwargs):
        """
        If 'cancel' in request redirects to update-profile view
        otherwise continues to success_url and user deletion
        :return:
        """
        if "cancel" in request.POST:
            return redirect('update-profile')
        return super().post(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'auth/password-reset.html'
    form_class = BootstrapResetPasswordForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'auth/password-reset-done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'auth/password-reset-confirm.html'
    form_class = BootstrapSetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'auth/password-reset-complete.html'


def activate(request, uidb64, token):
    """
    Decodes the user id from activation link ans checks the token.
    Sets the user as active and renders the sign-in view on success.
    Otherwise error msg is rendered.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'auth/sign-in.html', {"form": SignInForm})
    else:
        return render(request, 'auth/activation_invalid.html')


def change_password(request):
    """
    Password change view which updates the session with the new credentials
    Uses custom form and redirects to update-profile url.
    """
    if request.method == 'POST':
        form = BootstrapChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('update-profile')
    else:
        form = BootstrapChangePasswordForm(request.user)
    context = {'form': form}
    return render(request, 'auth/change-password.html', context)
