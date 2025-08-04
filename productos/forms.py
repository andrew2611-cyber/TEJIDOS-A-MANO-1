# productos/forms.py

from django import forms
from .models import Producto, Categoria, ImagenProducto # Asegúrate de que ImagenProducto esté aquí si lo usas

class ProductoForm(forms.ModelForm):
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))

    class Meta:
        model = Producto
        # Eliminar 'stock' de la lista de campos
        fields = ['nombre', 'descripcion', 'precio', 'imagen_principal', 'disponible', 'categoria']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            # Eliminar el widget para 'stock'
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nombre')


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'slug', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'form-control'}),
        }