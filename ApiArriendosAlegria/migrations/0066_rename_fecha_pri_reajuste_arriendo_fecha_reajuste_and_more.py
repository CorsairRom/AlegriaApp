# Generated by Django 4.1.7 on 2023-06-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0065_rename_fecha_pri_ajuste_arriendo_fecha_pri_reajuste_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arriendo',
            old_name='fecha_pri_reajuste',
            new_name='fecha_reajuste',
        ),
        migrations.AddField(
            model_name='arriendo',
            name='valor_arriendo',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Valor Arriendo'),
        ),
    ]
