from django.urls import path

from cctv_manager.records import views

urlpatterns = [
    path('', views.LiveStreamView.as_view(), name='live_stream'),
    path('archive/', views.RecordsListView.as_view(), name='records_list'),
    path('archive/<int:pk>/edit', views.record_edit, name='record_edit'),
    path('archive/<int:pk>/delete', views.record_delete, name='record_delete'),
    path('archive/<int:pk>/download', views.record_download, name='record_download'),
    path('archive/<int:pk>/preview', views.record_preview, name='record_preview'),
]
