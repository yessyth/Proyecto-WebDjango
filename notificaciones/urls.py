# notificaciones/urls.py
from django.urls import path
from . import views

app_name = 'notificaciones' # Es buena práctica definir un app_name

urlpatterns = [
    path('', views.lista_notificaciones, name='lista'),
    path('marcar-leida/<int:notificacion_pk>/', views.marcar_como_leida, name='marcar_leida'),
    path('marcar-todas-leidas/', views.marcar_todas_como_leidas, name='marcar_todas_leidas'),
]