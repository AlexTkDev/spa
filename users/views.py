from django.shortcuts import render, redirect
from django.views import View
from django.contrib import auth
from users.forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    def get_success_url(self):
        return reverse_lazy('post_list')


class LogoutUser(View):
    def get(self, request):
        auth.logout(request)
        return redirect('post_list')