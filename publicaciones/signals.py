# publicaciones/signals.py
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Comentario, Publicacion # Modelos de la app actual (publicaciones)
from notificaciones.models import Notificacion # <--- IMPORTA EL MODELO DE LA APP NOTIFICACIONES

@receiver(post_save, sender=Comentario)
def notificar_nuevo_comentario(sender, instance, created, **kwargs):
    if created:
        comentario = instance
        publicacion = comentario.publicacion
        autor_publicacion = publicacion.autor
        
        # Evitar auto-notificaciones
        if comentario.autor != autor_publicacion:
            Notificacion.objects.create(
                destinatario=autor_publicacion,
                emisor=comentario.autor,
                tipo=Notificacion.NUEVO_COMENTARIO,
                publicacion_afectada=publicacion,
                comentario_afectado=comentario
                # El mensaje se generará automáticamente por el método save() de Notificacion
            )

@receiver(m2m_changed, sender=Publicacion.likes.through)
def notificar_nuevo_like(sender, instance, action, pk_set, **kwargs):
    """
    Crea una notificación cuando se añade un nuevo "Me Gusta".
    """
    if action == "post_add": # Se ejecuta después de que se hayan añadido los usuarios al ManyToManyField
        publicacion_likeada = instance # 'instance' es el objeto Publicacion
        autor_publicacion = publicacion_likeada.autor
        
        for user_pk in pk_set: # pk_set contiene los pks de los User que dieron like
            emisor_del_like = User.objects.get(pk=user_pk)
            
            # Evitar auto-notificaciones (si el autor se da like a sí mismo)
            if emisor_del_like != autor_publicacion:
                # Opcional: Podrías añadir una lógica para no enviar demasiadas notificaciones de like
                # por la misma publicación y usuario en un corto periodo de tiempo, o agruparlas.
                # Por ahora, creamos una por cada nuevo like que no sea del autor.
                if not Notificacion.objects.filter(
                    destinatario=autor_publicacion,
                    emisor=emisor_del_like,
                    tipo=Notificacion.NUEVO_LIKE,
                    publicacion_afectada=publicacion_likeada
                ).exists(): # Evita duplicados exactos si la lógica de like pudiera llamarse múltiples veces
                    Notificacion.objects.create(
                        destinatario=autor_publicacion,
                        emisor=emisor_del_like,
                        tipo=Notificacion.NUEVO_LIKE,
                        publicacion_afectada=publicacion_likeada
                    )