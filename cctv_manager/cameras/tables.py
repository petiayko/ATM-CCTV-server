import django_tables2 as tables
from django.utils.html import format_html

from . import models
from design.tables import TableStyleMeta
from utils.network_scripts import check_ping


class CamerasTable(tables.Table):
    name = tables.Column(verbose_name='Имя')
    ip_address = tables.Column(verbose_name='IP адрес', orderable=False)
    status = tables.TemplateColumn(template_name='cameras/camera_status.html', verbose_name='Статус', orderable=False)
    detail = tables.TemplateColumn(template_name='cameras/camera_detail.html', verbose_name='', orderable=False)

    def render_status(self, record):
        def get_html_status(colour, status):
            return format_html(
                '<div class="d-flex justify-content-between">'
                f'<strong style="color: {colour};">{status}</strong>'
                '</div>')

        camera = models.Camera.objects.get(id=record.pk)
        if check_ping(camera.ip_address):
            return get_html_status('green', 'Доступна')
        return get_html_status('red', 'Недоступна')

    class Meta(TableStyleMeta):
        model = models.Camera
        fields = 'name', 'ip_address',
        row_attrs = {
            'camera-id': lambda record: record.pk
        }
