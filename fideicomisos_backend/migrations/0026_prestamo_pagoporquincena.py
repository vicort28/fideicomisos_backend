# Generated by Django 4.1.7 on 2024-01-22 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0025_prestamo_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='pagoporquincena',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
