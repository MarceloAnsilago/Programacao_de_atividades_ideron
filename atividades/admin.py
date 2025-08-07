from django.contrib import admin
from .models import Atividade

@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'area', 'ativo', 'unidade')
    list_filter = ('area', 'ativo', 'unidade')
    search_fields = ('nome',)