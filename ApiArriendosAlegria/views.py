from datetime import datetime
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from ApiArriendosAlegria.models import Banco
from ApiArriendosAlegria.serializers import SerializadorTokenUsuario
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


def load_data_bank(request):
    
    path = 'list-bank-chile.json'
    with open(path, 'r', encoding='utf-8-sig') as file:
        try:
            dataBank = json.load(file)
            msg = {"message": dataBank}
        except json.decoder.JSONDecodeError:
            msg = {'Error': "Error al abrir el archivo"}
            
    with transaction.atomic():        
        for data in dataBank:
            banks = Banco()
            # print(data)
            banks.nombre_banco = data['name']
            banks.cod_banco = data['code']
            time.sleep(1)
            banks.save()
    
    
    d = Banco.objects.all()
    print(d)
    
        
    
    return JsonResponse(msg)