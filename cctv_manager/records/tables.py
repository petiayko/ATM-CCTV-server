import django_tables2 as tables

from . import models
from design.tables import TableStyleMeta


class LiveStreamTable(tables.Table):
    class Meta:
        pass


class ArchiveTable(tables.Table):
    name = tables.Column(verbose_name='Название')
    timestamp = tables.Column(verbose_name='Время записи')
    camera = tables.Column(verbose_name='Имя камеры')
    edit = tables.TemplateColumn(template_name='records/record_edit.html', verbose_name='', orderable=False)
    delete = tables.TemplateColumn(template_name='records/record_delete.html', verbose_name='', orderable=False)
    download = tables.TemplateColumn(template_name='records/record_download.html', verbose_name='', orderable=False)

    class Meta(TableStyleMeta):
        model = models.Record
        fields = 'name', 'timestamp',
        row_attrs = {
            'record-id': lambda record: record.pk
        }
