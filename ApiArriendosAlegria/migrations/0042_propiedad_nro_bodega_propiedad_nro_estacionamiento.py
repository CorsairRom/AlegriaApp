# Generated by Django 4.1.7 on 2023-05-16 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0041_rename_extradepartamento_arriendodepartamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='propiedad',
            name='nro_bodega',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número Bodega'),
        ),
        migrations.AddField(
            model_name='propiedad',
            name='nro_estacionamiento',
            field=models.IntegerField(blank=True, null=True, verbose_name='Número Estacionamiento'),
        ),
    ]
