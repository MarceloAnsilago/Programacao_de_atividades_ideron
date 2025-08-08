from django.db import models
from django.contrib.auth.models import User
from atividades.models import Atividade
from organizacao.models import Supervisao, Unidade  # ajuste conforme seus apps

class Meta(models.Model):
    STATUS_CHOICES = [
        ('nova', 'Nova'),
        ('atribuida', 'Atribuída'),
        ('concluida', 'Concluída'),
        ('atrasada', 'Atrasada'),
        ('vencida', 'Vencida'),
    ]
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    quantidade_realizada = models.PositiveIntegerField(default=0)  # progresso
    prazo = models.DateField()
    observacoes = models.TextField(blank=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='metas_criadas')
    destinatario_supervisao = models.ForeignKey(
        Supervisao, null=True, blank=True, on_delete=models.SET_NULL, related_name='metas_recebidas'
    )
    destinatario_unidade = models.ForeignKey(
        Unidade, null=True, blank=True, on_delete=models.SET_NULL, related_name='metas_unidade'
    )
    criada_em = models.DateTimeField(auto_now_add=True)
    concluida_em = models.DateTimeField(null=True, blank=True)  # quando foi marcada como concluída
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='nova')

    class Meta:
        verbose_name = "Meta"
        verbose_name_plural = "Metas"

    def __str__(self):
        if self.destinatario_unidade:
            return f"{self.atividade} - Unidade: {self.destinatario_unidade}"
        elif self.destinatario_supervisao:
            return f"{self.atividade} - Supervisão: {self.destinatario_supervisao}"
        return str(self.atividade)
