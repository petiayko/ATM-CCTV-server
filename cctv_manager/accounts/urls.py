from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('information/', views.information, name='information'),
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/add', views.StaffAddView.as_view(), name='staff_add'),
    path('staff/<int:pk>/delete', views.staff_delete, name='staff_delete'),
    path('staff/<int:pk>/edit', views.StaffEditView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/password', views.StaffChangePasswordView.as_view(), name='staff_change_password'),
    path('', include('django.contrib.auth.urls')),
]
