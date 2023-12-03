import cv2
import os
import datetime
from django.db import models


class Record(models.Model):
    name = models.CharField(verbose_name='Имя записи', max_length=100)
    location = models.CharField(verbose_name='Путь к файлу', max_length=1000)
    timestamp = models.DateTimeField(verbose_name='Время записи', auto_now_add=True)
    camera = models.ForeignKey(to='cameras.Camera', verbose_name='Камера', related_name='record_camera_match',
                               on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = 'timestamp', 'name',
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name

    @property
    def record_timestamp(self):
        if not os.path.exists(self.location) or self.timestamp is None:
            return 'не удалось определить.'
        timestamp = self.timestamp + datetime.timedelta(hours=3)
        return timestamp.strftime('%d.%m.%Y %H:%M:%S')

    @property
    def record_size(self):
        if not os.path.exists(self.location):
            return 'не удалось определить.'
        return f'{round(os.stat(self.location).st_size / (1024 * 1024))} Мб'

    @property
    def record_duration(self):
        if not os.path.exists(self.location):
            return 'не удалось определить.'
        video = cv2.VideoCapture(self.location)
        duration = video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
        return f'{round(duration / 60)} мин {round(duration % 60)} с'

    @property
    def record_preview(self):
        if not os.path.exists(self.location):
            return 'не удалось определить.'
        return '124'
