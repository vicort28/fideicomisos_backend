# Generated by Django 4.1.7 on 2023-12-07 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0013_remove_prestamo_cantidad1_remove_prestamo_cantidad2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prestamoaprobado',
            old_name='cantidad1',
            new_name='cantidad',
        ),
        migrations.RemoveField(
            model_name='prestamoaprobado',
            name='cantidad2',
        ),
    ]
