# servicios/models.py

from django.db import models

# Modelos principales para la gestión de servicios y cursos.
# Relacionan servicios/cursos con inscripciones y gestionan atributos clave como disponibilidad y precio.
# Si se agregan nuevos campos, documentar su propósito y uso.

class Servicio(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="URL amigable (ej: taller-tejido-basico)")
    descripcion_corta = models.TextField(blank=True, help_text="Breve resumen del servicio")
    descripcion_larga = models.TextField()
    precio_referencia = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Precio estimado o desde")
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Servicios" # Podríamos cambiarlo a "Cursos" si quieres renombrar el modelo Servicio
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

# --- NUEVO MODELO PARA INSCRIPCIONES DE CURSOS ---
class InscripcionCurso(models.Model):
    # Relaciona esta inscripción con un curso específico.
    # Si el curso se elimina, las inscripciones asociadas también se eliminan (CASCADE).
    # 'related_name' permite acceder a las inscripciones desde un objeto Servicio (ej: curso.inscripciones.all())
    curso = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='inscripciones')

    # Campos del formulario de inscripción
    nombre_completo = models.CharField(max_length=150)
    correo_electronico = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    # Campo para "Dirección adicional/otros"
    direccion_adicional = models.TextField(blank=True, help_text="Dirección, ciudad, o cualquier otro detalle de contacto.")
    # Campo para "Observaciones"
    observaciones = models.TextField(blank=True, help_text="Observaciones o preguntas adicionales del inscrito.")
    # Campo para "¿De dónde vienes?"
    como_supo_del_curso = models.CharField(max_length=100, blank=True, help_text="¿De dónde supiste del curso?")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True) # Fecha y hora de la inscripción

    class Meta:
        verbose_name_plural = "Inscripciones a Cursos" # Nombre que aparecerá en el admin
        ordering = ['-fecha_inscripcion'] # Ordena las inscripciones por fecha, las más recientes primero

    def __str__(self):
        # Representación legible de la inscripción
        return f"Inscripción de {self.nombre_completo} para {self.curso.nombre}"

# El modelo SolicitudServicio se mantiene si lo usas para otras cosas, o lo podemos eliminar si solo es para cursos.
# Si SolicitudServicio solo se usaba para las inscripciones a cursos, podríamos eliminarlo.
# Si lo usas para otras "solicitudes" que no son inscripciones, déjalo como está.
class SolicitudServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes')
    nombre_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefono_cliente = models.CharField(max_length=20, blank=True, null=True)
    mensaje = models.TextField(help_text="Detalles de la solicitud o pregunta")
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    resuelto = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Solicitudes de Servicio"
        ordering = ['-fecha_solicitud']

    def __str__(self):
        return f"Solicitud de {self.nombre_cliente} para {self.servicio.nombre if self.servicio else 'Servicio no especificado'}"
