from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

CATEGORIAS_CHOICES = [
    ('f1', 'Fórmula 1'),
    ('rally', 'Rally'),
    ('tuning', 'Tuning'),
    ('clasicos', 'Clásicos'),
    ('supercar', 'Supercars'),
    ('electrico', 'Eléctricos'),
    ('motorsport', 'Motorsport'),
    ('otros', 'Otros'),
]

class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS_CHOICES, default='otros')
    imagen = models.ImageField(upload_to='publicaciones/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='publicaciones_gustadas', blank=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.titulo
    def get_absolute_url(self):
        # Asume que tienes una URL nombrada 'detalle_publicacion' en tu urls.py
        # que espera un parámetro 'pk' (la clave primaria de la publicación).
        return reverse('detalle_publicacion', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()

class Comentario(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.publicacion.titulo}'