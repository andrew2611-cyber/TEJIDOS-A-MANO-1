# productos/forms.py

from django import forms
from .models import Producto, Categoria, ImagenProducto # Asegúrate de que ImagenProducto esté aquí si lo usas

# Formularios personalizados para productos y categorías.
# Se recomienda mantener estos comentarios para facilitar el trabajo colaborativo.
# Si se agregan nuevos campos, documentar su propósito y uso.

class ProductoForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
    tallas = forms.CharField(required=False, help_text="Ejemplo: 36,37,38,39", widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: 36,37,38,39'}))
    colores = forms.CharField(required=False, help_text="Ejemplo: Rojo, Azul, Verde", widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Rojo, Azul, Verde'}))

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen_principal', 'imagen_fondo', 'disponible', 'categoria', 'tallas', 'colores']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen_fondo': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nombre')

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre) < 3:
            raise forms.ValidationError('El nombre del producto debe tener al menos 3 caracteres.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a cero.')
        return precio

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'slug', 'descripcion', 'imagen_fondo', 'imagen_principal']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'form-control'}),
            'imagen_fondo': forms.Select(attrs={'class': 'form-control'}),
            'imagen_principal': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre or len(nombre) < 3:
            raise forms.ValidationError('El nombre de la categoría debe tener al menos 3 caracteres.')
        return nombre