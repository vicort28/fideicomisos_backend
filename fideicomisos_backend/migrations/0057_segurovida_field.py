# Generated by Django 4.1.7 on 2024-08-13 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0056_remove_segurovida_beneficiario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='segurovida',
            name='field',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Ingresa el porcentaje (0.00 - 100.00)', max_digits=5),
        ),
    ]