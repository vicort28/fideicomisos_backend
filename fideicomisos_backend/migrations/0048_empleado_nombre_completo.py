# Generated by Django 4.1.7 on 2024-08-09 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0047_empleado_fecha_ingreso_empleado_fecha_nacimiento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='nombre_completo',
            field=models.CharField(default='', max_length=80),
        ),
    ]
