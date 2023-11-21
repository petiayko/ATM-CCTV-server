from django.urls import path

from . import views

urlpatterns = [
    path('', views.CamerasListView.as_view(), name='cameras_list'),
]
