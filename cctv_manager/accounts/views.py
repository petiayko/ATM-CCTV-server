from django.contrib.auth import logout, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django_tables2 import SingleTableView

from cctv_manager.accounts import tables, forms
from cctv_manager.utils.rbac_scripts import is_user_able


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
            'is_able_edit': is_user_able(self.request.user, 'U', 'C'),
        })
        return context

    def get_queryset(self):
        fields = ['username', 'first_name', 'last_name', 'groups']
        return super().get_queryset().only(*fields)


class StaffAddView(CreateView):
    model = models.User
    template_name = 'accounts/create.html'
    form_class = forms.StaffAddForm

    def get(self, request, *args, **kwargs):
        if is_user_able(request.user, 'U', 'A'):
            return super().get(args, kwargs)
        return HttpResponseRedirect(reverse_lazy('staff_list'))

    def get_success_url(self):
        return reverse_lazy('staff_list')


class StaffEditView(UpdateView):
    model = models.User
    template_name = 'accounts/edit.html'
    form_class = forms.StaffEditForm

    def get(self, request, *args, **kwargs):
        if is_user_able(request.user, 'U', 'C'):
            return super().get(args, kwargs)
        return HttpResponseRedirect(reverse_lazy('staff_list'))

    def get_success_url(self):
        return reverse_lazy('staff_list')


class StaffChangePasswordView(UpdateView):
    model = models.User
    template_name = 'accounts/edit_password.html'
    form_class = forms.StaffChangePasswordForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):
        if request.user.id == kwargs.get('pk'):
            return super().get(args, kwargs)
        return HttpResponseRedirect(reverse_lazy('staff_list'))

    def get_success_url(self):
        return reverse_lazy('staff_list')


def staff_delete(request, pk):
    if not is_user_able(request.user, 'U', 'D'):
        return HttpResponse(status=404)
    user = get_object_or_404(models.User, pk=pk)
    user.delete()
    return HttpResponseRedirect(reverse_lazy('staff_list'))
