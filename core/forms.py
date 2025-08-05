# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Pedido, Producto

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electrónico', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.help_text = None
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                field.widget.attrs.update({'class': 'form-control'})

        if 'password' in self.fields:
            self.fields['password'].label = 'Contraseña' # Esto afecta al primer campo de contraseña

        if 'password2' in self.fields:
            self.fields['password2'].label = 'Confirmar Contraseña'


    class Meta(UserCreationForm.Meta):
        model = User
        # ESTA ES LA LÍNEA CLAVE:
        fields = UserCreationForm.Meta.fields + ('email',)

class CustomUserChangeForm(UserChangeForm):
    """
    Formulario de edición de usuario personalizado (para la página de perfil).
    SOLO incluye los campos username, first_name, last_name, email.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Iterar sobre todos los campos y quitar su help_text.
        for field_name, field in self.fields.items():
            field.help_text = None
            # Asegurarse de que los campos de texto/email tengan el estilo form-control
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({'class': 'form-control'})

        # Eliminar los campos que NO queremos mostrar.
        fields_to_remove = [
            'password', 'last_login', 'date_joined', 'groups', 'user_permissions',
            'is_staff', 'is_active', 'is_superuser'
        ]
        for field_name in fields_to_remove:
            self.fields.pop(field_name, None) # 'None' para no dar error si el campo ya no existe

    class Meta(UserChangeForm.Meta):
        model = User
        # Definir EXPLICITAMENTE los campos que quieres que aparezcan en la edición de perfil.
        fields = ('username', 'first_name', 'last_name', 'email')

class PedidoAnonimoForm(forms.ModelForm):
    # Aquí puedes añadir campos específicos del formulario si son diferentes a los del modelo
    # Por ejemplo, si quieres que el teléfono sea obligatorio aquí pero no en el modelo
    # email_confirm = forms.EmailField(label='Confirmar Correo Electrónico')

    class Meta:
        model = Pedido
        fields = ['nombre_completo', 'email', 'telefono', 'direccion_envio', 'ciudad', 'codigo_postal', 'pais']
        labels = {
            'nombre_completo': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'telefono': 'Número de Teléfono',
            'direccion_envio': 'Dirección de Envío',
            'ciudad': 'Ciudad',
            'codigo_postal': 'Código Postal',
            'pais': 'País',
        }
        widgets = {
            'direccion_envio': forms.Textarea(attrs={'rows': 3}),
            'pais': forms.Select(choices=[
                ('Colombia', 'Colombia'), # Puedes añadir más países si lo necesitas
                # ('Mexico', 'México'),
                # ('Spain', 'España'),
            ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases de Bootstrap a los campos del formulario
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput) or \
               isinstance(field.widget, forms.EmailInput) or \
               isinstance(field.widget, forms.Textarea) or \
               isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-control'
            # Puedes añadir más personalización aquí si es necesario

            