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

    def create(self, validated_data):
        user = Usuario.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class SerializadorListaUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'is_active': instance['is_active'],
        }
        
class serializerRegion(serializers.ModelSerializer):
    
    class Meta:
        model = Region
        fields = '__all__'

class serializerComuna(serializers.ModelSerializer):
    
    class Meta:
        model = Comuna
        fields = '__all__'
        
class serializerTipoTrabajado(serializers.ModelSerializer):
    
    class Meta:
        model = TipoTrabajador
        fields = '__all__'
        
class serializerTrabajador(serializers.ModelSerializer):
    
    class Meta:
        model = Trabajador
        fields = '__all__'
        
class serializerBanco(serializers.ModelSerializer):
    
    class Meta:
        model = Banco
        fields = '__all__'
        
class serializerTipoCuenta(serializers.ModelSerializer):
    
    class Meta:
        model = TipoCuenta
        fields = '__all__'
        
class serializerCuenta(serializers.ModelSerializer):
    
    class Meta:
        model = Cuenta
        fields = '__all__'
        
class serializerPropietario(serializers.ModelSerializer):
    
    class Meta:
        model = Propietario
        fields = '__all__'

class serializerPersonalidadJuridica(serializers.ModelSerializer):
    
    class Meta:
        model = PersonalidadJuridica
        fields = '__all__'
        
class serializerPropiedad(serializers.ModelSerializer):
    
    class Meta:
        model = Propiedad
        fields = '__all__'
        
class serializerTipoPropiedad(serializers.ModelSerializer):
    
    class Meta:
        model = TipoPropiedad
        fields = '__all__'

class serializerArrendatario(serializers.ModelSerializer):
    
    class Meta:
        model = Arrendatario
        fields = '__all__'
        
class serializerArriendo(serializers.ModelSerializer):
    
    class Meta:
        model = Arriendo
        fields = '__all__'

class serializerDetalleArriendo(serializers.ModelSerializer):
    
    class Meta:
        model = DetalleArriendo
        fields = '__all__'
        
class serializerServiciosExtas(serializers.ModelSerializer):
    
    class Meta:
        model = ServiciosExtras
        fields = '__all__'
        
class serializerGastoComun(serializers.ModelSerializer):
    
    class Meta:
        model = Gastocomun
        fields = '__all__'

    