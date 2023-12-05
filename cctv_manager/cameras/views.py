from typing import Any, Dict

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django_tables2 import SingleTableView
from django.shortcuts import get_object_or_404

from . import forms, models, tables
from utils.network_scripts import check_ping
from utils.rbac_scripts import is_user_able


class CameraViewFilterMixin:
    def get_queryset(self):
        return models.Camera.objects.for_user(self.request.user)


class CameraChangeFilterMixin:
    def get_queryset(self):
        return models.Camera.objects.for_user(self.request.user, action='C')


class CameraAddFilterMixin:
    def get_queryset(self):
        return models.Camera.objects.for_user(self.request.user, action='A')


class CameraDeleteFilterMixin:
    def get_queryset(self):
        return models.Camera.objects.for_user(self.request.user, action='D')


class CamerasListView(CameraViewFilterMixin, SingleTableView):
    model = models.Camera
    template_name = 'cameras/list.html'
    table_class = tables.CamerasTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_able_add': is_user_able(self.request.user, 'C', 'A'),
        })
        return context

    def get_queryset(self):
        fields = ['name', 'ip_address']
        return super().get_queryset().only(*fields)


class CameraDetailView(CameraViewFilterMixin, DetailView):
    model = models.Camera
    template_name = 'cameras/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        camera = self.object
        context.update({
            'fields': camera.get_fields().items(),
            'is_able_edit': is_user_able(self.request.user, 'C', 'C'),
            'is_able_delete': is_user_able(self.request.user, 'C', 'D'),
            'is_able_reload': is_user_able(self.request.user, 'C', 'R'),
        })
        return context


class CameraAddView(CameraAddFilterMixin, CreateView):
    model = models.Camera
    template_name = 'cameras/create.html'
    form_class = forms.CameraAddForm

    def get_success_url(self):
        return reverse_lazy('camera_detail', kwargs={'pk': self.object.id})


class CameraEditView(CameraChangeFilterMixin, UpdateView):
    model = models.Camera
    template_name = 'cameras/edit.html'
    fields = ['name', 'ip_address', 'prerecord_time_sec', 'postrecord_time_sec', 'video_length_min']

    def get_success_url(self):
        return reverse_lazy('camera_detail', kwargs={'pk': self.object.id})


def camera_delete(request, pk):
    if not is_user_able(request.user, 'C', 'D'):
        return HttpResponse(status=404)
    camera = get_object_or_404(models.Camera, pk=pk)
    camera.delete()
    return HttpResponseRedirect(reverse_lazy('cameras_list'))


def ping_camera(request, pk):
    camera = get_object_or_404(models.Camera, pk=pk)
    try:
        if check_ping(camera.ip_address):
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})
    except Exception as e:
        return JsonResponse({'success': False}, status=500)
