from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from ApiArriendosAlegria.authentication import ExpiringTokenAuthentication

class Authentication(authentication.BaseAuthentication):
    """
    Módulo base de autenticación de usuarios, que permite la autenticación
    mediante sistema de tokens de Django REST Framework.
    """
    def authenticate(self, request):
        token = get_authorization_header(request).split()
        
        if not token:
            raise exceptions.AuthenticationFailed('No hay token en la petición.')
        
        try:
            token = token[1].decode()
        except:
            raise exceptions.AuthenticationFailed('El token es inválido o está dañado.')
    
        token_expire = ExpiringTokenAuthentication()
        user = token_expire.authenticate_credentials(token)

        return (user, 1)
