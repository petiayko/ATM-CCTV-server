from django.db import models


def configuration_default():
    return {
        'ip_address': '192.168.17.19',  # ipv4 camera address
        'prerecord_time': 5,  # prerecord time in secs
        'postrecord_time': 5,  # postrecord time in secs
    }


class Camera(models.Model):
    name = models.CharField(verbose_name='Имя камеры', max_length=20)
    configuration = models.JSONField(verbose_name='Конфигурация камеры', default=configuration_default)

    class Meta:
        ordering = 'name',
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'

    def __str__(self):
        return self.name
