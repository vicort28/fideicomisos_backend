# Generated by Django 4.1.7 on 2023-12-07 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0020_alter_prestamo_cantidad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gastosfunerarios',
            name='esposo',
        ),
        migrations.RemoveField(
            model_name='gastosfunerarios',
            name='hijo',
        ),
        migrations.RemoveField(
            model_name='gastosfunerarios',
            name='madre',
        ),
        migrations.RemoveField(
            model_name='gastosfunerarios',
            name='padre',
        ),
        migrations.AddField(
            model_name='gastosfunerarios',
            name='parentesco',
            field=models.CharField(choices=[('padre', 'Padre'), ('madre', 'Madre'), ('esposo', 'Esposo'), ('hijo', 'Hijo')], max_length=10, null=True),
        ),
    ]
