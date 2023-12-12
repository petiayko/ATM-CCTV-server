from django import forms

from cctv_manager.cameras import models


class CameraAddForm(forms.ModelForm):
    name = forms.CharField(
        label='Имя камеры',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    ip_address = forms.CharField(
        label='IP адрес',
        strip=True,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': ''
        }),
    )

    prerecord_time_sec = forms.IntegerField(
        label='Время предзаписи, сек',
        help_text='Длительность сохраняемого фрагмента до начала активности в кадре',
        min_value=0,
        #step_size=1,
        initial=5,
        widget=forms.NumberInput(attrs={
            'placeholder': ''
        }),
    )

    postrecord_time_sec = forms.IntegerField(
        label='Время постзаписи, сек',
        help_text='Длительность сохраняемого фрагмента после окончания активности в кадре',
        min_value=0,
        #step_size=1,
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': ''
        }),
    )

    video_length_min = forms.IntegerField(
        label='Время предзаписи, мин',
        help_text='Максимальная длительность сохраняемого видео',
        min_value=1,
        #step_size=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'placeholder': ''
        }),
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

    class Meta:
        model = models.Camera
        fields = 'name', 'ip_address', 'prerecord_time_sec', 'postrecord_time_sec', 'video_length_min'
