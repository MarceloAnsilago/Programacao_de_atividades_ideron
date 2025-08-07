from django.contrib import admin
from .models import Servidor

@admin.register(Servidor)
class ServidorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cargo', 'status', 'unidade')
    list_filter = ('status', 'unidade')
    search_fields = ('nome', 'matricula', 'cargo')