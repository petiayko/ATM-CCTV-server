from django.urls import path

from . import views

urlpatterns = [
    path('', views.LiveStreamView.as_view(), name='live_stream'),
    path('<int:pk>', views.get_video_stream, name='video_stream'),
    path('archive/', views.RecordsListView.as_view(), name='records_archive'),
    # path('archive/<int:pk>/edit', views.RecordEditView.as_view(), name='record_edit'),
    # path('archive/<int:pk>/delete', views.record_delete, name='record_delete'),
    # path('archive/<int:pk>/download', views.record_download, name='record_download'),
]
