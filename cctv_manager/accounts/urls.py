from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('information/', views.information, name='information'),
    path('', include('django.contrib.auth.urls')),
]
