from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_publicaciones, name='lista_publicaciones'),
    path('<int:pk>/', views.detalle_publicacion, name='detalle_publicacion'),
    path('nueva/', views.crear_publicacion, name='crear_publicacion'),
    path('<int:pk>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('<int:pk>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('comentario/<int:pk>/editar/', views.editar_comentario, name='editar_comentario'),
    path('comentario/<int:pk>/eliminar/', views.eliminar_comentario, name='eliminar_comentario'),
    path('publicacion/<int:pk>/like/', views.dar_like_publicacion, name='dar_like_publicacion'),
]