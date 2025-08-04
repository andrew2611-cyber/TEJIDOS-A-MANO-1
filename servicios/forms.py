# servicios/forms.py

from django import forms
from .models import SolicitudServicio

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
