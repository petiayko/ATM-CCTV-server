import cv2
import datetime
import os
from django.db import models

from cctv_manager.utils.rbac_scripts import is_user_able


class RecordManager(models.Manager):
    def for_user(self, user, action=None):
        if action is None:
            return self.get_queryset()
        if is_user_able(user, 'R', action):
            return self.get_queryset()
        return Record.objects.none()


class Record(models.Model):
    name = models.CharField(verbose_name='Имя записи', unique=True, max_length=100)
    location = models.CharField(verbose_name='Путь к файлу', unique=True, max_length=1000)
    timestamp = models.DateTimeField(verbose_name='Время записи', auto_now_add=True)
    camera = models.ForeignKey(to='cameras.Camera', verbose_name='Камера', related_name='record_camera_match',
                               on_delete=models.SET_NULL, blank=True, null=True)

    objects = RecordManager()

    class Meta:
        ordering = 'timestamp', 'name',
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name

    @property
    def record_timestamp(self):
        if not os.path.exists(self.location) or self.timestamp is None:
            return None
        timestamp = self.timestamp + datetime.timedelta(hours=3)
        return timestamp.strftime('%d.%m.%Y %H:%M:%S')

    @property
    def record_size(self):
        if not os.path.exists(self.location):
            return None
        return f'{round(os.stat(self.location).st_size / (1024 * 1024))} Мб'

    @property
    def record_duration(self):
        if not os.path.exists(self.location):
            return None
        video = cv2.VideoCapture(self.location)
        duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
        return f'{round(duration / 60)} мин {round(duration % 60)} с'
