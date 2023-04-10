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
    rut_trab = models.CharField(max_length=12, unique=True)
    pri_nom = models.CharField(max_length=50)
    seg_nom = models.CharField(max_length=50)
    pri_ape = models.CharField(max_length=50)
    seg_ape = models.CharField(max_length=50)
    celular = models.IntegerField()
    direccion = models.CharField(max_length=250)
    comuna_id = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    tipo_trab = models.ForeignKey(TipoTrabajador, on_delete=models.CASCADE)
    # agregar usuario
    
    def __str__(self):
        return self.rut_trab
 
# model propietario-propiedad   }

class Propietaro(models.Model):
    rut_prop = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=200)
    
    
    
    
    
# model banco-cuenta-tipo cuenta

class Banco(models.Model):
    nombre_banco = models.CharField(max_length=180, unique=True)
    nic_banco = models.CharField(max_length=50, unique=True)
    cod_banco = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nic_banco
    

class TipoCuenta(models.Model):
    nom_cuenta = models.CharField(max_length=150)
    desc_cuenta = models.CharField(max_length=250)
    cuenta_estado = models.BooleanField()
    
    