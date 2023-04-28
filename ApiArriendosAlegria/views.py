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
from ApiArriendosAlegria.models import Usuario, Banco, Region, Comuna, TipoCuenta, Trabajador, TipoTrabajador
from ApiArriendosAlegria.serializers import SerializadorUsuario, SerializadorTokenUsuario, serializerBanco, serializerRegion, serializerComuna, serializerTipoTrabajado, serializerTrabajador,\
                serializerTipoCuenta
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
        regiones_srz = serializerRegion(regiones, many = True)
        return Response(regiones_srz.data, status=status.HTTP_200_OK)

#-----Api Banks only method get
@api_view(['GET'])
def get_api_banks(request):
    #List Banks
    if request.method == 'GET':
        bancos = Banco.objects.all()
        bancos_srz = serializerBanco(bancos, many = True)
        return Response(bancos_srz.data, status=status.HTTP_200_OK)

#-----Api TypeAccountsBanks only method get
@api_view(['GET'])
def get_api_TypeAccountsBanks(request):
    #List TypeAccounts
    if request.method == 'GET':
        typeAcounts = TipoCuenta.objects.all()
        typeAcounts_srz = serializerTipoCuenta(typeAcounts, many = True)
        return Response(typeAcounts_srz.data, status=status.HTTP_200_OK)
    
    
#-----Api Crud TypeWorkers
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
@authentication_classes([Authentication])
def get_post_api_CrudTyperWorkers(request):
    # List typeWorkers
    if request.method == 'GET':
        typerWorkers = TipoTrabajador.objects.all()
        typerWorkers_srz = serializerTipoTrabajado(typerWorkers, many = True)
        return Response(typerWorkers_srz.data, status=status.HTTP_200_OK)
    #Create typeWorkers
    elif request.method == 'POST':
        typerWorkers_srz = serializerTipoTrabajado(data=request.data)
        if typerWorkers_srz.is_valid():
            typerWorkers_srz.save()
            return Response(typerWorkers_srz.data, status=status.HTTP_201_CREATED)
        return Response(typerWorkers_srz.errors, status=status.HTTP_400_BAD_REQUEST)

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
            typerWorkers_srz = serializerTipoTrabajado(typerWorkers)
            return Response(typerWorkers_srz.data, status=status.HTTP_200_OK)
        # update typeWorker
        elif request.method == 'PUT':
            typerWorkers_srz = serializerTipoTrabajado(typerWorkers, data=request.data)
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
    serializer_class = serializerTipoTrabajado
    queryset = TipoTrabajador.objects.all()




# -------------Api Worker---------------
class TrabajadorViewSet(viewsets.ModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    serializer_class = serializerTrabajador
    queryset = Trabajador.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        rut_trab = request.query_params.get('rut_trab', None)
        pri_nom_trab = request.query_params.get('pri_nom_trab', None)
        
        if rut_trab:
            queryset = queryset.filter(rut_trab=rut_trab)
        if pri_nom_trab:
            queryset = queryset.filter(pri_nom_trab=pri_nom_trab)

        if queryset.exists():
            serializer = serializerTrabajador(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("No se encontraron trabajadores", status=status.HTTP_400_BAD_REQUEST)
    
# -------------Api Communes---------------    
class ComunaReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated, IsStaffUser]
    queryset = Comuna.objects.all()
    serializer_class = serializerComuna
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
