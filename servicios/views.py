# servicios/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required # Para requerir que el usuario esté logueado
from django.contrib.admin.views.decorators import staff_member_required # Para requerir que el usuario sea staff (admin)
from django.contrib import messages # Para enviar mensajes de éxito/error

from .models import Servicio, InscripcionCurso # Importamos el nuevo modelo InscripcionCurso
# Necesitarás crear estos formularios en servicios/forms.py
from .forms import InscripcionCursoForm, ServicioForm


# --- VISTAS PÚBLICAS (EXISTENTES Y MODIFICADAS) ---

def lista_servicios(request):
    """
    Muestra el único curso/servicio disponible al público.
    """
    curso = Servicio.objects.filter(disponible=True).first()
    context = {
        'curso': curso,
        'titulo_pagina': 'Curso Presencial',
    }
    return render(request, 'servicios/lista_servicios.html', context)

def detalle_servicio(request, slug):
    """
    Muestra los detalles de un curso/servicio específico y maneja el formulario de inscripción.
    """
    servicio = get_object_or_404(Servicio, slug=slug, disponible=True)
    form = InscripcionCursoForm() # Usamos el nuevo formulario de inscripción

    if request.method == 'POST':
        form = InscripcionCursoForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False) # Guardamos el formulario sin guardarlo aún en la DB
            inscripcion.curso = servicio # Asignamos el curso a la inscripción
            inscripcion.save() # Ahora sí, guardamos la inscripción en la DB
            messages.success(request, '¡Tu inscripción ha sido enviada con éxito! Nos pondremos en contacto contigo pronto.')
            # Redirigimos para evitar reenvío del formulario al recargar
            return redirect('servicios:detalle_servicio', slug=servicio.slug)
        else:
            messages.error(request, 'Hubo un error al procesar tu inscripción. Por favor, revisa los datos.')

    context = {
        'servicio': servicio,
        'form': form,
        'titulo_pagina': servicio.nombre,
    }
    return render(request, 'servicios/detalle_servicio.html', context)


# --- VISTAS PARA EL PANEL DE ADMINISTRACIÓN (NUEVAS) ---

@staff_member_required
@login_required
def curso_lista_admin(request):
    """
    Muestra la lista de todos los cursos para el administrador.
    Permite ver, editar, eliminar y añadir nuevos cursos.
    """
    cursos = Servicio.objects.all().order_by('nombre')
    context = {
        'cursos': cursos,
        'titulo_pagina': 'Gestión de Cursos',
    }
    return render(request, 'servicios/admin/curso_lista.html', context)

@staff_member_required
@login_required
def curso_crear_admin(request):
    """
    Permite al administrador crear un nuevo curso.
    """
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES) # Usamos ServicioForm para crear/editar cursos
        if form.is_valid():
            form.save()
            messages.success(request, '¡Curso creado exitosamente!')
            return redirect('servicios:curso_lista_admin')
        else:
            messages.error(request, 'Hubo un error al crear el curso. Por favor, revisa los datos.')
    else:
        form = ServicioForm()

    context = {
        'form': form,
        'titulo_pagina': 'Crear Nuevo Curso',
    }
    return render(request, 'servicios/admin/curso_form.html', context)

@staff_member_required
@login_required
def curso_editar_admin(request, pk):
    """
    Permite al administrador editar un curso existente.
    """
    curso = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Curso actualizado exitosamente!')
            return redirect('servicios:curso_lista_admin')
        else:
            messages.error(request, 'Hubo un error al actualizar el curso. Por favor, revisa los datos.')
    else:
        form = ServicioForm(instance=curso)

    context = {
        'form': form,
        'curso': curso,
        'titulo_pagina': f'Editar Curso: {curso.nombre}',
    }
    return render(request, 'servicios/admin/curso_form.html', context)

@staff_member_required
@login_required
def curso_eliminar_admin(request, pk):
    """
    Permite al administrador eliminar un curso.
    """
    curso = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, '¡Curso eliminado exitosamente!')
        return redirect('servicios:curso_lista_admin')
    
    # Si se accede por GET, simplemente mostramos una página de confirmación (opcional)
    context = {
        'curso': curso,
        'titulo_pagina': f'Confirmar Eliminación: {curso.nombre}',
    }
    return render(request, 'servicios/admin/curso_confirm_delete.html', context)


@staff_member_required
@login_required
def inscripciones_curso_admin(request, pk):
    """
    Muestra la lista de inscripciones para un curso específico.
    """
    curso = get_object_or_404(Servicio, pk=pk)
    inscripciones = InscripcionCurso.objects.filter(curso=curso).order_by('-fecha_inscripcion')

    context = {
        'curso': curso,
        'inscripciones': inscripciones,
        'titulo_pagina': f'Inscripciones para: {curso.nombre}',
    }
    return render(request, 'servicios/admin/inscripciones_curso.html', context)

# Vistas principales para la gestión de servicios/cursos e inscripciones.
# Cada vista debe tener un comentario explicativo sobre su propósito y uso.
# Si se agregan nuevas vistas, documentar su funcionalidad y parámetros importantes.

