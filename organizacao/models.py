from django.db import models
from django.contrib.auth.models import User

class Supervisao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Unidade(models.Model):
    nome = models.CharField(max_length=100)
    supervisao = models.ForeignKey(Supervisao, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='Ativo')

    def __str__(self):
        return self.nome

class PerfilUsuario(models.Model):
    PERFIS = (
        ('gerente', 'Gerente'),
        ('supervisor', 'Supervisor'),
        ('unidade', 'Unidade'),
    )

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    perfil = models.CharField(max_length=20, choices=PERFIS)
    supervisao = models.ForeignKey(Supervisao, on_delete=models.SET_NULL, null=True, blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.username} ({self.get_perfil_display()})"
