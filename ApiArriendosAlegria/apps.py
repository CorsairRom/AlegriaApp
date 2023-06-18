from django.apps import AppConfig


class ApiarriendosalegriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ApiArriendosAlegria'

    def ready(self) -> None:
        import ApiArriendosAlegria.signals
