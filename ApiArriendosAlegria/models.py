from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from datetime import datetime
from rest_framework import serializers
from ApiArriendosAlegria.managers import GestorUsuario


class ValoresGlobales(models.Model):
    nombre= models.CharField(max_length=200)
    valor = models.FloatField()
    
    def __str__(self):
        return self.nombre

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
    cuenta = models.PositiveBigIntegerField(verbose_name='Numero de cuenta')
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    tipocuenta = models.ForeignKey(TipoCuenta, on_delete=models.CASCADE)
    estado_cuenta = models.CharField( max_length=100, verbose_name='Estado de cuenta')
    propietario_rut = models.CharField( max_length=12, verbose_name='Propietario de la cuenta', default='01.234.456-7')
    rut_tercero = models.CharField( max_length=12, verbose_name='Propietario de la cuenta', null=True, blank=True, default="111.111.111-1")
    
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
class PersonalidadJuridica(models.Model):
    """
    Modelo que representa a las personalidades jurídicas, especialmente si son propietarios.
    """
    rut = models.CharField(max_length=80, unique=True)
    razon_social = models.CharField(max_length=250, verbose_name='Razón Social')
    direccion = models.CharField(max_length=200, verbose_name='Dirección Principal', null=True, blank=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    contacto = models.IntegerField(verbose_name='Contacto', null=True, blank=True)
    
    def __str__(self):
        return self.rut

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
    pctje_cobro_honorario = models.FloatField(verbose_name='Porcentaje Contacto Propietario', null=True, blank=True)
    personalidad_juridica = models.ForeignKey(PersonalidadJuridica, null=True, blank=True, default=None, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.rut_prop
    


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
    numero_ppdd = models.CharField(verbose_name='Número Propiedad', null=True, blank=True, max_length=50)
    rol_ppdd = models.CharField(max_length=50, verbose_name='Rol propiedad', null=True, blank=True)

    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    tipopropiedad = models.ForeignKey(TipoPropiedad, on_delete=models.CASCADE)
    
    cod = models.IntegerField(null=True, blank=True, unique=True) # Código que se maneja en los archivos ad hoc.

    nro_bodega = models.IntegerField(verbose_name='Número Bodega', null=True, blank=True, default=None)
    nro_estacionamiento = models.IntegerField(verbose_name='Número Estacionamiento', null=True, blank=True, default=None)

    valor_arriendo_base = models.PositiveBigIntegerField(verbose_name='Valor Arriendo Base')
    es_valor_uf = models.BooleanField(default=False)
    
    #Codigos de agua luz gas, en una proxima revision es necesario destructurar esta informacion
    gas = models.CharField(verbose_name='Código Gas', null=True, blank=True, max_length=50) # codigo y nombre de compañia de gas
    agua = models.CharField(verbose_name='Código ESSBIO', null=True, blank=True, max_length=50) # codigo y nombre de compañia de agua
    luz = models.CharField(verbose_name='Código Luz', null=True, blank=True, max_length=50)  # codigo y nombre de compañia de luz
    
    def __str__(self):
        return str(self.id)    
    
    
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
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE, null=True)
    arrendatario = models.ForeignKey(Arrendatario, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(verbose_name='Fecha de Inicio')
    fecha_termino = models.DateTimeField(verbose_name= 'Fecha de Termino')
    dia_pago = models.IntegerField(verbose_name='Día de pago (nro.)', null=True, blank=True)
    comision = models.FloatField(verbose_name='Comisión', null=True, blank=True) # sumatoria de los porcentajes o se puede crear de forma manual
    porcentaje_1 = models.FloatField(verbose_name='Porcentaje 1', null=True, blank=True) # Porcentaje honorarios
    porcentaje_2 = models.FloatField(verbose_name='Porcentaje 2', null=True, blank=True) # Procentaje boleta de honorarios
    fecha_pri_ajuste = models.DateTimeField(blank=True, null=True) #creado al momento de guardar o modificar el el monto del arriendo
    periodo_reajuste = models.IntegerField(verbose_name='Perdio Reajuste')
    monto_arriendo = models.IntegerField(verbose_name='Monto arriendo')
    fecha_entrega = models.DateTimeField(verbose_name='Fecha entrega arriendo', null=True, blank=True)
    estado_arriendo = models.BooleanField(default=True)
    observaciones = models.TextField(verbose_name='Observaciones adicionales sobre el arriendo')
        
    def __str__(self):
        return self.cod_arriendo
    
class ArriendoDepartamento(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.id)
    
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
    
class Externo(models.Model):
    """
    Modelo para trabajadores como administrador de condominios (edificios o casas),
    o conserjes.
    """
    nombre = models.CharField(max_length=50, unique=True)
    contacto_arr = models.IntegerField( verbose_name='Contacto')
    correo_arr = models.EmailField(verbose_name='Correo')
    direccion = models.CharField(max_length=50)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL)
