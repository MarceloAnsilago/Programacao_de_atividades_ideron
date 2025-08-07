from django.contrib import admin
from .models import Plantao, SemanaPlantao

class SemanaPlantaoInline(admin.TabularInline):
    model = SemanaPlantao
    extra = 0

@admin.register(Plantao)
class PlantaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'unidade', 'periodo_inicial', 'periodo_final', 'criado_por', 'criado_em')
    list_filter = ('unidade', 'periodo_inicial', 'periodo_final')
    search_fields = ('nome',)
    inlines = [SemanaPlantaoInline]

@admin.register(SemanaPlantao)
class SemanaPlantaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'plantao', 'data_inicio', 'data_fim', 'servidor', 'motivo_bloqueio')
    list_filter = ('plantao', 'servidor')
    search_fields = ('plantao__nome', 'servidor__nome')
