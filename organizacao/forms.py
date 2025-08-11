# organizacao/forms.py
from django import forms
from django.contrib.auth.models import Permission
from .models import PerfilPolitica

APPS_INTERESSANTES = [
    'atividades', 'servidores', 'veiculos', 'descanso', 'plantao', 'metas', 'organizacao'
]

class PerfilPoliticaForm(forms.ModelForm):
    permissoes = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type')
                 .filter(content_type__app_label__in=APPS_INTERESSANTES)
                 .order_by('content_type__app_label', 'name'),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    class Meta:
        model = PerfilPolitica
        fields = ['nome', 'descricao', 'permissoes']
