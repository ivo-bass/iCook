from urllib.parse import quote_from_bytes

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, RedirectView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from LetsCook.profiles.forms import SignUpForm, SignInForm, UserUpdateForm, ProfileUpdateForm

UserModel = get_user_model()


@login_required(login_url=reverse_lazy('sign-in'))
def home(request):
    context = {

    }
    return render(request, 'profiles/home.html', context)


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


@login_required(login_url=reverse_lazy('sign-in'))
def show_profile(request):
    context = {

    }
    return render(request, 'profiles/show-profile.html', context)



class ProfileUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    redirect_field_name = 'profile'

    @staticmethod
    def get(request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'profiles/update-profile.html', context)

    @staticmethod
    def post(request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Success')
            update_session_auth_hash(request, request.user)
            return redirect('update-profile')


class UserRecipesListView(LoginRequiredMixin, SingleObjectMixin, ListView):
    login_url = 'sign-in'
    model = UserModel
    template_name = 'profiles/my-recipes.html'
    object = None
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        return context

    def get_queryset(self):
        return self.object.recipe_set.all()


class UserLikedRecipesListView(LoginRequiredMixin, SingleObjectMixin, ListView):
    login_url = 'sign-in'
    model = UserModel
    template_name = 'profiles/liked-recipes.html'
    object = None
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        return context

    def get_queryset(self):
        return self.object.like_set.all()