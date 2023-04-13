# Generated by Django 4.1.7 on 2023-04-12 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrendatario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_arr', models.CharField(max_length=12, unique=True, verbose_name='Rut Arrendatario')),
                ('pri_nom_arr', models.CharField(max_length=50, verbose_name='Primer Nombre')),
                ('seg_nom_arr', models.CharField(max_length=50, verbose_name='Segundo Nombre')),
                ('pri_ape_arr', models.CharField(max_length=50, verbose_name='Primero Apellido')),
                ('seg_ape_arr', models.CharField(max_length=50, verbose_name='Segundo Apellido')),
                ('contacto_arr', models.IntegerField(verbose_name='Contacto')),
                ('correo_arr', models.EmailField(max_length=254, verbose_name='Correo')),
                ('estado', models.BooleanField()),
                ('saldo', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Arriendo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_arriendo', models.IntegerField(verbose_name='Codigo Arriendo')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_termino', models.DateField(verbose_name='Fecha de Termino')),
                ('fecha_pri_ajuste', models.DateField(verbose_name='Fecha Primer Reajuste')),
                ('periodo_reajuste', models.DateField(verbose_name='Perdio Reajuste')),
                ('monto_arriendo', models.IntegerField(verbose_name='Monto arriendo')),
                ('fecha_entrega', models.DateField(verbose_name='Fecha entrega arriendo')),
                ('estado_arriendo', models.CharField(max_length=120, verbose_name='Estado del arriendo')),
                ('porcentaje_multa', models.IntegerField(verbose_name='Porcentaje Multa')),
                ('arrendatario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.arrendatario')),
            ],
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_banco', models.CharField(max_length=180, unique=True, verbose_name='Nombre del Banco')),
                ('nic_banco', models.CharField(max_length=50, unique=True, verbose_name='Siglas Banco')),
                ('cod_banco', models.CharField(max_length=100, unique=True, verbose_name='Código Banco ')),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('nom_com', models.CharField(max_length=200, unique=True, verbose_name='Nombre Comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('nom_reg', models.CharField(max_length=200, verbose_name='Nombre Región')),
            ],
        ),
        migrations.CreateModel(
            name='TipoPropiedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipoppdd', models.CharField(max_length=150, verbose_name='Tipo de propiedad')),
                ('descripcion_tipoppdd', models.CharField(max_length=250, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='TipoTrabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=150, unique=True)),
                ('descripcion', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_trab', models.CharField(max_length=12, unique=True, verbose_name='Rut Trabajador')),
                ('pri_nom_trab', models.CharField(max_length=50, verbose_name='Primer Nombre')),
                ('seg_nom_trab', models.CharField(max_length=50, verbose_name='Segundo Nombre')),
                ('pri_ape_trab', models.CharField(max_length=50, verbose_name='Primer Apellido')),
                ('seg_ape_trab', models.CharField(max_length=50, verbose_name='Segundo Apellido')),
                ('celular', models.IntegerField()),
                ('direccion', models.CharField(max_length=250)),
                ('cuenta', models.CharField(max_length=120)),
                ('comuna_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.comuna')),
                ('tipo_trab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.tipotrabajador', verbose_name='Area Trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='TipoCuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_cuenta', models.CharField(max_length=150, verbose_name='Nombre de la cuenta')),
                ('desc_cuenta', models.CharField(max_length=250, verbose_name='Descripcion de la cuenta')),
                ('banco_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.banco')),
            ],
        ),
        migrations.CreateModel(
            name='ServiciosExtras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_servicio', models.CharField(max_length=150, verbose_name='Nombre servicio')),
                ('descripcion', models.CharField(max_length=250)),
                ('fecha', models.DateField()),
                ('Monto', models.IntegerField()),
                ('arriendo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.arriendo')),
            ],
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut_prop', models.CharField(max_length=12, unique=True, verbose_name='Rut Propietario')),
                ('pri_nom_pro', models.CharField(max_length=50, verbose_name='Primer Nombre')),
                ('seg_nom_prop', models.CharField(max_length=50, verbose_name='Segundo Nombre')),
                ('pri_ape_prop', models.CharField(max_length=50, verbose_name='Primero Apellido')),
                ('seg_ape_prop', models.CharField(max_length=50, verbose_name='Segundo Apellido')),
                ('direccion_prop', models.CharField(max_length=200, verbose_name='Dirección Principal')),
                ('email_prop', models.EmailField(max_length=254)),
                ('contacto_prop', models.IntegerField()),
                ('comuna_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_ppdd', models.CharField(max_length=40, unique=True, verbose_name='Código Propiedad')),
                ('direccion_ppdd', models.CharField(max_length=150, verbose_name='Dirección Propiedad')),
                ('rol_ppdd', models.CharField(max_length=50, verbose_name='Rol propiedad')),
                ('comuna_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.comuna')),
                ('propietario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.propietario')),
                ('tipopropiedad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.tipopropiedad')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalidadJuridica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=80, unique=True)),
                ('razon_social', models.CharField(max_length=250, verbose_name='Razón Social')),
                ('representante', models.CharField(max_length=150)),
                ('propietario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.propietario')),
            ],
        ),
        migrations.CreateModel(
            name='Gastocomun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('fecha', models.DateField()),
                ('arriendo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.arriendo')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleArriendo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField()),
                ('arriendo_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.arriendo')),
                ('propiedad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.propiedad')),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuenta', models.IntegerField()),
                ('estado_cuenta', models.CharField(max_length=100, verbose_name='Estado de cuenta')),
                ('banco_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.banco')),
                ('propietario_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.propietario')),
                ('tipocuenta_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.tipocuenta')),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='reg_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.region'),
        ),
        migrations.AddField(
            model_name='arrendatario',
            name='cuenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ApiArriendosAlegria.tipocuenta'),
        ),
    ]
