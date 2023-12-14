import cv2
import os
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from . import models
from cameras.models import Camera
from utils.rbac_scripts import is_user_able


class RecordViewFilterMixin:
    def get_queryset(self):
        return models.Record.objects.for_user(self.request.user)


class LiveStreamView(RecordViewFilterMixin, TemplateView):
    template_name = 'records/live_stream.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = Camera.objects.all()
        context['cameras'] = [cameras[i:i + 2] for i in range(0, len(cameras), 2)]
        if len(cameras) and len(context['cameras'][-1]) == 1:
            context['cameras'][-1].append(None)
        context['is_able_add'] = is_user_able(self.request.user, 'R', 'C')
        return context


class RecordsListView(RecordViewFilterMixin, TemplateView):
    template_name = 'records/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_able_edit': is_user_able(self.request.user, 'R', 'E'),
            'is_able_delete': is_user_able(self.request.user, 'R', 'D'),
            'is_able_download': is_user_able(self.request.user, 'R', 'A'),
        })
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
            context['sort'] = 3
            records = records.order_by('name')
        if '-name' in self.request.GET['sort']:
            context['sort'] = 2
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
    if not is_user_able(request.user, 'R', 'E'):
        return HttpResponse(status=404)
    if request.method == 'GET':
        return HttpResponse(status=405)
    record = get_object_or_404(models.Record, pk=pk)
    record.name = request.POST.get('new_name', record.name)
    record.save()
    return redirect('records_list')


def record_delete(request, pk):
    if not is_user_able(request.user, 'R', 'D'):
        return HttpResponse(status=404)
    record = get_object_or_404(models.Record, pk=pk)
    record.delete()
    return HttpResponseRedirect(reverse_lazy('records_list'))


def record_download(request, pk):
    if not is_user_able(request.user, 'R', 'A'):
        return HttpResponse(status=404)
    record = get_object_or_404(models.Record, pk=pk)
    if os.path.exists(record.location):
        return FileResponse(open(record.location, 'rb'), as_attachment=True, filename=f'{record.name}.mp4')
    raise Http404('File not found')


def record_preview(request, pk):
    record = get_object_or_404(models.Record, pk=pk)
    if not os.path.exists(record.location):
        return HttpResponse(status=404)

    f = cv2.VideoCapture(record.location)
    ret, frame = f.read()
    f.release()
    resize = cv2.resize(frame, (490, 267))
    return HttpResponse(cv2.imencode('.jpg', resize)[1].tostring(), content_type='image/jpg')
