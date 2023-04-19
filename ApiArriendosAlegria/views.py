from datetime import datetime
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from ApiArriendosAlegria.models import Banco, Region, Comuna
from ApiArriendosAlegria.serializers import SerializadorTokenUsuario, serializerBanco, serializerRegion, serializerComuna, serializerTipoTrabajado, serializerTrabajador
from django.db import transaction

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
                if created:
                    return Response({
                        'Token': token.key,
                        'Usuario': user_serializer.data,
                        'Mensaje': 'Ingreso exitoso'
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
                    return Response({'ERROR': 'Este usuario ya ha ingresado'})

            return Response({'ERROR': 'No se puede ingresar con usuario inactivo'},
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response({'ERROR': 'Usuario o contraseña incorrecta'},
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

                token_message = 'Token eliminado'
                session_message = 'Todas las sesiones exitosamente cerradas'
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


#-----Api Comunas filtered by id_reg only method get
@api_view(['GET'])
def get_api_comunas_by_id_reg(request, id_reg):
    comunas = Comuna.objects.filter(reg_id = id_reg)
    if comunas:
        if request.method == 'GET':
            comunas_srz = serializerComuna(comunas, many = True)
            return Response(comunas_srz.data, status=status.HTTP_200_OK)
    return Response({'message':f'Comunas with ID: {id_reg} not found'}, status=status.HTTP_400_BAD_REQUEST)

#-----Api Banks only method get
@api_view(['GET'])
def get_api_banks(request):
    #List Banks
    if request.method == 'GET':
        bancos = Banco.objects.all()
        bancos_srz = serializerBanco(bancos, many = True)
        return Response(bancos_srz.data, status=status.HTTP_200_OK)

