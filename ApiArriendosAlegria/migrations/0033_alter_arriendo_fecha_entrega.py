# Generated by Django 4.1.7 on 2023-05-15 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0032_alter_arriendo_periodo_reajuste'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arriendo',
            name='fecha_entrega',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha entrega arriendo'),
        ),
    ]