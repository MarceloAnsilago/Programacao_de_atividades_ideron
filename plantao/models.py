from django.db import models
from django.conf import settings

class Plantao(models.Model):
    nome = models.CharField(max_length=100)
    periodo_inicial = models.DateField()
    periodo_final = models.DateField()
    unidade = models.ForeignKey('organizacao.Unidade', on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

class SemanaPlantao(models.Model):
    plantao = models.ForeignKey(Plantao, on_delete=models.CASCADE, related_name='semanas')
    data_inicio = models.DateField()
    data_fim = models.DateField()
    servidor = models.ForeignKey('servidores.Servidor', on_delete=models.SET_NULL, null=True, blank=True)
    motivo_bloqueio = models.CharField(max_length=200, blank=True, null=True)  # opcional

    def __str__(self):
        return f"{self.data_inicio} a {self.data_fim} ({self.servidor or 'Nenhum'})"
