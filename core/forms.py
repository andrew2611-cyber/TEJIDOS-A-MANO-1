from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .models import Pedido # Importa el modelo Pedido

User = get_user_model()

# Formularios personalizados para usuarios y pedidos.
# Se recomienda mantener estos comentarios para facilitar el trabajo colaborativo.
# Si se agregan nuevos campos, documentar su propósito y uso.

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        # Sobrescribe los widgets para añadir placeholders y eliminar help_text predeterminados
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Elimina los help_text de los campos de contraseña y username
        if 'password' in self.fields:
            self.fields['password'].help_text = ''
        if 'password2' in self.fields:
            self.fields['password2'].help_text = ''
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        # Elimina los help_text de password1 si existe
        if 'password1' in self.fields:
            self.fields['password1'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('No se pudo registrar con ese correo. Intente con otro correo.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        # No mostrar detalles de seguridad
        if password1 and self.cleaned_data.get('username') and password1.lower() in self.cleaned_data.get('username').lower():
            raise forms.ValidationError('La contraseña no es válida. Intente con otra contraseña.')
        return password2

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return email

class PedidoAnonimoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_completo', 'email', 'telefono', 'direccion_envio', 'ciudad', 'codigo_postal', 'pais'] # Elimino 'admin_observaciones'
        # Los campos 'telefono', 'codigo_postal' y 'admin_observaciones' son opcionales porque están definidos con blank=True, null=True en el modelo Pedido.
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-lg'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'direccion_envio': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'pais': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or '@' not in email:
            raise forms.ValidationError('Ingrese un correo electrónico válido.')
        return email

    def clean_nombre_completo(self):
        nombre = self.cleaned_data.get('nombre_completo')
        if not nombre or len(nombre) < 3:
            raise forms.ValidationError('El nombre completo debe tener al menos 3 caracteres.')
        return nombre
