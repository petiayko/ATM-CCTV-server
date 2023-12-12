import threading
import cv2
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from django_tables2 import SingleTableView
from django.views.decorators import gzip

from . import forms, models, tables
from utils.network_scripts import check_ping
from utils.rbac_scripts import is_user_able


class CameraViewFilterMixin:
    def get_queryset(self):
        return models.Camera.objects.for_user(self.request.user)


class CameraChangeFilterMixin:
    def get_queryset(self):
        return models.Camera.objects.for_user(self.request.user, action='C')


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


class CameraAddView(CreateView):
    model = models.Camera
    template_name = 'cameras/create.html'
    form_class = forms.CameraAddForm

    def get(self, request, *args, **kwargs):
        if is_user_able(request.user, 'C', 'A'):
            return super().get(args, kwargs)
        return HttpResponseRedirect(reverse_lazy('cameras_list'))

    def get_success_url(self):
        return reverse_lazy('camera_detail', kwargs={'pk': self.object.id})


class CameraEditView(CameraChangeFilterMixin, UpdateView):
    model = models.Camera
    template_name = 'cameras/edit.html'
    fields = ['name', 'prerecord_time_sec', 'postrecord_time_sec', 'video_length_min']

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


class VideoCamera(object):
    def __init__(self, camera_ip):
        self.video = cv2.VideoCapture(camera_ip)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def get_camera_ip(pk, hd_quality=True):
    camera = get_object_or_404(models.Camera, id=pk)
    return f'rtsp://{camera.ip_address}/live/{"ch00_1" if hd_quality else "ch00_0"}'


# надо реализовать функцию получения всех ip
def get_all_ips():
    ip = ['rtsp:\\first', 'rtsp:\\second']
    return ip


# надо добавить куда рендериться будет(либо будет на отдельной страничке как сейчас)
@gzip.gzip_page
def show_camera_stream(request, pk):
    try:
        return StreamingHttpResponse(gen(VideoCamera(get_camera_ip(pk))),
                                     content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        pass
    # надо отобразить страничку где стрим с камеры
    # return render(request, 'cameras/stream.html')
    return None
