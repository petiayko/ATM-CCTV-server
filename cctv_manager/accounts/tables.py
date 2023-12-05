import django_tables2 as tables
from django.contrib.auth import models
from django.utils.html import format_html

from design.tables import TableStyleMeta


class StaffTable(tables.Table):
    username = tables.Column(verbose_name='Логин')
    first_name = tables.Column(verbose_name='Имя')
    last_name = tables.Column(verbose_name='Фамилия')
    groups = tables.Column(verbose_name='Роль', orderable=False)
    edit = tables.TemplateColumn(template_name='accounts/action_edit.html', verbose_name='', orderable=False)
    delete = tables.TemplateColumn(template_name='accounts/action_delete.html', verbose_name='', orderable=False)

    def render_username(self, value, record):
        if self.request.user.id == record.pk:
            return format_html(f'<strong>{value}</strong>')
        return value

    def render_groups(self, record):
        output = list()
        for group in record.groups.all().values_list('name', flat=True):
            if group == 'O':
                output.append('Оператор')
            elif group == 'LA':
                output.append('Локальный администратор')
            elif group == 'NA':
                output.append('Сетевой администратор')
        return ', '.join(output).capitalize()

    class Meta(TableStyleMeta):
        model = models.User
        fields = 'username', 'first_name', 'last_name', 'groups',
