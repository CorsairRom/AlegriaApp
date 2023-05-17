from rest_framework import serializers
from ApiArriendosAlegria.models import ArriendoDepartamento, Usuario, Region, Comuna, TipoTrabajador, Trabajador, Propietario, PersonalidadJuridica,\
                                        TipoPropiedad,Propiedad, Banco, TipoCuenta, Cuenta, Arrendatario, Arriendo, ServiciosExtras,\
                                        Gastocomun, DetalleArriendo 
from ApiArriendosAlegria.Rut import validarRut

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
       
    comuna_id= serializers.PrimaryKeyRelatedField(
        queryset=Comuna.objects.all(),
        source='comuna', 
        write_only=True,  
    )
    tipo_trab_id= serializers.PrimaryKeyRelatedField(
        queryset=TipoTrabajador.objects.all(),
        source='tipo_trab', 
        write_only=True,  
    )
    usuario = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        source='usuario_id',
        write_only=True,
        required=False
    )
    comuna = serializers.SerializerMethodField()
    tipo_trab = serializers.SerializerMethodField()
    usuario_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Trabajador
        fields = '__all__'
    
    def validate(self, data):
        rut_trab = data.get('rut_trab')
        if not validarRut(rut_trab):
            raise serializers.ValidationError("Rut inválido")
        return data
        
    def get_comuna(self, obj):
        return {'id':obj.comuna.id, 'nom_com':obj.comuna.nom_com}
    
    def get_tipo_trab(self, obj):
        return {'id':obj.tipo_trab.id, 'tipo':obj.tipo_trab.tipo}
    
    def get_usuario_id(self, obj):
        if obj.usuario_id:
            return {'id':obj.usuario_id.id, 'username':obj.usuario_id.username}
        return None
    
        
        
class SerializerBanco(serializers.ModelSerializer):
    
    class Meta:
        model = Banco
        fields = '__all__'
        
class SerializerTipoCuenta(serializers.ModelSerializer):
    
    class Meta:
        model = TipoCuenta
        fields = '__all__'
        
class SerializerCuenta(serializers.ModelSerializer):
    banco_id = serializers.PrimaryKeyRelatedField(
        queryset=Banco.objects.all(),
        source='banco', 
        write_only=True,  
    )
    tipocuenta_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoCuenta.objects.all(),
        source='tipocuenta', 
        write_only=True,  
    )
    banco = serializers.SerializerMethodField()
    tipocuenta = serializers.SerializerMethodField()
    class Meta:
        model = Cuenta
        fields = '__all__'
    
    def get_banco(self, obj):
        return {'id': obj.banco.id, 'nombre_banco':obj.banco.nombre_banco}
    
    def get_tipocuenta(self, obj):
        return {'id':obj.tipocuenta.id, 'nom_cuenta':obj.tipocuenta.nom_cuenta}
        
class SerializerPropietario(serializers.ModelSerializer):
    comuna_id= serializers.PrimaryKeyRelatedField(
        queryset=Comuna.objects.all(),
        source='comuna', 
        write_only=True,  
    )
    comuna = serializers.SerializerMethodField()
    
    def validate(self, data):
        rut_prop = data.get('rut_prop')
        if not validarRut(rut_prop):
            raise serializers.ValidationError("Rut inválido")
        return data
    
    class Meta:
        model = Propietario
        fields = '__all__'
        
    def get_comuna(self, obj):
        return {'id':obj.comuna.id, 'nom_comuna':obj.comuna.nom_com}
    

class SerializerPersonalidadJuridica(serializers.ModelSerializer):
    propietario_id = serializers.SerializerMethodField()
    class Meta:
        model = PersonalidadJuridica
        fields = '__all__'
     
    def get_propietario_id(self, obj):
        return{'id': obj.propietario_id.id, 'rut_prop': obj.propietario_id.rut_prop}  



class SerializerBodega(serializers.Serializer):
    numero_bodega = serializers.IntegerField()
    bodega_independiente = serializers.BooleanField()

class SerializerEstacionamiento(serializers.Serializer):
    numero_estacionamiento = serializers.IntegerField()
    estacionamiento_independiente = serializers.BooleanField()

class SerializerRegistroPropiedad(serializers.ModelSerializer):
    bodega = SerializerBodega(required=False, allow_null=True)
    estacionamiento = SerializerEstacionamiento(required=False, allow_null=True)
    class Meta:
        model = Propiedad
        fields = (
            'direccion_ppdd',
            'numero_ppdd',
            'rol_ppdd',
            'comuna',
            'propietario',
            'tipopropiedad',
            'bodega',
            'estacionamiento'
        ) 

class SerializerPropiedad(serializers.ModelSerializer):
    comuna_id= serializers.PrimaryKeyRelatedField(
        queryset=Comuna.objects.all(),
        source='comuna', 
        write_only=True,  
    )
    comuna = serializers.SerializerMethodField()

    tipopropiedad_id= serializers.PrimaryKeyRelatedField(
        queryset=TipoPropiedad.objects.all(),
        source='tipopropiedad', 
        write_only=True,  
    )
    tipopropiedad = serializers.SerializerMethodField()
    
    propietario_id= serializers.PrimaryKeyRelatedField(
        queryset=Propietario.objects.all(),
        source='propietario', 
        write_only=True,  
    )
    propietario = serializers.SerializerMethodField()    
    class Meta:
        model = Propiedad
        fields = '__all__'

    
    def get_comuna(self, obj):
        return {'id':obj.comuna.id, 'nom_comuna':obj.comuna.nom_com}
        
    def get_tipopropiedad(self, obj):
        return {'id': obj.tipopropiedad.id, 'nombre_tipoppdd': obj.tipopropiedad.nombre_tipoppdd}
    
    def get_propietario(self,obj):
        return{'id': obj.propietario.id, 
               'rut_prop':obj.propietario.rut_prop,
               'pri_nom_prop':obj.propietario.pri_nom_prop,
               'seg_nom_prop':obj.propietario.seg_nom_prop,
               'pri_ape_prop':obj.propietario.pri_ape_prop,
               'seg_ape_prop':obj.propietario.seg_ape_prop,
               }


 
class SerializerTipoPropiedad(serializers.ModelSerializer):
    
    class Meta:
        model = TipoPropiedad
        fields = '__all__'

class SerializerArrendatario(serializers.ModelSerializer):
    
    class Meta:
        model = Arrendatario
        fields = '__all__'
        
    def validate(self, data):
        rut_arr = data.get('rut_arr')
        if not validarRut(rut_arr):
            raise serializers.ValidationError("Rut inválido")
        return data
        
class SerializerArriendo(serializers.ModelSerializer):
    arrendatario_id= serializers.PrimaryKeyRelatedField(
        queryset=Arrendatario.objects.all(),
        source='arrendatario', 
        write_only=True,  
    )
    arrendatario = serializers.SerializerMethodField()   
     
    propiedad_id= serializers.PrimaryKeyRelatedField(
        queryset=Propiedad.objects.all(),
        source='propiedad', 
        write_only=True,  
    )
    propiedad = serializers.SerializerMethodField()    
    
    
    class Meta:
        model = Arriendo
        fields = '__all__'
        
    def get_arrendatario(self,obj):
        return{'id': obj.arrendatario.id, 
               'rut_arr':obj.arrendatario.rut_arr,
               'pri_nom_arr':obj.arrendatario.pri_nom_arr, 
               'pri_ape_arr':obj.arrendatario.pri_ape_arr,
               }
        

    def get_propiedad(self, obj):
        return {'id':obj.propiedad.id, 
                'direccion_ppdd': obj.propiedad.direccion_ppdd,
                'numero_ppdd': obj.propiedad.numero_ppdd
                }

class SerializerArriendoDepartamento(serializers.ModelSerializer):
    
    class Meta:
        model = ArriendoDepartamento
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

    