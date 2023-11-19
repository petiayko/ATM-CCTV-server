# Generated by Django 4.1.9 on 2023-11-19 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cameras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Имя записи')),
                ('location', models.CharField(max_length=1000, verbose_name='Путь к файлу')),
                ('timestamp', models.TimeField(auto_now_add=True, verbose_name='Время записи')),
                ('camera', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='record_camera_match', to='cameras.camera', verbose_name='Камера')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
                'ordering': ('timestamp', 'name'),
            },
        ),
    ]