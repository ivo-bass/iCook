from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView

from LetsCook.auth_icook.forms import SignUpForm, SignInForm

UserModel = get_user_model()


class SignUpView(CreateView):
    template_name = 'profiles/sign-up.html'
    model = UserModel
    form_class = SignUpForm
    success_url = reverse_lazy('update-profile')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        login(self.request, self.object)
        return to_return


class SignInView(LoginView):
    template_name = 'profiles/sign-in.html'
    form_class = SignInForm

    def get_success_url(self):
        # if self.request.GET.get('next'):
        #     url = self.request.GET.get('next')
        #     return redirect(url)
        return reverse('home')


class SignOutView(LoginRequiredMixin, View):
    login_url = 'sign-in'

    @staticmethod
    def get(request):
        logout(request)
        return redirect('index')


class UserDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'sign-in'
    model = UserModel
    template_name = 'profiles/delete-user.html'

    def get_success_url(self):
        logout(self.request)
        return reverse('index')