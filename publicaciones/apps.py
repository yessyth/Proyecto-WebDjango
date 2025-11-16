# publicaciones/apps.py
from django.apps import AppConfig

class PublicacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'publicaciones'

    def ready(self):
        import publicaciones.signals # Esto registrará las señales definidas en signals.py