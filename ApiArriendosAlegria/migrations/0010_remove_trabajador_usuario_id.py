# Generated by Django 4.1.7 on 2023-06-18 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0009_alter_detallearriendo_toca_reajuste'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trabajador',
            name='usuario_id',
        ),
    ]