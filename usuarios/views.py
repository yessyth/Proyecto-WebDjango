from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import Perfil
from .forms import PerfilForm
from publicaciones.models import Publicacion

def inicio(request):
    ultimas_publicaciones = Publicacion.objects.all().order_by('-id')[:7] 

    context = {
        'ultimas_publicaciones': ultimas_publicaciones,
    }
    return render(request, 'usuarios/inicio.html', context)

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/registro.html', {'form': form})

# AUTOMOVILISMO/usuarios/views.py


@login_required
def perfil(request):
    # Obtenemos el objeto Perfil. get_or_create es bueno por si acaso.
    perfil_obj, creado = Perfil.objects.get_or_create(user=request.user)
    
    # Obtenemos las publicaciones hechas por este usuario
    # Ordenadas por la más reciente (asumiendo -id o -fecha_creacion)
    publicaciones_usuario = Publicacion.objects.filter(autor=request.user).order_by('-id')
    
    context = {
        'perfil_usuario': perfil_obj, # Pasamos el objeto Perfil
        'publicaciones_usuario': publicaciones_usuario
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    perfil_obj, creado = Perfil.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil_obj)
        if form.is_valid():
            form.save()
            # Redirigir a la vista de perfil después de editar con éxito
            return redirect('perfil') # Cambiado de 'inicio' a 'perfil'
    else:
        form = PerfilForm(instance=perfil_obj)

    return render(request, 'usuarios/editar_perfil.html', {'form': form})