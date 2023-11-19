from django.db import models


class Record(models.Model):
    name = models.CharField(verbose_name='Имя записи', max_length=20)
    location = models.CharField(verbose_name='Путь к файлу', max_length=1000)
    timestamp = models.TimeField(verbose_name='Время записи', auto_now_add=True)
    camera = models.ForeignKey(to='cameras.Camera', verbose_name='Камера', related_name='record_camera_match',
                               on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        ordering = 'timestamp', 'name',
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.name
