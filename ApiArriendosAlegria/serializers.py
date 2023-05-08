from rest_framework import serializers
from ApiArriendosAlegria.models import Usuario, Region, Comuna, TipoTrabajador, Trabajador, Propietario, PersonalidadJuridica,\
                                        TipoPropiedad,Propiedad, Banco, TipoCuenta, Cuenta, Arrendatario, Arriendo, ServiciosExtras,\
                                        Gastocomun, DetalleArriendo 


class SerializadorTokenUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email')


class SerializadorUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'is_active')
        extra_kwargs = {'is_staff': {'write_only': True}, 'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

        
class SerializerRegion(serializers.ModelSerializer):
    
    class Meta:
        model = Region
        fields = '__all__'

class SerializerComuna(serializers.ModelSerializer):
    
    class Meta:
        model = Comuna
        fields = '__all__'
        
class SerializerTipoTrabajado(serializers.ModelSerializer):
    
    class Meta:
        model = TipoTrabajador
        fields = '__all__'
        
class SerializerTrabajador(serializers.ModelSerializer):
    
    class Meta:
        model = Trabajador
        fields = '__all__'
        
class SerializerBanco(serializers.ModelSerializer):
    
    class Meta:
        model = Banco
        fields = '__all__'
        
class SerializerTipoCuenta(serializers.ModelSerializer):
    
    class Meta:
        model = TipoCuenta
        fields = '__all__'
        
class SerializerCuenta(serializers.ModelSerializer):
    
    class Meta:
        model = Cuenta
        fields = '__all__'
        
class SerializerPropietario(serializers.ModelSerializer):
    
    class Meta:
        model = Propietario
        fields = '__all__'

class SerializerPersonalidadJuridica(serializers.ModelSerializer):
    
    class Meta:
        model = PersonalidadJuridica
        fields = '__all__'
        
class SerializerPropiedad(serializers.ModelSerializer):
    
    class Meta:
        model = Propiedad
        fields = '__all__'
        
class SerializerTipoPropiedad(serializers.ModelSerializer):
    
    class Meta:
        model = TipoPropiedad
        fields = '__all__'

class SerializerArrendatario(serializers.ModelSerializer):
    
    class Meta:
        model = Arrendatario
        fields = '__all__'
        
class SerializerArriendo(serializers.ModelSerializer):
    
    class Meta:
        model = Arriendo
        fields = '__all__'

class SerializerDetalleArriendo(serializers.ModelSerializer):
    
    class Meta:
        model = DetalleArriendo
        fields = '__all__'
        
class SerializerServiciosExtas(serializers.ModelSerializer):
    
    class Meta:
        model = ServiciosExtras
        fields = '__all__'
        
class SerializerGastoComun(serializers.ModelSerializer):
    
    class Meta:
        model = Gastocomun
        fields = '__all__'

    