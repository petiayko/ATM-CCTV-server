from django.contrib.auth import logout
from django.shortcuts import redirect, render


def information(request):
    return render(request, 'base/information.html')


def logout_user(request):
    logout(request)
    return redirect('login')
