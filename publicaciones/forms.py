# publicaciones/forms.py
from django import forms
from .models import Publicacion, Comentario
from tinymce.widgets import TinyMCE # <--- IMPORTAR TinyMCE

class PublicacionForm(forms.ModelForm):
    # Opcional: Si quieres usar una configuración de TinyMCE diferente a la global para este campo
    # contenido = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}, mce_attrs={'toolbar': 'bold italic | bullist numlist'}))

    class Meta:
        model = Publicacion
        fields = ['titulo', 'categoria', 'contenido', 'imagen']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Un título atractivo para tu publicación'}),
            'contenido': TinyMCE(attrs={'cols': 80, 'rows': 20}), # <--- USA EL WIDGET TinyMCE
            'categoria': forms.Select(),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'titulo': 'Título de la publicación',
            'categoria': 'Categoría',
            'contenido': 'Contenido',
            'imagen': 'Imagen de portada (opcional)'
        }
        help_texts = {
            'categoria': 'Elige la categoría que mejor describa tu publicación.',
            'imagen': 'Una buena imagen hace tu publicación más atractiva.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['titulo', 'categoria']: # 'contenido' ahora usa TinyMCE, no necesita 'form-control' directamente
                 field.widget.attrs.update({'class': 'form-control'})


# ... (PublicacionForm) ...

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Escribe tu comentario aquí...',
                'class': 'form-control' # Clase para estilos
            }),
        }
        labels = {
            'contenido': '' # Label vacío, el placeholder ya indica la función
        }