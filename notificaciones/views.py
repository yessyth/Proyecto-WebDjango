# notificaciones/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notificacion
from django.http import JsonResponse # Para marcar como leída con AJAX (opcional)

@login_required
def lista_notificaciones(request):
    # Opción 1: Marcar todas como leídas al ver la lista
    # request.user.notificaciones_recibidas.filter(leida=False).update(leida=True)
    
    # Opción 2: No marcar como leídas aquí, hacerlo con un botón/acción específica (ver abajo)
    
    notificaciones = request.user.notificaciones_recibidas.all() # Ya ordenadas por el Meta del modelo

    # Marcar como leídas solo las que se están mostrando (si decides hacerlo aquí)
    # Esta es una forma de hacerlo si no quieres marcarlas todas de golpe al cargar la página.
    # O puedes tener un botón "Marcar todas como leídas".
    # for notif in notificaciones:
    #     if not notif.leida:
    #         notif.leida = True
    #         notif.save() # Esto puede ser ineficiente para muchas notificaciones

    context = {
        'notificaciones_list': notificaciones # Renombrado para evitar conflicto con la app
    }
    return render(request, 'notificaciones/lista_notificaciones.html', context)

@login_required
def marcar_como_leida(request, notificacion_pk):
    notificacion = get_object_or_404(Notificacion, pk=notificacion_pk, destinatario=request.user)
    if not notificacion.leida:
        notificacion.leida = True
        notificacion.save()
    
    # Si la notificación tiene un enlace a una publicación, redirige allí
    if notificacion.publicacion_afectada:
        url_destino = notificacion.publicacion_afectada.get_absolute_url()
        # Si es un comentario, añade el ancla
        if notificacion.comentario_afectado:
            url_destino += f"#comentario-{notificacion.comentario_afectado.pk}"
        return redirect(url_destino)
        
    return redirect('lista_notificaciones') # Fallback

@login_required
def marcar_todas_como_leidas(request):
    request.user.notificaciones_recibidas.filter(leida=False).update(leida=True)
    # Para AJAX, podrías devolver una respuesta JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'message': 'Todas las notificaciones marcadas como leídas.'})
    return redirect('lista_notificaciones')