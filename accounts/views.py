from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import LoginForm, RegisterForm


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('posts_list_url'))
        form = LoginForm()
        return render(request, 'accounts/login.html', context={'login_form': form})

    def post(self, request):
        bound_form = LoginForm(request.POST)

        if bound_form.is_valid():
            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('posts_list_url'))

        return render(request, 'accounts/login.html', context={'login_form': bound_form})


class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'accounts/register.html', context={'register_form': register_form})

    def post(self, request):

        bound_form = RegisterForm(request.POST)
        if bound_form.is_valid():
            username = bound_form.cleaned_data.get('username')
            password = bound_form.cleaned_data.get('password')
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect(reverse('posts_list_url'))
        return render(request, 'accounts/registration.html', context={'register_form': bound_form})


def logout_view(request):
    logout(request)
    return redirect(reverse('login_url'))