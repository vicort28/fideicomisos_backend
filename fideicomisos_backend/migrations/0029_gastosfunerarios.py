# Generated by Django 4.1.7 on 2024-04-22 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fideicomisos_backend', '0028_delete_gastosfunerarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='GastosFunerarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parentesco', models.CharField(choices=[('Padre', 'Padre'), ('Madre', 'Madre'), ('Esposo', 'Esposo'), ('Hijo', 'Hijo')], max_length=10, null=True)),
                ('empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gastos_funerarios', to='fideicomisos_backend.empleado')),
            ],
        ),
    ]
