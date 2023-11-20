from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect


class LoginUserView(LoginView):
    pass


def logout_user(request):
    logout(request)
    return redirect('login')
