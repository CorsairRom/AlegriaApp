from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from datetime import datetime
from rest_framework import serializers
from ApiArriendosAlegria.managers import GestorUsuario

# Create your models here.
# ---------Choices---------

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
    """
    Modelo que representa a los usuarios del sistema, basado en AbstractBaseUser.
    """
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
    """
    Modelo que representa a las regiones.
    """
    id = models.IntegerField(verbose_name="Numero Región", primary_key=True)
    orden = models.IntegerField(verbose_name="orden region", default=0, unique=True)
    nom_reg = models.CharField(max_length=250, verbose_name="Nombre Región", unique=True)
    
    def __str__(self):
        return self.nom_reg
    
class Comuna(models.Model):
    """
    Modelo que representa a las comunas.
    """
    nom_com = models.CharField(max_length=200, unique=True, verbose_name="Nombre Comuna")
    reg_id = models.ForeignKey(Region, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nom_com

# model banco-cuenta-tipo cuenta

class Banco(models.Model):
    """
    Modelo que representa a los bancos para el registro de los pagos.
    """
    nombre_banco = models.CharField(max_length=180, unique=True, verbose_name='Nombre del Banco')
    cod_banco = models.CharField(max_length=100, unique=True, verbose_name='Código Banco ')

    def __str__(self):
        return self.nombre_banco
    

class TipoCuenta(models.Model):
    """
    Modelo que representa al tipo de cuenta bancaria.
    """
    nom_cuenta = models.CharField(max_length=150, verbose_name='Nombre de la cuenta')
   
    def __str__(self):
        return self.nom_cuenta
    
class Cuenta(models.Model):
    """
    Modelo que representa a la cuenta bancaria.
    """
    cuenta = models.IntegerField(verbose_name='Numero de cuenta')
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    tipocuenta = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)
    estado_cuenta = models.CharField( max_length=100, verbose_name='Estado de cuenta')
    propietario_rut = models.CharField( max_length=12, verbose_name='Propietario de la cuenta', default='01.234.456-7')
    
    def __str__(self):
        return self.cuenta      
    
# model trabajador

class TipoTrabajador(models.Model):
    """
    Modelo que representa al tipo de trabajador de Propiedades Alegría.
    """
    tipo = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=250)
    
    def __str__(self):
        return self.tipo
    
class Trabajador(models.Model):
    """
    Modelo que representa al trabajador de Propiedades Alegría.
    """
    rut_trab = models.CharField(max_length=12, unique=True, verbose_name='Rut Trabajador')
    pri_nom_trab = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_trab = models.CharField(max_length=50, verbose_name='Segundo Nombre', blank=True, null=True)
    pri_ape_trab = models.CharField(max_length=50, verbose_name='Primer Apellido')
    seg_ape_trab = models.CharField(max_length=50, verbose_name='Segundo Apellido', blank=True, null=True)
    celular = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=250)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_trab = models.ForeignKey(TipoTrabajador, on_delete=models.CASCADE, verbose_name='Area Trabajador')
    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.rut_trab
 
# model propietario-personalidadJuridica   

class Propietario(models.Model):
    """
    Modelo que representa a los propietarios.
    """
    rut_prop = models.CharField(max_length=12, unique=True, verbose_name='Rut Propietario')
    pri_nom_prop = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_prop = models.CharField(max_length=50, verbose_name='Segundo Nombre', null=True, blank=True)
    pri_ape_prop = models.CharField(max_length=50, verbose_name='Primero Apellido')
    seg_ape_prop = models.CharField(max_length=50, verbose_name='Segundo Apellido', null=True, blank=True)
    direccion_prop = models.CharField(max_length=200, verbose_name='Dirección Principal')
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    email_prop = models.EmailField(verbose_name='Email Propietario')
    contacto_prop = models.IntegerField(verbose_name='Contacto Propietario')
    
    def __str__(self):
        return self.rut_prop
    
class PersonalidadJuridica(models.Model):
    """
    Modelo que representa a las personalidades jurídicas, especialmente si son propietarios.
    """
    rol = models.CharField(max_length=80, unique=True)
    razon_social = models.CharField(max_length=250, verbose_name='Razón Social')
    representante = models.CharField(max_length=150)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.rol

# model propiedad - tipo propiedad  

class TipoPropiedad(models.Model):
    """
    Modelo que representa al tipo de propiedad.
    """
    nombre_tipoppdd = models.CharField(max_length=150, verbose_name='Tipo de propiedad')
    descripcion_tipoppdd = models.CharField(max_length=250, verbose_name='Descripción')
    
    def __str__(self):
        return self.nombre_tipoppdd 
    
class Propiedad(models.Model):
    """
    Modelo que representa a la propiedad.
    """
    direccion_ppdd = models.CharField(max_length=150, verbose_name='Dirección Propiedad')
    numero_ppdd = models.IntegerField(verbose_name='Número Propiedad', null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    tipopropiedad = models.ForeignKey(TipoPropiedad, on_delete=models.CASCADE)
    rol_ppdd = models.CharField(max_length=50, verbose_name='Rol propiedad', null=True, blank=True)
    
    def __str__(self):
        return str(self.id)    
    
class ExtraDepartamento(models.Model):
    bodega = models.IntegerField( blank=True, null=True )
    estacionamiento = models.IntegerField( blank=True, null=True) 
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)

    
# model Arrendatario - arriendo - servicios extras - gasto comun - detalle arriendo

class Arrendatario(models.Model):
    """
    Modelo que representa al arrendatario.
    """
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
    """
    Modelo que representa a los arriendos.
    """
    cod_arriendo = models.CharField(max_length=50, verbose_name='Codigo Arriendo', null=True, blank=True)
    arrendatario = models.ForeignKey(Arrendatario, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField( verbose_name='Fecha de Inicio')
    fecha_termino = models.DateTimeField( verbose_name= 'Fecha de Termino')
    fecha_pri_ajuste = models.DateTimeField(blank=True, null=True)
    periodo_reajuste = models.IntegerField(verbose_name='Perdio Reajuste')
    monto_arriendo = models.IntegerField(verbose_name='Monto arriendo')
    fecha_entrega = models.DateTimeField(verbose_name='Fecha entrega arriendo', null=True, blank=True)
    estado_arriendo = models.BooleanField(default=True)
    porcentaje_multa = models.IntegerField(verbose_name='Porcentaje Multa')
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.cod_arriendo
    
class ServiciosExtras(models.Model):
    """
    Modelo que representa a los servicios extra.

    Por ejemplo: Gásfiter.
    """
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    nom_servicio = models.CharField(max_length=150, verbose_name='Nombre servicio')
    descripcion = models.CharField(max_length=250)
    fecha = models.DateTimeField()
    Monto = models.IntegerField()
    
    def __str__(self):
        return self.arriendo_id +' - '+ self.nom_servicio
    
class Gastocomun(models.Model):
    """
    Modelo que representa a los gastos comunes.
    """
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    valor = models.IntegerField()
    fecha = models.DateTimeField()
    
    def __str__(self):
        return self.arriendo + ' - ' + self.valor
    
class DetalleArriendo(models.Model):
    """
    Modelo que representa el detalle de los arriendos.
    """
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField()
    monto_pago = models.PositiveIntegerField(null=True)
    
    def __str__(self):
        return self.arriendo
    
    
    
    