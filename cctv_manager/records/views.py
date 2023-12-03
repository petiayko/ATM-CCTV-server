import os
from bootstrap_modal_forms.generic import BSModalUpdateView
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django_tables2 import SingleTableView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from . import models, tables, forms
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


class RecordsListView(TemplateView):
    template_name = 'records/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'search' in self.request.GET:
            template = self.request.GET['search']
            context['search'] = template
            records = models.Record.objects.filter(
                Q(name__istartswith=template) | Q(name__iendswith=template) | Q(name__contains=template))
        else:
            records = models.Record.objects.all()

        if 'sort' not in self.request.GET:
            context['records'] = records.order_by('-timestamp')
            return context
        if 'name' in self.request.GET['sort']:
            context['sort'] = 2
            records = records.order_by('name')
        if '-name' in self.request.GET['sort']:
            context['sort'] = 3
            records = records.order_by('-name')
        if 'timestamp' in self.request.GET['sort']:
            context['sort'] = 1
            records = records.order_by('timestamp')
        if '-timestamp' in self.request.GET['sort']:
            context['sort'] = 0
            records = records.order_by('-timestamp')
        context['records'] = records
        return context


def record_edit(request, pk):
    record = get_object_or_404(models.Record, pk=pk)
    return HttpResponseRedirect(reverse_lazy('records_list'))


# class RecordEditView(BSModalUpdateView):
#     model = models.Record
#     template_name = 'records/record_edit.html'
#     form_class = forms.RecordEditForm
#
#     def get_success_url(self):
#         return reverse_lazy('records_list')


def record_delete(request, pk):
    record = get_object_or_404(models.Record, pk=pk)
    record.delete()
    return HttpResponseRedirect(reverse_lazy('records_list'))


def record_download(request, pk):
    record = get_object_or_404(models.Record, pk=pk)
    if os.path.exists(record.location):
        return FileResponse(open(record.location, 'rb'), as_attachment=True, filename=f'{record.name}.mp4')
    raise Http404('File not found')
