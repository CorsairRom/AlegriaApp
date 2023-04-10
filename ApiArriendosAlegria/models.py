from django.db import models

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





# Models region-comuna

class Region(models.Model):
    id = models.CharField(primary_key=True )
    nom_reg = models.CharField(max_length=200, verbose_name="Nombre Región")
    
    def __str__(self):
        return self.nom_reg
    
class Comuna(models.Model):
    id = models.CharField(primary_key=True)
    nom_com = models.CharField(max_length=200, unique=True, verbose_name="Nombre Comuna")
    reg_id = models.ForeignKey(Region, on_delete= models.CASCADE)
    
    def __str__(self):
        return self.nom_com
    
# model trabajador

class TipoTrabajador(models.Model):
    tipo = models.CharField(max_length=150, unique=True)
    descripcion = models.CharField(max_length=250)
    
    def __str__(self):
        return self.tipo
    
class Trabajador(models.Model):
    rut_trab = models.CharField(max_length=12, unique=True, verbose_name='Rut Trabajador')
    pri_nom_trab = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_trab = models.CharField(max_length=50, verbose_name='Segundo Nombre')
    pri_ape_trab = models.CharField(max_length=50, verbose_name='Primer Apellido')
    seg_ape_trab = models.CharField(max_length=50, verbose_name='Segundo Apellido')
    celular = models.IntegerField()
    direccion = models.CharField(max_length=250)
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_trab = models.ForeignKey(TipoTrabajador, on_delete=models.CASCADE, verbose_name='Area Trabajador')
    # agregar usuario
    
    def __str__(self):
        return self.rut_trab
 
# model propietario-propiedad   

class Propietario(models.Model):
    rut_prop = models.CharField(max_length=12, unique=True, verbose_name='Rut Propietario')
    pri_nom_pro = models.CharField(max_length=50, verbose_name='Primer Nombre')
    seg_nom_prop = models.CharField(max_length=50, verbose_name='Segundo Nombre')
    pri_ape_prop = models.CharField(max_length=50, verbose_name='Primero Apellido')
    seg_ape_prop = models.CharField(max_length=50, verbose_name='Segundo Apellido')
    direccion_prop = models.CharField(max_length=200, verbose_name='Dirección Principal')
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    email_prop = models.EmailField()
    contacto_prop = models.IntegerField()
    
    def __str__(self):
        return self.rut_prop
    
            
# model banco-cuenta-tipo cuenta

class Banco(models.Model):
    nombre_banco = models.CharField(max_length=180, unique=True, verbose_name='Nombre del Banco')
    nic_banco = models.CharField(max_length=50, unique=True, verbose_name='Siglas Banco')
    cod_banco = models.CharField(max_length=100, unique=True, verbose_name='Código Banco ')

    def __str__(self):
        return self.nic_banco
    

class TipoCuenta(models.Model):
    nom_cuenta = models.CharField(max_length=150, verbose_name='Nombre de la cuenta')
    desc_cuenta = models.CharField(max_length=250, verbose_name='Descripcion de la cuenta')
    banco_id = models.ForeignKey(Banco, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nom_cuenta
    
class Cuenta(models.Model):
    cuenta = models.IntegerField()
    tipo_cuenta = models.CharField(max_length=150, verbose_name='Tipo de cuenta')
    banco_id = models.ForeignKey(Banco, on_delete=models.CASCADE)
    estado_cuenta = models.BooleanField()
    propietario_id = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.cuenta
    
    