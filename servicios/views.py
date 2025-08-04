# servicios/views.py

from django.shortcuts import render, get_object_or_404
from .models import Servicio, SolicitudServicio
from .forms import SolicitudServicioForm

def lista_servicios(request):
    servicios = Servicio.objects.filter(disponible=True)
    context = {
        'servicios': servicios,
        'titulo_pagina': 'Cursos Presenciales',
    }
    return render(request, 'servicios/lista_servicios.html', context)

def detalle_servicio(request, slug):
    servicio = get_object_or_404(Servicio, slug=slug, disponible=True)
    form = SolicitudServicioForm()

    if request.method == 'POST':
        form = SolicitudServicioForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.servicio = servicio
            solicitud.save()
            context = {
                'servicio': servicio,
                'form': SolicitudServicioForm(),
                'mensaje_exito': '¡Tu inscripción ha sido enviada con éxito!',
                'titulo_pagina': servicio.nombre,
            }
            return render(request, 'servicios/detalle_servicio.html', context)

    context = {
        'servicio': servicio,
        'form': form,
        'titulo_pagina': servicio.nombre,
    }
    return render(request, 'servicios/detalle_servicio.html', context)
