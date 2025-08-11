from django.contrib import admin
from .models import Supervisao, Unidade, PerfilUsuario, PerfilPolitica

@admin.register(Supervisao)
class SupervisaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'supervisao', 'status')
    list_filter = ('status', 'supervisao')
    search_fields = ('nome',)

@admin.register(PerfilPolitica)
class PerfilPoliticaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'descricao')
    search_fields = ('nome',)
    filter_horizontal = ('permissoes',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'perfil_politica', 'perfil', 'supervisao', 'unidade')
    list_filter = ('perfil_politica', 'perfil', 'supervisao', 'unidade')
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')
    autocomplete_fields = ('usuario', 'unidade', 'supervisao', 'perfil_politica')
