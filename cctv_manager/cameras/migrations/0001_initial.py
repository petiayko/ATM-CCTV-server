# Generated by Django 4.1.9 on 2023-11-21 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя камеры')),
                ('ip_address', models.CharField(max_length=15, verbose_name='IP адрес камеры')),
                ('prerecord_time_sec', models.PositiveIntegerField(default=5, verbose_name='Время предзаписи, сек')),
                ('postrecord_time_sec', models.PositiveIntegerField(default=0, verbose_name='Время постзаписи, сек')),
                ('video_length_min', models.PositiveIntegerField(default=10, verbose_name='Длительность видео, мин')),
            ],
            options={
                'verbose_name': 'Камера',
                'verbose_name_plural': 'Камеры',
                'ordering': ('name',),
            },
        ),
    ]
