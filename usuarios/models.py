# AUTOMOVILISMO/usuarios/models.py
from django.db import models
from django.contrib.auth.models import User
# from .models import Perfil  <--- ELIMINA ESTA LÍNEA

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True, default='fotos_perfil/default.png')
    autos_favoritos = models.CharField(max_length=200, blank=True, null=True)
    foto_portada = models.ImageField(upload_to='fotos_portada/', blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'

# Otros modelos que puedas tener en usuarios/models.py ...