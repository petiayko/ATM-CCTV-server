from django import forms
from django.contrib.auth import models


class StaffAddForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    first_name = forms.CharField(
        label='Имя',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    last_name = forms.CharField(
        label='Фамилия',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    password = forms.CharField(
        label='Пароль',
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': ''
        })
    )

    groups = forms.ChoiceField(
        label='Роль',
        required=True,
        widget=forms.RadioSelect,
        choices=[(1, 'Сетевой администратор'), (2, 'Локальный администратор'), (3, 'Оператор')],
        initial=3,
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_user = models.User.objects.create_user(username=instance.username, password=instance.password)
        new_user.first_name = instance.first_name
        new_user.last_name = instance.last_name
        new_user.save()
        models.Group.objects.get(id=self.cleaned_data['groups']).user_set.add(new_user)
        return instance

    class Meta:
        model = models.User
        fields = 'username', 'first_name', 'last_name', 'password',


class StaffEditForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    last_name = forms.CharField(
        label='Фамилия',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    groups = forms.ChoiceField(
        label='Роль',
        required=True,
        widget=forms.RadioSelect,
        choices=[(1, 'Сетевой администратор'), (2, 'Локальный администратор'), (3, 'Оператор')],
        initial=3,
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        for group_id in instance.groups.all().values_list('id', flat=True):
            models.Group.objects.get(id=group_id).user_set.remove(instance)
        models.Group.objects.get(id=self.cleaned_data['groups']).user_set.add(instance)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.User
        fields = 'first_name', 'last_name',


class StaffChangePasswordForm(forms.ModelForm):
    password = forms.CharField(
        label='Новый пароль',
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': ''
        })
    )

    password_confirm = forms.CharField(
        label='Подтвердите пароль',
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': ''
        })
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.User
        fields = 'password',
