# Create your models here.
from django.db import models
from servidores.models import Servidor

class Descanso(models.Model):
    TIPO_CHOICES = [
        ('Férias', 'Férias'),
        ('Afastamento', 'Afastamento'),
        ('Folga compensatória', 'Folga compensatória'),
        ('Outros', 'Outros'),
    ]

    servidor = models.ForeignKey(Servidor, on_delete=models.CASCADE, related_name="descansos")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    inicio = models.DateField()
    fim = models.DateField()
    observacao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.servidor.nome} - {self.tipo} ({self.inicio} a {self.fim})"

    class Meta:
        verbose_name = "Descanso"
        verbose_name_plural = "Descansos"
        ordering = ['-inicio']