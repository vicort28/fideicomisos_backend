# Generated by Django 4.1.7 on 2023-11-07 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0005_segurovida'),
    ]

    operations = [
        migrations.AddField(
            model_name='segurovida',
            name='empleado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='fideicomisos_backend.empleado'),
        ),
    ]
