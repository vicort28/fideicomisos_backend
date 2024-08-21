# Generated by Django 4.1.7 on 2024-08-16 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0065_rename_fecha_nacimiento_empleado_fechanacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='correo',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='curp',
            field=models.CharField(blank=True, max_length=18),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='direccion',
            field=models.TextField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='domicilio',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='rfc',
            field=models.CharField(blank=True, max_length=13),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='unidad',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
