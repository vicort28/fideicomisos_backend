# Generated by Django 4.1.7 on 2024-08-13 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0058_rename_field_segurovida_porcentaje'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='segurovida',
            name='domicilio',
        ),
        migrations.RemoveField(
            model_name='segurovida',
            name='telefono',
        ),
    ]