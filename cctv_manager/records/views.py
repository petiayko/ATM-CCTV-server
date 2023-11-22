from django_tables2 import SingleTableView

from . import models, tables


class LiveStreamView(SingleTableView):
    model = models.Record
    template_name = 'records/live_stream.html'
    table_class = tables.LiveStreamTable


class RecordsListView(SingleTableView):
    model = models.Record
    template_name = 'records/list.html'
    table_class = tables.ArchiveTable
