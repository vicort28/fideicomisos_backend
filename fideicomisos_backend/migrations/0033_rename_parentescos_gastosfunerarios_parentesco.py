# Generated by Django 4.1.7 on 2024-04-22 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0032_parentesco_remove_gastosfunerarios_parentesco_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gastosfunerarios',
            old_name='parentescos',
            new_name='parentesco',
        ),
    ]
