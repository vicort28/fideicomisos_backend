# Generated by Django 4.1.7 on 2024-08-09 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0044_alter_prestamo_numero_empleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='numero_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestamos', to='fideicomisos_backend.empleado'),
        ),
    ]
