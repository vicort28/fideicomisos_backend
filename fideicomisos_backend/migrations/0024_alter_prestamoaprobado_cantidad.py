# Generated by Django 4.1.7 on 2023-12-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0023_alter_prestamo_empleado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamoaprobado',
            name='cantidad',
            field=models.CharField(max_length=10),
        ),
    ]