from django.db import models
from organizacao.models import Unidade

class Atividade(models.Model):
    AREA_CHOICES = [
        ('animal', 'Animal'),
        ('vegetal', 'Vegetal'),
        ('apoio', 'Apoio'),
    ]
    nome = models.CharField(max_length=255)
    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    ativo = models.BooleanField(default=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='atividades')

    def __str__(self):
        return self.nome
