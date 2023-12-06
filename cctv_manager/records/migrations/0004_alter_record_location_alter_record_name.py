# Generated by Django 4.1.9 on 2023-12-05 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_alter_record_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='location',
            field=models.CharField(max_length=1000, unique=True, verbose_name='Путь к файлу'),
        ),
        migrations.AlterField(
            model_name='record',
            name='name',
            field=models.CharField(max_length=100, unique=True, verbose_name='Имя записи'),
        ),
    ]
