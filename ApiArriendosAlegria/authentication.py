from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import timezone

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Autenticación de credenciales mediante token (authtoken) con tiempo de expiración.
    """
    token_expired = False

    def expires_in(self, token):
        # Tiempo que falta para que el token expire.
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRE_TIME_IN_SECONDS) - time_elapsed
        return left_time


    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds=0)


    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)

        if is_expire:
            user = token.user
            self.token_expired = True
            # Delete all sessions for user
            all_sessions = Session.objects.filter(
                expire_date__gte=datetime.now())
            if all_sessions.exists():
                for session in all_sessions:
                    session_data = session.get_decoded()
                    # auth_user_id is the primary key's user on the session
                    if user.id == int(session_data.get('_auth_user_id')):
                        session.delete()
            token.delete()
            
        return is_expire, token


    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token inválido.')
        
        if token is not None:
            if not token.user.is_active:
                raise exceptions.AuthenticationFailed('Usuario inactivo o eliminado.')
        
        is_expired, token = self.token_expire_handler(token)
        

        if is_expired == True:
            raise exceptions.AuthenticationFailed('Token expirado. Se ha cerrado la sesión activa.')
        
        return token.user
    