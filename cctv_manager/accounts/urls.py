from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    # path('profile/', views.profile, name='profile'),
    path('', include('django.contrib.auth.urls')),
]
