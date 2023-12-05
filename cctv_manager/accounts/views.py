from django.contrib.auth import logout, models
from django.shortcuts import redirect, render
from django_tables2 import SingleTableView

from . import tables
from utils.rbac_scripts import is_user_able


def information(request):
    return render(request, 'base/information.html')


def logout_user(request):
    logout(request)
    return redirect('login')


class StaffListView(SingleTableView):
    model = models.User
    template_name = 'accounts/list.html'
    table_class = tables.StaffTable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'is_able_add': is_user_able(self.request.user, 'U', 'A'),
            'is_able_delete': is_user_able(self.request.user, 'U', 'D'),
        })
        return context

    def get_queryset(self):
        fields = ['username', 'first_name', 'last_name', 'groups']
        return super().get_queryset().only(*fields)


def staff_delete(request, pk):
    pass
