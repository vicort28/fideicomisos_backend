# Generated by Django 4.1.7 on 2024-04-22 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0034_remove_gastosfunerarios_parentesco_delete_parentesco_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parentesco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Padre', 'Padre'), ('Madre', 'Madre'), ('Esposo', 'Esposo'), ('Hijo', 'Hijo')], max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='gastosfunerarios',
            name='parentesco',
        ),
        migrations.AddField(
            model_name='gastosfunerarios',
            name='parentesco',
            field=models.ManyToManyField(to='fideicomisos_backend.parentesco'),
        ),
    ]
