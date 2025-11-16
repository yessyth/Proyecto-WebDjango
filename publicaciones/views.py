from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Publicacion, Comentario
from .forms import PublicacionForm, ComentarioForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

def lista_publicaciones(request):
    publicaciones_list = Publicacion.objects.all() # Ya está ordenado por el Meta del modelo
    
    categoria = request.GET.get('categoria')
    busqueda = request.GET.get('buscar')
    
    if categoria and categoria != 'todos':
        publicaciones_list = publicaciones_list.filter(categoria=categoria)
    
    if busqueda:
        publicaciones_list = publicaciones_list.filter(
            Q(titulo__icontains=busqueda) | 
            Q(contenido__icontains=busqueda) |
            Q(autor__username__icontains=busqueda)
        )
    
    # Configuración de Paginación
    paginator = Paginator(publicaciones_list, 9) # Muestra 9 publicaciones por página (ajusta según necesites)
    page_number = request.GET.get('page')
    try:
        publicaciones_page = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page no es un entero, entrega la primera página.
        publicaciones_page = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango (ej. 9999), entrega la última página de resultados.
        publicaciones_page = paginator.page(paginator.num_pages)

    categorias_choices = Publicacion._meta.get_field('categoria').choices
    
    context = {
        'publicaciones': publicaciones_page, # <--- PASAR EL OBJETO DE PÁGINA
        'is_paginated': True,              # <--- INDICAR QUE HAY PAGINACIÓN
        'page_obj': publicaciones_page,    # <--- EL TEMPLATE ESPERA page_obj
        'categorias_choices': categorias_choices,
        'categoria_actual': categoria,
        'busqueda_actual': busqueda
    }
    return render(request, 'publicaciones/lista.html', context)

# ... el resto de tus vistas ...

# publicaciones/views.py
def detalle_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    comentarios = publicacion.comentarios.all().order_by('-fecha_creacion') # Ordenar más nuevos primero
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.publicacion = publicacion
            comentario.autor = request.user
            comentario.save()
            return redirect('detalle_publicacion', pk=pk) # Redirige a la misma página para ver el comentario
    else:
        form = ComentarioForm() # Formulario vacío para GET o si el POST falla
    
    context = {
        'publicacion': publicacion,
        'comentarios': comentarios,
        'form_comentario': form # Renombrado para claridad en el template
    }
    return render(request, 'publicaciones/detalle.html', context)
@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('detalle_publicacion', pk=publicacion.pk)
    else:
        form = PublicacionForm()
    return render(request, 'publicaciones/formulario.html', {'form': form, 'titulo': 'Crear Publicación'})

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_publicacion', pk=pk)
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'publicaciones/formulario.html', {
        'form': form, 
        'titulo': 'Editar Publicación',
        'publicacion': publicacion
    })

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, autor=request.user)
    if request.method == 'POST':
        publicacion.delete()
        return redirect('lista_publicaciones')
    return render(request, 'publicaciones/confirmar_eliminar.html', {'publicacion': publicacion})

@login_required
def editar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('detalle_publicacion', pk=comentario.publicacion.pk)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, 'publicaciones/editar_comentario.html', {
        'form': form,
        'comentario': comentario
    })

@login_required
def eliminar_comentario(request, pk):
    comentario = get_object_or_404(Comentario, pk=pk, autor=request.user)
    publicacion_pk = comentario.publicacion.pk
    if request.method == 'POST':
        comentario.delete()
        return redirect('detalle_publicacion', pk=publicacion_pk)
    return render(request, 'publicaciones/confirmar_eliminar_comentario.html', {'comentario': comentario})

# publicaciones/views.py
# ... (otros imports) ..

# ... (tus otras vistas: lista_publicaciones, detalle_publicacion, etc.) ...

@login_required
def dar_like_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    user = request.user
    liked = False

    if publicacion.likes.filter(id=user.id).exists():
        # El usuario ya le dio like, entonces se lo quitamos
        publicacion.likes.remove(user)
        liked = False
    else:
        # El usuario no le ha dado like, entonces se lo añadimos
        publicacion.likes.add(user)
        liked = True
    
    # Opcional: Si quieres una respuesta JSON para AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'liked': liked, 'count': publicacion.total_likes()})

    # Redirigir a la página anterior o a una específica (ej. detalle)
    # Usar HTTP_REFERER es común pero puede no ser siempre fiable o seguro
    # return redirect(request.META.get('HTTP_REFERER', 'detalle_publicacion')) 
    return redirect('detalle_publicacion', pk=publicacion.pk) # Redirige al detalle