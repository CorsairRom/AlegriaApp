# Generated by Django 4.1.7 on 2023-05-11 21:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ApiArriendosAlegria', '0027_remove_detallearriendo_propiedad_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arriendo',
            old_name='arrendatario_id',
            new_name='arrendatario',
        ),
        migrations.RenameField(
            model_name='arriendo',
            old_name='propiedad_id',
            new_name='propiedad',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='banco_id',
            new_name='banco',
        ),
        migrations.RenameField(
            model_name='cuenta',
            old_name='tipocuenta_id',
            new_name='tipocuenta',
        ),
        migrations.RenameField(
            model_name='detallearriendo',
            old_name='arriendo_id',
            new_name='arriendo',
        ),
        migrations.RenameField(
            model_name='gastocomun',
            old_name='arriendo_id',
            new_name='arriendo',
        ),
        migrations.RenameField(
            model_name='personalidadjuridica',
            old_name='propietario_id',
            new_name='propietario',
        ),
        migrations.RenameField(
            model_name='propiedad',
            old_name='propietario_id',
            new_name='propietario',
        ),
        migrations.RenameField(
            model_name='propiedad',
            old_name='tipopropiedad_id',
            new_name='tipopropiedad',
        ),
        migrations.RenameField(
            model_name='serviciosextras',
            old_name='arriendo_id',
            new_name='arriendo',
        ),
    ]
