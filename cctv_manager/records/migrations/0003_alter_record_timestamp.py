# Generated by Django 4.1.9 on 2023-12-03 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_alter_record_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время записи'),
        ),
    ]
