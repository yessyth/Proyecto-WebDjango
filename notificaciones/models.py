# notificaciones/models.py
from django.db import models
from django.contrib.auth.models import User
# No necesitamos importar Publicacion o Comentario aquí directamente
# si usamos ForeignKey con strings de app_label.Modelo

class Notificacion(models.Model):
    NUEVO_COMENTARIO = 'NC'
    NUEVO_LIKE = 'NL'
    # Podrías añadir más tipos en el futuro, como 'NUEVA_RESPUESTA', 'NUEVO_SEGUIDOR', etc.

    TIPO_NOTIFICACION_CHOICES = [
        (NUEVO_COMENTARIO, 'Nuevo Comentario'),
        (NUEVO_LIKE, 'Nuevo Like'),
    ]

    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_recibidas') # Renombrado related_name
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificaciones_emitidas', null=True, blank=True)
    tipo = models.CharField(max_length=2, choices=TIPO_NOTIFICACION_CHOICES)
    
    # Usaremos ForeignKey con el nombre del modelo como string para evitar importaciones directas
    # Esto es útil si los modelos están en diferentes apps y quieres evitar importaciones circulares
    # o dependencias directas a nivel de modelo.
    publicacion_afectada = models.ForeignKey('publicaciones.Publicacion', on_delete=models.CASCADE, null=True, blank=True)
    comentario_afectado = models.ForeignKey('publicaciones.Comentario', on_delete=models.CASCADE, null=True, blank=True)
    
    mensaje = models.TextField(blank=True) # El mensaje se autogenerará
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"Notificación para {self.destinatario.username}: {self.get_tipo_display()} por {self.emisor.username if self.emisor else 'Sistema'}"

    def generar_mensaje(self):
        """Genera un mensaje legible para la notificación basado en su tipo y objetos relacionados."""
        msg = "Tienes una nueva notificación." # Mensaje por defecto
        if self.emisor:
            if self.tipo == self.NUEVO_COMENTARIO and self.publicacion_afectada and self.comentario_afectado:
                msg = f"{self.emisor.username} comentó en tu publicación: \"{self.publicacion_afectada.titulo}\""
            elif self.tipo == self.NUEVO_LIKE and self.publicacion_afectada:
                msg = f"A {self.emisor.username} le gustó tu publicación: \"{self.publicacion_afectada.titulo}\""
        # Puedes añadir más condiciones para otros tipos de notificaciones
        return msg

    def save(self, *args, **kwargs):
        if not self.mensaje: # Solo genera el mensaje si no se ha establecido uno explícitamente
            self.mensaje = self.generar_mensaje()
        super().save(*args, **kwargs)