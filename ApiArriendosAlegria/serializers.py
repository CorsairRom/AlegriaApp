from rest_framework import serializers
from ApiArriendosAlegria.models import Usuario, Region, Comuna, TipoTrabajador, Trabajador, Propietario, PersonalidadJuridica,\
                                        TipoPropiedad,Propiedad, Banco, TipoCuenta, Cuenta, Arrendatario, Arriendo, ServiciosExtras,\
                                        Gastocomun, DetalleArriendo 


class SerializadorUsuario(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'is_staff': instance.is_staff,
            'is_superuser': instance.is_superuser
        }
        return data

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
        
    def to_representation(self, instance):
        data = {
            'id': instance.id,
            'nom_com': instance.nom_com,
            'reg_id': {
                'id': instance.reg_id.id,
                'nom_reg': instance.reg_id.nom_reg
            }
        }
        return data
        
class SerializerTipoTrabajado(serializers.ModelSerializer):
    
    class Meta:
        model = TipoTrabajador
        fields = '__all__'
    
    
        
class SerializerTrabajador(serializers.ModelSerializer):
    comuna_id = serializers.SerializerMethodField()
    tipo_trab = serializers.SerializerMethodField()
    class Meta:
        model = Trabajador
        fields = '__all__'
    
    def get_comuna_id(self, obj):
        return {'id': obj.comuna_id.id, 'nom_com': obj.comuna_id.nom_com}
    
    def get_tipo_trab(self, obj):
        return {'id': obj.tipo_trab.id, 'tipo': obj.tipo_trab.tipo}
        
class SerializerBanco(serializers.ModelSerializer):
    
    class Meta:
        model = Banco
        fields = '__all__'
        
class SerializerTipoCuenta(serializers.ModelSerializer):
    
    class Meta:
        model = TipoCuenta
        fields = '__all__'
        
class SerializerCuenta(serializers.ModelSerializer):
    banco_id = serializers.SerializerMethodField()
    tipocuenta_id = serializers.SerializerMethodField()
    class Meta:
        model = Cuenta
        fields = '__all__'
    
    def get_banco_id(self, obj):
        return {'id': obj.banco_id.id, 'nombre_banco':obj.banco_id.nombre_banco}
    
    def get_tipocuenta_id(self, obj):
        return {'id':obj.tipocuenta_id.id, 'nom_cuenta':obj.tipocuenta_id.nom_cuenta}
        
class SerializerPropietario(serializers.ModelSerializer):
    
    class Meta:
        model = Propietario
        fields = '__all__'
        
    

class SerializerPersonalidadJuridica(serializers.ModelSerializer):
    propietario_id = serializers.SerializerMethodField()
    class Meta:
        model = PersonalidadJuridica
        fields = '__all__'
     
    def get_propietario_id(self, obj):
        return{'id': obj.propietario_id.id, 'rut_prop': obj.propietario_id.rut_prop}  
     
class SerializerPropiedad(serializers.ModelSerializer):
    tipopropiedad_id = serializers.SerializerMethodField()
    comuna_id = serializers.SerializerMethodField()
    propietario_id = serializers.SerializerMethodField()
    class Meta:
        model = Propiedad
        fields = '__all__'
        
    def get_tipopropiedad_id(self, obj):
        return {'id': obj.tipopropiedad_id.id, 'nombre_tipoppdd': obj.tipopropiedad_id.nombre_tipoppdd}
    
    def get_comuna_id(self, obj):
        return{'id': obj.comuna_id.id, 'nom_com': obj.comuna_id.nom_com}
    def get_propietario_id(self,obj):
        return{'id': obj.propietario_id.id, 
               'rut_prop':obj.propietario_id.rut_prop,
               'pri_nom_prop':obj.propietario_id.pri_nom_prop,
               'seg_nom_prop':obj.propietario_id.seg_nom_prop,
               'pri_ape_prop':obj.propietario_id.pri_ape_prop,
               'seg_ape_prop':obj.propietario_id.seg_ape_prop,
               }
        
class SerializerTipoPropiedad(serializers.ModelSerializer):
    
    class Meta:
        model = TipoPropiedad
        fields = '__all__'

class SerializerArrendatario(serializers.ModelSerializer):
    
    class Meta:
        model = Arrendatario
        fields = '__all__'
        
class SerializerArriendo(serializers.ModelSerializer):
    
    arrendatario_id = serializers.SerializerMethodField()
    class Meta:
        model = Arriendo
        fields = '__all__'

    def get_arrendatario_id(self, obj):
        return {'id':obj.arrendatario_id.id, 
                'rut_arr': obj.arrendatario_id.rut_arr,
                'pri_nom_arr': obj.arrendatario_id.pri_nom_arr,
                'seg_nom_arr': obj.arrendatario_id.seg_nom_arr,
                'pri_ape_arr': obj.arrendatario_id.pri_ape_arr,
                'seg_ape_arr': obj.arrendatario_id.seg_ape_arr,
                'correo_arr': obj.arrendatario_id.correo_arr,
                
                }
    
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

    