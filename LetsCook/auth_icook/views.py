from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DeleteView

from LetsCook.auth_icook.forms import SignUpForm, SignInForm, UserUpdateForm
from LetsCook.profiles.forms import ProfileUpdateForm

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'auth/sign-up.html'
    model = UserModel
    form_class = SignUpForm
    success_url = reverse_lazy('update-profile')

    def form_valid(self, form):
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


def activate(request, uidb64, token):
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


class SignInView(LoginView):
    template_name = 'auth/sign-in.html'
    form_class = SignInForm
    # redirect_authenticated_user = True
    redirect_field_name = 'next'


class SignOutView(LoginRequiredMixin, View):
    login_url = 'sign-in'

    @staticmethod
    def get(request):
        logout(request)
        return redirect('index')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'sign-in'
    model = UserModel
    template_name = 'auth/delete-user.html'

    def get_success_url(self):
        logout(self.request)
        return reverse('index')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect('update-profile')
        return super().post(request, *args, **kwargs)
