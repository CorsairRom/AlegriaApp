from datetime import datetime

from django.contrib.sessions.models import Session
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated

from ApiArriendosAlegria.models import (
    Usuario,
    Trabajador,
    TipoTrabajador,
    Region,
    Comuna,
    Banco,
    TipoCuenta,
    Cuenta,
    Propiedad,
    TipoPropiedad,
    Propietario,
    PersonalidadJuridica,
    Arrendatario,
    Arriendo,
    DetalleArriendo,
    Gastocomun,
    ServiciosExtras,
    ArriendoDepartamento,
)
from ApiArriendosAlegria.serializers import (
    SerializadorUsuario,
    SerializerArriendoDepartamento,
    SerializerTrabajador,
    SerializerTipoTrabajado,
    SerializerRegion,
    SerializerComuna,
    SerializerBanco,
    SerializerTipoCuenta,
    SerializerCuenta,
    SerializerPropiedad,
    SerializerPersonalidadJuridica,
    SerializerTipoPropiedad,
    SerializerPropietario,
    SerializerArrendatario,
    SerializerArriendo,
    SerializerDetalleArriendo,
    SerializerGastoComun,
    SerializerServiciosExtas,
)
# from django.db import transaction
from ApiArriendosAlegria.permission import IsStaffUser
from ApiArriendosAlegria.authentication_mixins import Authentication



# --- General views: Login / Logout ---
class Login(ObtainAuthToken):
    """
    Vista Login.

    Usa autenticación de token propia de Django REST Framework (Authtoken).

    Se admite sólo una sesión activa por usuario. Dicha sesión se destruye
    si se repite la petición POST con la sesión ya iniciada.
    """
    def post(self, request, *args, **kwargs):

        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})
        
        if not login_serializer.is_valid():
            return Response({'error': 'Usuario o contraseña incorrecta'},
                        status=status.HTTP_400_BAD_REQUEST)

        user = login_serializer.validated_data['user']
        if not user.is_active:
            return Response({'error': 'No se puede ingresar con usuario inactivo'},
                        status=status.HTTP_401_UNAUTHORIZED)
        
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = SerializadorUsuario(user)

        if not created:
            # Delete user token
            token.delete()
            # Delete all sessions for user
            all_sessions = Session.objects.filter(
                expire_date__gte=datetime.now())
            
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    # auth_user_id is the primary key's user on the session
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()

            return Response({'error': 'Su sessión quedo activa desde la última vez. Por favor ingrese nuevamente.'},
                            status=status.HTTP_400_BAD_REQUEST
                            )
    
        return Response({
                    'token': token.key,
                    'usuario': user_serializer.data,
                    'message': 'Ingreso exitoso.'
                }, status=status.HTTP_201_CREATED)

        

        

class Logout(APIView):
    """
    Vista Logout.
    
    Logout mediante authtoken de Django REST Framework.
    """
    def post(self, request, *args, **kwargs):
        try:
            token_request = request.GET.get('token')
            token = Token.objects.filter(key=token_request).first()

            if not token:
                return Response({'error': 'No hay usuario con ese token'},
                            status=status.HTTP_400_BAD_REQUEST)
            
            user = token.user

            token.delete()
            # Delete all sessions for user
            all_sessions = Session.objects.filter(
                expire_date__gte=datetime.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    # auth_user_id is the primary key's user on the session
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()
            # Delete user token

            token_message = 'Token eliminado.'
            session_message = 'Sesión exitosamente cerrada.'

            return Response({'token_message': token_message,
                            'session_message': session_message},
                            status=status.HTTP_200_OK)

        except:
            return Response({'error': 'No se ha encontrado el token ingresado'},
                            status=status.HTTP_409_CONFLICT)     
            
            

# -------------Api Bancos---------------
class BancoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista "Banco".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerBanco
    queryset = Banco.objects.all()

# -------------Api Tipo Cuentas Bancarias---------------
class TipoCuentaBancariaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista "Tipo Cuenta" (Bancaria).

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SerializerTipoCuenta
    queryset = TipoCuenta.objects.all()


# -------------Api TypeWorkers---------------
class TypeWorkerViewSet(viewsets.ModelViewSet):
    """
    Vista "Tipo Trabajador".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTipoTrabajado
    queryset = TipoTrabajador.objects.all()


# -------------Api Worker---------------
class TrabajadorViewSet(viewsets.ModelViewSet):
    """
    Vista "Trabajador".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTrabajador
    queryset = Trabajador.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut_trab', 'pri_nom_trab']

    
# -------------Api Regiones--------------- 
class RegionReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista "Region".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    queryset = Region.objects.all()
    serializer_class = SerializerRegion
    filter_backends = [DjangoFilterBackend]

# -------------Api Communes---------------   
class ComunaReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vista "Comuna".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    queryset = Comuna.objects.all()
    serializer_class = SerializerComuna
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reg_id']


# --- API Usuario (nuevo) ---
class UsuarioViewSet(viewsets.ModelViewSet):
    """
    Vista "Usuario".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializadorUsuario
    queryset = Usuario.objects.all()


# ---------------------Segundo sprint-------------------
class PropietarioViewSet(viewsets.ModelViewSet):
    """
    Vista "Propietario".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPropietario
    queryset = Propietario.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut_prop','pri_nom_prop','pri_ape_prop']
    
    
class PersonalidadJuridicaViewSet(viewsets.ModelViewSet):
    """
    Vista "Personalidad Jurídica".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPersonalidadJuridica
    queryset = PersonalidadJuridica.objects.all()


class CuentaViewSet(viewsets.ModelViewSet):
    """
    Vista "Cuenta".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerCuenta
    queryset = Cuenta.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cuenta','propietario_rut']

class PropiedadViewSet(viewsets.ModelViewSet):
    """
    Vista "Propiedad".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPropiedad
    queryset = Propiedad.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['propietario']


class TipoPropiedadViewSet(viewsets.ModelViewSet):
    """
    Vista "Tipo Propiedad".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTipoPropiedad
    queryset = TipoPropiedad.objects.all()

class ArriendatarioViewSet(viewsets.ModelViewSet):
    """
    Vista "Arrendatario".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArrendatario
    queryset = Arrendatario.objects.all()
    
class ArriendoViewSet(viewsets.ModelViewSet):
    """
    Vista "Arriendo".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArriendo
    queryset = Arriendo.objects.all()
    
    
class ArriendoDepartamentoViewSet(viewsets.ModelViewSet):
    """
    Vista "Arriendo departamento".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArriendoDepartamento
    queryset = ArriendoDepartamento.objects.all()
    


class DetalleArriendoViewSet(viewsets.ModelViewSet):
    """
    Vista "Detalle Arriendo".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerDetalleArriendo
    queryset = DetalleArriendo.objects.all()

class ServiciosExtrasViewSet(viewsets.ModelViewSet):
    """
    Vista "Servicios Extra".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerServiciosExtas
    queryset = ServiciosExtras.objects.all()
    
class GastoComunViewSet(viewsets.ModelViewSet):
    """
    Vista "Gastos Comun".

    Métodos disponibles: list, create, retrieve, update, destroy.
    """
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerGastoComun
    queryset = Gastocomun.objects.all()
