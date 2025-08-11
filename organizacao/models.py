from django.db import models
from django.contrib.auth.models import User, Permission  # + Permission

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

# NOVO: perfil/política baseado em permissões do Django
class PerfilPolitica(models.Model):
    nome = models.CharField(max_length=60, unique=True)
    descricao = models.CharField(max_length=255, blank=True)
    permissoes = models.ManyToManyField(Permission, blank=True)

    class Meta:
        permissions = [
            ("manage_policies", "Pode gerenciar perfis e políticas"),
        ]

    def __str__(self):
        return self.nome

class PerfilUsuario(models.Model):
    PERFIS = (
        ('gerente', 'Gerente'),
        ('supervisor', 'Supervisor'),
        ('unidade', 'Unidade'),
    )

    # ALTERAÇÃO: de OneToOne -> ForeignKey (permite vários vínculos por usuário)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vinculos')

    # Campo antigo agora OPCIONAL (vamos manter por compatibilidade)
    perfil = models.CharField(max_length=20, choices=PERFIS, null=True, blank=True)

    supervisao = models.ForeignKey(Supervisao, on_delete=models.SET_NULL, null=True, blank=True)
    unidade = models.ForeignKey(Unidade, on_delete=models.SET_NULL, null=True, blank=True)

    # NOVO: liga este vínculo a um conjunto de permissões
    perfil_politica = models.ForeignKey(
        PerfilPolitica,
        null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='vinculos'
    )

    def __str__(self):
        label = self.perfil_politica.nome if self.perfil_politica_id else (self.get_perfil_display() if self.perfil else '?')
        scope = self.unidade or self.supervisao or '—'
        return f"{self.usuario.username} @ {scope} [{label}]"
