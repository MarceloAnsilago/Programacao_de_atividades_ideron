from django.db import models
from organizacao.models import Unidade

class Servidor(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
    ]

    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    cargo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')

    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='servidores', null=True, blank=True)

    def __str__(self):
        return self.nome