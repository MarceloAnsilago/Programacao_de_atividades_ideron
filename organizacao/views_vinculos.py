# organizacao/views_vinculos.py
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Supervisao, Unidade, PerfilPolitica, PerfilUsuario

# (Opcional) home de vínculos – se você não quer usar página separada,
# podemos manter como página simples ou redirecionar.
@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def vinculos_home(request):
    # Se quiser página própria, troque para render(...)
    return redirect('organizacao:politicas_lista')

# Seletor: Supervisão -> Unidades (para um perfil específico)
@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def vinculos_seletor(request, perfil_id: int):
    perfil = get_object_or_404(PerfilPolitica, pk=perfil_id)
    supervisoes = Supervisao.objects.all().order_by('nome')
    return render(request, 'organizacao/vinculos_seletor.html', {
        'perfil': perfil,
        'supervisoes': supervisoes,
    })

# API para popular o select de unidades
@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def unidades_por_supervisao(request, supervisao_id: int):
    unidades = Unidade.objects.filter(supervisao_id=supervisao_id).order_by('nome') \
               .values('id', 'nome')
    return JsonResponse({'unidades': list(unidades)})

# Editor: marcar usuários com o perfil naquela unidade
@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def vinculos_editar(request, perfil_id: int, unidade_id: int):
    perfil = get_object_or_404(PerfilPolitica, pk=perfil_id)
    unidade = get_object_or_404(Unidade, pk=unidade_id)

    marcados_ids = set(
        PerfilUsuario.objects.filter(unidade=unidade, perfil_politica=perfil)
        .values_list('usuario_id', flat=True)
    )
    usuarios = User.objects.order_by('first_name', 'username')

    if request.method == 'POST':
        enviados = set(map(int, request.POST.getlist('usuarios')))
        # cria novos vínculos
        to_create = enviados - marcados_ids
        PerfilUsuario.objects.bulk_create([
            PerfilUsuario(usuario_id=uid, unidade=unidade, perfil_politica=perfil)
            for uid in to_create
        ])
        # remove os vínculos desmarcados
        to_delete = marcados_ids - enviados
        if to_delete:
            PerfilUsuario.objects.filter(
                unidade=unidade, perfil_politica=perfil, usuario_id__in=to_delete
            ).delete()
        return redirect('organizacao:vinculos_editar', perfil_id=perfil.id, unidade_id=unidade.id)

    return render(request, 'organizacao/vinculos_editar.html', {
        'perfil': perfil,
        'unidade': unidade,
        'usuarios': usuarios,
        'marcados_ids': marcados_ids,
    })
@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def permissoes_seletor(request, perfil_id: int):
    """
    Seletor Supervisão -> Unidade para o fluxo de PERMISSÕES.
    O editor que abriremos depois é o politicas_editar (global).
    """
    perfil = get_object_or_404(PerfilPolitica, pk=perfil_id)
    supervisoes = Supervisao.objects.all().order_by('nome')
    return render(request, 'organizacao/permissoes_seletor.html', {
        'perfil': perfil,
        'supervisoes': supervisoes,
    })