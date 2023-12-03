from bootstrap_modal_forms.forms import BSModalModelForm
from django import forms

from . import models


class RecordEditForm(BSModalModelForm):
    class Meta:
        model = models.Record
        fields = 'name',
        widgets = {
            'name': forms.TextInput()
        }
