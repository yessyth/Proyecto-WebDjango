from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto', 'biografia', 'autos_favoritos', 'foto_portada']
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 4}),
            'autos_favoritos': forms.TextInput(attrs={'placeholder': 'Ej: Ferrari, Lamborghini, McLaren'})
        }