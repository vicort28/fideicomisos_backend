# Generated by Django 4.1.7 on 2024-04-24 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0040_remove_gastosfunerarios_parentesco'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gastosfunerarios',
            name='parentescos',
        ),
        migrations.AddField(
            model_name='gastosfunerarios',
            name='esposo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gastosfunerarios',
            name='hijo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gastosfunerarios',
            name='madre',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gastosfunerarios',
            name='padre',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Parentesco',
        ),
    ]
