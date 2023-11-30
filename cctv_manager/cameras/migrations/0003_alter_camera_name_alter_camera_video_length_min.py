# Generated by Django 4.1.9 on 2023-11-30 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cameras', '0002_alter_camera_ip_address_alter_camera_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Имя камеры'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='video_length_min',
            field=models.PositiveIntegerField(default=1, verbose_name='Длительность видео, мин'),
        ),
    ]
