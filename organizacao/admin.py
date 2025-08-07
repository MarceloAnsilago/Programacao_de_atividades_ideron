from django.contrib import admin
from .models import Supervisao, Unidade, PerfilUsuario

@admin.register(Supervisao)
class SupervisaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ('nome',)

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'supervisao', 'status')
    list_filter = ('status', 'supervisao')
    search_fields = ('nome',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'perfil', 'supervisao', 'unidade')
    list_filter = ('perfil',)
    search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name')