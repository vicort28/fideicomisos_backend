# Generated by Django 4.1.7 on 2024-08-12 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0050_remove_prestamo_numero_empleado_prestamo_empleado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='nombre',
            new_name='nombres',
        ),
    ]
