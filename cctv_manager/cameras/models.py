from django.db import models


class Camera(models.Model):
    name = models.CharField(verbose_name='Имя камеры', max_length=20, null=False, blank=False)
    ip_address = models.CharField(verbose_name='IP адрес камеры', max_length=15, null=False, blank=False)
    prerecord_time_sec = models.PositiveIntegerField(verbose_name='Время предзаписи, сек', default=5, null=False,
                                                     blank=False)
    postrecord_time_sec = models.PositiveIntegerField(verbose_name='Время постзаписи, сек', default=0, null=False,
                                                      blank=False)
    video_length_min = models.PositiveIntegerField(verbose_name='Длительность видео, мин', default=10, null=False,
                                                   blank=False)

    class Meta:
        ordering = 'name',
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'

    def __str__(self):
        return self.name

    def get_fields(self):
        dct = dict()

        fields = ['name', 'ip_address', 'prerecord_time_sec', 'postrecord_time_sec', 'video_length_min']
        fields_to_hide_if_none = []
        fields_to_replace_if_none = {}
        fields_boolean = []
        for field in fields:
            field_value = getattr(self, field)
            if field in fields_to_hide_if_none and not field_value:
                continue
            if field in fields_to_replace_if_none and not field_value:
                field_value = fields_to_replace_if_none[field]
            if field in fields_boolean:
                field_value = 'Да' if field_value else 'Нет'
            dct[self._meta.get_field(field).verbose_name] = field_value
        return dct
