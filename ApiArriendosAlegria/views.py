from datetime import datetime
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from ApiArriendosAlegria.models import Usuario, Banco, Region, Comuna, TipoCuenta, Trabajador, TipoTrabajador, Propiedad, Propietario, TipoPropiedad, Arrendatario,\
                                        Arriendo, DetalleArriendo, Cuenta,Gastocomun,PersonalidadJuridica, ServiciosExtras
from ApiArriendosAlegria.serializers import SerializadorUsuario, SerializadorTokenUsuario, SerializerBanco, SerializerRegion, SerializerComuna, SerializerTipoTrabajado,\
                                            SerializerTrabajador, SerializerTipoCuenta, SerializerPropietario, SerializerPropiedad, SerializerCuenta, SerializerArrendatario,\
                                            SerializerArriendo, SerializerDetalleArriendo, SerializerGastoComun, SerializerPersonalidadJuridica, SerializerServiciosExtas,\
                                            SerializerTipoPropiedad, ServiciosExtras
# from django.db import transaction
from ApiArriendosAlegria.permission import IsAdminUser, IsStaffUser
from ApiArriendosAlegria.authentication_mixins import Authentication
import time
import json


# Create your views here.
class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(
            data=request.data, context={'request': request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = SerializadorTokenUsuario(user)
                trabajador = Trabajador.objects.get(usuario_id = user.id)
                trabajador_tipo = trabajador.tipo_trab
                if created:
                    return Response({
                        'token': token.key,
                        'usuario': user_serializer.data,
                        'tipo_trabajador': trabajador_tipo.id,
                        'message': 'Ingreso exitoso.'
                    }, status=status.HTTP_201_CREATED)
                else:
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
                    return Response({'error': 'Este usuario ya ha ingresado. Se cerrará la sesión activa.'})

            return Response({'error': 'No se puede ingresar con usuario inactivo'},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response({'error': 'Usuario o contraseña incorrecta'},
                        status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def post(self, request, *args, **kwargs):
        try:
            token_request = request.GET.get('token')
            token = Token.objects.filter(key=token_request).first()

            if token:
                user = token.user
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
                token.delete()

                token_message = 'Token eliminado.'
                session_message = 'Sesión exitosamente cerrada.'
                return Response({'token_message': token_message,
                                'session_message': session_message},
                                status=status.HTTP_200_OK)

            return Response({'ERROR': 'No hay usuario con ese token'},
                            status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'ERROR': 'No se ha encontrado el token ingresado'},
                            status=status.HTTP_409_CONFLICT)
            
            
#-----Api Regiones only method get
@api_view(['GET'])
def get_api_regions(request):
    #List regions
    if request.method == 'GET':
        regiones = Region.objects.all()
        regiones_srz = SerializerRegion(regiones, many = True)
        return Response(regiones_srz.data, status=status.HTTP_200_OK)

#-----Api Banks only method get
@api_view(['GET'])
def get_api_banks(request):
    #List Banks
    if request.method == 'GET':
        bancos = Banco.objects.all()
        bancos_srz = SerializerBanco(bancos, many = True)
        return Response(bancos_srz.data, status=status.HTTP_200_OK)

#-----Api TypeAccountsBanks only method get
@api_view(['GET'])
def get_api_TypeAccountsBanks(request):
    #List TypeAccounts
    if request.method == 'GET':
        typeAcounts = TipoCuenta.objects.all()
        typeAcounts_srz = SerializerTipoCuenta(typeAcounts, many = True)
        return Response(typeAcounts_srz.data, status=status.HTTP_200_OK)
    
    
#-----Api Crud TypeWorkers <- deprecated
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
@authentication_classes([Authentication])
def get_post_api_CrudTyperWorkers(request):
    # List typeWorkers
    if request.method == 'GET':
        typerWorkers = TipoTrabajador.objects.all()
        typerWorkers_srz = SerializerTipoTrabajado(typerWorkers, many = True)
        return Response(typerWorkers_srz.data, status=status.HTTP_200_OK)
    #Create typeWorkers
    elif request.method == 'POST':
        typerWorkers_srz = SerializerTipoTrabajado(data=request.data)
        if typerWorkers_srz.is_valid():
            typerWorkers_srz.save()
            return Response(typerWorkers_srz.data, status=status.HTTP_201_CREATED)
        return Response(typerWorkers_srz.errors, status=status.HTTP_400_BAD_REQUEST)
    
# <- deprecated
@permission_classes([IsAuthenticated])    
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([Authentication])
def get_put_delete_CrudTyperWorkers(request, tpTrab_id):
    # queryset of typeWorker
    typerWorkers = TipoTrabajador.objects.filter(id=tpTrab_id).first()
    if typerWorkers:
        # obtain a name for the typeWorker
        tipoName = typerWorkers.tipo
        # retrieve typeWorker
        if request.method == 'GET':
            typerWorkers_srz = SerializerTipoTrabajado(typerWorkers)
            return Response(typerWorkers_srz.data, status=status.HTTP_200_OK)
        # update typeWorker
        elif request.method == 'PUT':
            typerWorkers_srz = SerializerTipoTrabajado(typerWorkers, data=request.data)
            if typerWorkers_srz.is_valid():
                typerWorkers_srz.save()
                return Response(typerWorkers_srz.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            typerWorkers.delete()
            return Response({'message' : f'TypeWorker ID : {tpTrab_id} deleted'}, status=status.HTTP_200_OK)
    return Response({'message': f"TypeWorker ID:{tpTrab_id} not have TypeWorker"}, status=status.HTTP_400_BAD_REQUEST) #fix detail with name


# -------------Api TypeWorkers---------------
class TypeWorkerViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTipoTrabajado
    queryset = TipoTrabajador.objects.all()




# -------------Api Worker---------------
class TrabajadorViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTrabajador
    queryset = Trabajador.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut_trab', 'pri_nom_trab']

    
# -------------Api Communes---------------    
class ComunaReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    queryset = Comuna.objects.all()
    serializer_class = SerializerComuna
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['reg_id']


# --- API view Usuario (lista) ---
@api_view(['GET', 'POST'])
@authentication_classes([Authentication])
@permission_classes([permissions.IsAuthenticated])
def user_api_view(request):

    # List
    if request.method == 'GET':
        # Queryset: devuelve todos los usuarios normales (no superuser)
        users = Usuario.objects.all().filter(is_superuser=False).order_by('id')
        users_serializer = SerializadorUsuario(users, many=True)

        return Response(users_serializer.data, status=status.HTTP_200_OK)

    # Create
    elif request.method == 'POST':
        users_serializer = SerializadorUsuario(data=request.data)
        
        # Validation
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- API view Usuario (detalle) ---
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([Authentication])
@permission_classes([permissions.IsAuthenticated])
def user_detail_api_view(request, pk=None):
    # Queryset
    user = Usuario.objects.filter(id=pk).first()

    # Validation
    if user:

        # Retrieve
        if request.method == 'GET':
            user_serializer = SerializadorUsuario(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        # Update
        elif request.method == 'PUT':
            user_serializer = SerializadorUsuario(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario eliminado'}, status=status.HTTP_200_OK)
    
    return Response({'message': 'No se ha encontrado un usuario con esos datos'}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------Segundo sprint-------------------
class PropietarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPropietario
    queryset = Propietario.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rut_prop','pri_nom_prop','pri_ape_prop']
    
    
class PersonalidadJuridicaViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPersonalidadJuridica
    queryset = PersonalidadJuridica.objects.all()

class CuentaViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerCuenta
    queryset = Cuenta.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cuenta','propietario_rut']
    
    
    

class PropiedadViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerPropiedad
    queryset = Propiedad.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['propietario_id']
    
    
    
class TipoPropiedadViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerTipoPropiedad
    queryset = TipoPropiedad.objects.all()

class ArriendatarioViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArrendatario
    queryset = Arrendatario.objects.all()
    
class ArriendoViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerArriendo
    queryset = Arriendo.objects.all()

class DetalleArriendoViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerDetalleArriendo
    queryset = DetalleArriendo.objects.all()

class ServiciosExtrasViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerServiciosExtas
    queryset = ServiciosExtras.objects.all()
    
class GastoComunViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = SerializerGastoComun
    queryset = Gastocomun.objects.all()
