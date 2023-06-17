from datetime import datetime

from django.contrib.sessions.models import Session
from django.utils import timezone

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from django.conf import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Autenticación de credenciales mediante token (authtoken)
    con tiempo de expiración.
    """
    token_expired = False

    def is_token_expired(self):
        current_time = timezone.localtime(timezone.now()).time()
        expiration_time = settings.DAILY_TOKEN_EXPIRATION_TIME  # Aquí puedes definir la hora de muerte diaria del token.
        
        token_is_expired = current_time > expiration_time

        return token_is_expired


    def authenticate_credentials(self, key):
        model = self.get_model()

        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Token inválido.')
        
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('Usuario inactivo o eliminado.')

        if self.is_token_expired():
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
            raise exceptions.AuthenticationFailed('Token expirado. Se ha cerrado la sesión activa.')
        
        return token.user
    