from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ApiArriendosAlegria.models import Usuario
from ApiArriendosAlegria.serializers import SerializadorUsuario


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def user_api_view(request):

    # List
    if request.method == 'GET':
        # Queryset
        users = Usuario.objects.all()
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


@api_view(['GET', 'PUT', 'DELETE'])
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
