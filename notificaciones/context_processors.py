# notificaciones/context_processors.py
from .models import Notificacion # Importa desde la app actual

def contador_notificaciones_no_leidas(request):
    if request.user.is_authenticated:
        count = Notificacion.objects.filter(destinatario=request.user, leida=False).count()
        return {'notificaciones_no_leidas_count': count}
    return {}