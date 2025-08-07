from django import forms
from .models import Atividade

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ['nome', 'area']  
        widgets = {
            'area': forms.Select(choices=Atividade.AREA_CHOICES),
        }