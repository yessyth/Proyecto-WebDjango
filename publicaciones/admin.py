from django.contrib import admin
from .models import Publicacion, Comentario

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'fecha_creacion']
    list_filter = ['categoria', 'fecha_creacion', 'autor']
    search_fields = ['titulo', 'contenido', 'autor__username']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'publicacion', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['contenido', 'autor__username', 'publicacion__titulo']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']