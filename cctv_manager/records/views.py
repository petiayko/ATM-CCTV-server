from django.http import HttpResponse, StreamingHttpResponse
from django_tables2 import SingleTableView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

from . import models, tables
from cameras.models import Camera
from utils.network_scripts import rtsp_connection, get_stream_content


class LiveStreamView(TemplateView):
    template_name = 'records/live_stream.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = Camera.objects.all()
        context['cameras'] = [cameras[i:i + 2] for i in range(0, len(cameras), 2)]
        if len(cameras) and len(context['cameras'][-1]) == 1:
            context['cameras'][-1].append(None)
        return context


def get_video_stream(request, pk):
    camera = get_object_or_404(Camera, pk=pk)
    # return StreamingHttpResponse(get_stream_content(camera.ip_address, 'ch00_1'))
    return HttpResponse(rtsp_connection(camera.ip_address, 'ch00_1'),
                        content_type='multipart/x-mixed-replace; boundary=frame')


class RecordsListView(SingleTableView):
    model = models.Record
    template_name = 'records/list.html'
    table_class = tables.ArchiveTable
