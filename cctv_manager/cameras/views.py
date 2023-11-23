from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django_tables2 import SingleTableView
from django.shortcuts import get_object_or_404

from . import forms, models, tables
from utils.network_scripts import check_ping


class CamerasListView(SingleTableView):
    model = models.Camera
    template_name = 'cameras/list.html'
    table_class = tables.CamerasTable

    def get_queryset(self):
        fields = ['name', 'ip_address']
        return super().get_queryset().only(*fields)


class CameraDetailView(DetailView):
    model = models.Camera
    template_name = 'cameras/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        camera = self.object
        context.update({
            'fields': camera.get_fields().items(),
            'status': check_ping(camera.ip_address),
        })
        return context


class CameraAddView(CreateView):
    model = models.Camera
    template_name = 'cameras/create.html'
    form_class = forms.CameraAddForm

    def get_success_url(self):
        return reverse_lazy('camera_detail', kwargs={'pk': self.object.id})


class CameraEditView(UpdateView):
    model = models.Camera
    template_name = 'cameras/edit.html'
    fields = ['name', 'ip_address', 'prerecord_time_sec', 'postrecord_time_sec', 'video_length_min']

    def get_success_url(self):
        return reverse_lazy('camera_detail', kwargs={'pk': self.object.id})


def camera_delete(request, pk):
    camera = get_object_or_404(models.Camera, pk=pk)
    camera.delete()
    return HttpResponseRedirect(reverse_lazy('cameras_list'))
