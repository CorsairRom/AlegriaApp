# Generated by Django 4.1.7 on 2023-06-04 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0063_alter_cuenta_rut_tercero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propietario',
            name='pctje_cobro_honorario',
            field=models.FloatField(default=7, verbose_name='Porcentaje Cobro Propietario'),
        ),
    ]