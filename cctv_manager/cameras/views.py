from django_tables2 import SingleTableView

from . import models


class CamerasListView(SingleTableView):
    model = models.Camera
    template_name = 'cameras/list.html'
    table_class = ''
