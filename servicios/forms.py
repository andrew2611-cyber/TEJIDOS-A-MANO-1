# servicios/forms.py

from django import forms
from .models import Servicio, InscripcionCurso, SolicitudServicio # Importamos los modelos necesarios

class ServicioForm(forms.ModelForm):
    """
    Formulario para crear y editar cursos (modelo Servicio) en el panel de administración.
    """
    class Meta:
        model = Servicio
        # Incluye todos los campos que el admin puede editar para un curso
        fields = ['nombre', 'slug', 'descripcion_corta', 'descripcion_larga', 'precio_referencia', 'imagen', 'disponible']
        widgets = {
            'descripcion_larga': forms.Textarea(attrs={'rows': 5}), # Hace el campo de texto más grande
        }
        labels = {
            'nombre': 'Nombre del Curso',
            'slug': 'Slug (URL amigable)',
            'descripcion_corta': 'Breve resumen del servicio',
            'descripcion_larga': 'Descripción Detallada',
            'precio_referencia': 'Precio de Referencia',
            'imagen': 'Imagen del Curso',
            'disponible': 'Disponible',
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre) < 3:
            raise forms.ValidationError('El nombre del curso debe tener al menos 3 caracteres.')
        return nombre


class InscripcionCursoForm(forms.ModelForm):
    """
    Formulario para la inscripción a cursos, utilizado por los usuarios públicos.
    Basado en los campos del formulario de inscripción que me mostraste.
    """
    # Hacemos estos campos explícitamente no requeridos en el formulario
    direccion_adicional = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej: Calle Falsa 123, Ciudad, País'}),
        label='Dirección Adicional / Otros'
    )
    observaciones = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones o preguntas adicionales'}),
        label='Observaciones'
    )
    como_supo_del_curso = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Redes sociales, amigo, Google'}),
        label='¿Cómo supiste del curso?'
    )

    class Meta:
        model = InscripcionCurso
        # Excluimos el campo 'curso' y 'fecha_inscripcion' porque se asignan automáticamente en la vista
        # Ahora incluimos solo los campos que no hemos definido explícitamente arriba
        fields = ['nombre_completo', 'correo_electronico', 'telefono', 'direccion_adicional', 'observaciones', 'como_supo_del_curso']
        
        # Los labels para los campos definidos explícitamente arriba ya no necesitan estar aquí
        labels = {
            'nombre_completo': 'Nombre completo',
            'correo_electronico': 'Correo electrónico',
            'telefono': 'Teléfono',
        }

    def clean_correo_electronico(self):
        correo = self.cleaned_data.get('correo_electronico')
        if not correo or '@' not in correo:
            raise forms.ValidationError('Ingrese un correo electrónico válido.')
        return correo

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        if not nombre or len(nombre) < 3:
            raise forms.ValidationError('El nombre completo debe tener al menos 3 caracteres.')
        return nombre


# Mantenemos SolicitudServicioForm si todavía lo utilizas para otras funcionalidades
# Si SolicitudServicio y su formulario asociado ya no se necesitan porque InscripcionCurso
# cubre todas las necesidades de "solicitudes" para cursos, podrías eliminar este bloque.
class SolicitudServicioForm(forms.ModelForm):
    origen = forms.CharField(
        max_length=200,
        required=False,
        label='¿De dónde vienes?',
        widget=forms.TextInput(attrs={'placeholder': 'Ciudad, país, etc.'})
    )

    class Meta:
        model = SolicitudServicio
        fields = ['nombre_cliente', 'email_cliente', 'telefono_cliente', 'mensaje']
        labels = {
            'nombre_cliente': 'Nombre completo',
            'email_cliente': 'Correo electrónico',
            'telefono_cliente': 'Teléfono',
            'mensaje': 'Observaciones',
        }
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Observaciones adicionales'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        origen = cleaned_data.get('origen', '')
        mensaje = cleaned_data.get('mensaje', '')
        if origen:
            mensaje = f"De dónde viene: {origen}\n{mensaje}"
        cleaned_data['mensaje'] = mensaje
        return cleaned_data
