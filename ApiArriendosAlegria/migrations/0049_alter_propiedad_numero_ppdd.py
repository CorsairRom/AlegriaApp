# Generated by Django 4.1.7 on 2023-05-25 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0048_alter_cuenta_rut_tercero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propiedad',
            name='numero_ppdd',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Número Propiedad'),
        ),
    ]
