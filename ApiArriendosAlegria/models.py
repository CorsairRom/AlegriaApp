from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from ApiArriendosAlegria.managers import GestorUsuario

# Create your models here.
# ---------Choises---------

tipoCuenta = {
    'vista': "vista",
    'Cuenta corriente': "Cuenta corriente",
    'Rut' : "Rut",
    
}

sexo = {
    'Hombre': "Hombre",
    'Mujer' : "Mujer",
    'No definido' : "No definido",
}

# Model abstractUser
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField('Email', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = GestorUsuario()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def natural_key(self):
        return (self.username)
    
    def __str__(self):
        return f'{self.username}'


# Models region-comuna

class Region(models.Model):
    id = models.IntegerField(verbose_name="Numero Región", primary_key=True)
    orden = models.IntegerField(verbose_name="orden region", default=0, unique=True)
    nom_reg = models.CharField(max_length=250, verbose_name="Nombre Región", unique=True)
    
    def __str__(self):
        return self.nom_reg
    
class Comuna(models.Model):
    nom_com = models.CharField(max_length=200, unique=True, verbose_name="Nombre Comuna")
    reg_id = models.ForeignKey(Region, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nom_com

# model banco-cuenta-tipo cuenta

class Banco(models.Model):
    nombre_banco = models.CharField(max_length=180, unique=True, verbose_name='Nombre del Banco')
    cod_banco = models.CharField(max_length=100, unique=True, verbose_name='Código Banco ')

    def __str__(self):
        return self.nombre_banco
    

class TipoCuenta(models.Model):
    nom_cuenta = models.CharField(max_length=150, verbose_name='Nombre de la cuenta')
   
    def __str__(self):
        return self.nom_cuenta
    
class Cuenta(models.Model):
    cuenta = models.IntegerField(verbose_name='Numero de cuenta')
    banco_id = models.ForeignKey(Banco, on_delete=models.CASCADE)
    tipocuenta_id = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)
    estado_cuenta = models.CharField( max_length=100, verbose_name='Estado de cuenta')
    propietario_rut = models.CharField( max_length=12, verbose_name='Propietario de la cuenta', default='01.234.456-7')
    
    def __str__(self):
        return self.cuenta      
    
# model trabajador

class TipoTrabajador(models.Model):
    tipo = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=250)
    
    def __str__(self):
        return self.tipo
    
class Trabajador(models.Model):
    rut_trab = models.CharField(max_length=12, unique=True, verbose_name='Rut Trabajador')
    pri_nom_trab = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_trab = models.CharField(max_length=50, verbose_name='Segundo Nombre', blank=True, null=True)
    pri_ape_trab = models.CharField(max_length=50, verbose_name='Primer Apellido')
    seg_ape_trab = models.CharField(max_length=50, verbose_name='Segundo Apellido', blank=True, null=True)
    celular = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=250)
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_trab = models.ForeignKey(TipoTrabajador, on_delete=models.CASCADE, verbose_name='Area Trabajador')
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.rut_trab
 
# model propietario-personalidadJuridica   

class Propietario(models.Model):
    rut_prop = models.CharField(max_length=12, unique=True, verbose_name='Rut Propietario')
    pri_nom_prop = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_prop = models.CharField(max_length=50, verbose_name='Segundo Nombre', null=True, blank=True)
    pri_ape_prop = models.CharField(max_length=50, verbose_name='Primero Apellido')
    seg_ape_prop = models.CharField(max_length=50, verbose_name='Segundo Apellido', null=True, blank=True)
    direccion_prop = models.CharField(max_length=200, verbose_name='Dirección Principal')
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    email_prop = models.EmailField(verbose_name='Email Propietario')
    contacto_prop = models.IntegerField(verbose_name='Contacto Propietario')
    
    def __str__(self):
        return self.rut_prop
    
class PersonalidadJuridica(models.Model):
    rol = models.CharField(max_length=80, unique=True)
    razon_social = models.CharField(max_length=250, verbose_name='Razón Social')
    representante = models.CharField(max_length=150)
    propietario_id = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.rol

# model propiedad - tipo propiedad  

class TipoPropiedad(models.Model):
    nombre_tipoppdd = models.CharField(max_length=150, verbose_name='Tipo de propiedad')
    descripcion_tipoppdd = models.CharField(max_length=250, verbose_name='Descripción')
    
    def __str__(self):
        return str(self.id) + " - " + self.nombre_tipoppdd
    
    
class Propiedad(models.Model):
    direccion_ppdd = models.CharField(max_length=150, verbose_name='Dirección Propiedad')
    numero_ppdd = models.IntegerField(verbose_name='Número Propiedad')
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    propietario_id = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    tipopropiedad_id = models.ForeignKey(TipoPropiedad, on_delete=models.CASCADE)
    rol_ppdd = models.CharField(max_length=50, verbose_name='Rol propiedad', null=True, blank=True)
    
    def __str__(self):
        return str(self.id)     

    
# model Arrendatario - arriendo - servicios extras - gasto comun - detalle arriendo

class Arrendatario(models.Model):
    rut_arr = models.CharField(max_length=12, unique=True, verbose_name='Rut Arrendatario')
    pri_nom_arr = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_arr = models.CharField(max_length=50, verbose_name='Segundo Nombre', null=True, blank=True)
    pri_ape_arr = models.CharField(max_length=50, verbose_name='Primero Apellido')
    seg_ape_arr = models.CharField(max_length=50, verbose_name='Segundo Apellido', null=True, blank=True)
    contacto_arr = models.IntegerField( verbose_name='Contacto')
    correo_arr = models.EmailField(verbose_name='Correo')
    estado = models.BooleanField()
    saldo = models.IntegerField()
    
    def __str__(self):
        return self.rut_arr
    
class Arriendo(models.Model):
    cod_arriendo = models.IntegerField( verbose_name='Codigo Arriendo')
    arrendatario_id = models.ForeignKey(Arrendatario, on_delete=models.CASCADE)
    fecha_inicio = models.DateField( verbose_name='Fecha de Inicio')
    fecha_termino = models.DateField( verbose_name= 'Fecha de Termino')
    fecha_pri_ajuste = models.DateField(verbose_name='Fecha Primer Reajuste')
    periodo_reajuste = models.DateField(verbose_name='Perdio Reajuste')
    monto_arriendo = models.IntegerField(verbose_name='Monto arriendo')
    fecha_entrega = models.DateField(verbose_name='Fecha entrega arriendo')
    estado_arriendo = models.CharField(max_length=120, verbose_name='Estado del arriendo')
    porcentaje_multa = models.IntegerField(verbose_name='Porcentaje Multa')
    
    def __str__(self):
        return self.cod_arriendo
    
class ServiciosExtras(models.Model):
    arriendo_id = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    nom_servicio = models.CharField(max_length=150, verbose_name='Nombre servicio')
    descripcion = models.CharField(max_length=250)
    fecha = models.DateField()
    Monto = models.IntegerField()
    
    def __str__(self):
        return self.arriendo_id +' - '+ self.nom_servicio
    
class Gastocomun(models.Model):
    arriendo_id = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    valor = models.IntegerField()
    fecha = models.DateField()
    
    def __str__(self):
        return self.arriendo_id + ' - ' + self.valor
    
class DetalleArriendo(models.Model):
    arriendo_id = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    propiedad_id = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    
    def __str__(self):
        return self.arriendo_id
    
    
    
    