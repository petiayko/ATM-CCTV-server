import django_tables2 as tables
from django.utils.html import format_html

from . import models
from design.tables import TableStyleMeta


class CamerasTable(tables.Table):
    name = tables.Column(verbose_name='Имя')
    ip_address = tables.Column(verbose_name='IP адрес', orderable=False)
    status = tables.TemplateColumn(template_name='cameras/camera_status.html', verbose_name='Статус', orderable=False)
    detail = tables.TemplateColumn(template_name='cameras/action_detail.html', verbose_name='', orderable=False)

    def render_status(self, record):
        return format_html(f'<div class="d-flex justify-content-between" id="id-status-{record.pk}">'
                           '<strong>Определяется...</strong>'
                           '</div>')

    class Meta(TableStyleMeta):
        model = models.Camera
        fields = 'name', 'ip_address',
        row_attrs = {
            'camera-id': lambda record: record.pk
        }
