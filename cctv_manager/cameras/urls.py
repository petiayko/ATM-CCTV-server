from django.urls import path

from . import views

urlpatterns = [
    path('', views.CamerasListView.as_view(), name='cameras_list'),
    path('add', views.CameraAddView.as_view(), name='camera_add'),
    path('<int:pk>/detail', views.CameraDetailView.as_view(), name='camera_detail'),
    path('<int:pk>/edit', views.CameraEditView.as_view(), name='camera_edit'),
    path('<int:pk>/delete', views.camera_delete, name='camera_delete'),
]
