from django.db import models
from organizacao.models import Unidade  # Certifique-se que o nome do app está correto

class Veiculo(models.Model):
    nome = models.CharField(max_length=120)
    placa = models.CharField(max_length=15, unique=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE, related_name='veiculos')
    status = models.CharField(
        max_length=10,
        choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')],
        default='Ativo'
    )

    def __str__(self):
        return f'{self.nome} ({self.placa})'
