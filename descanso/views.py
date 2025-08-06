from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from servidores.models import Servidor
from descanso.models import Descanso
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
import calendar
from collections import defaultdict
import datetime

@login_required
def pagina_descanso(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    busca = request.GET.get('busca', '')

    servidores = Servidor.objects.filter(unidade=unidade, status="Ativo") if unidade else Servidor.objects.none()
    if busca:
        servidores = servidores.filter(nome__icontains=busca)

    context = {
        "servidores": servidores,
        "request": request,
    }
    return render(request, "descanso/pagina_descanso.html", context)

@login_required
def cadastrar_descanso(request, servidor_id):
    servidor = get_object_or_404(Servidor, id=servidor_id)

    tipos_descanso = [
        ("Férias", "Férias"),
        ("Afastamento", "Afastamento"),
        ("Folga compensatória", "Folga compensatória"),
        ("Outros", "Outros"),
    ]

    error_msg = None
    inicio = fim = tipo = observacao = ''

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        inicio = request.POST.get('inicio')
        fim = request.POST.get('fim')
        observacao = request.POST.get('observacao', '')

        # Checagem de sobreposição de períodos
        conflito = Descanso.objects.filter(
            servidor=servidor
        ).filter(
            Q(inicio__lte=inicio, fim__gte=inicio) |
            Q(inicio__lte=fim, fim__gte=fim) |
            Q(inicio__gte=inicio, fim__lte=fim)
        ).exists()

        if conflito:
            error_msg = "Já existe um período de descanso cadastrado que conflita com as datas informadas."
        else:
            Descanso.objects.create(
                servidor=servidor,
                tipo=tipo,
                inicio=inicio,
                fim=fim,
                observacao=observacao
            )
            messages.success(request, "Período de descanso cadastrado com sucesso!")
            return redirect('pagina_descanso')

    context = {
        'servidor': servidor,
        'tipos_descanso': tipos_descanso,
        'error_msg': error_msg,
        'inicio': inicio,
        'fim': fim,
        'tipo': tipo,
        'observacao': observacao,
    }
    return render(request, 'descanso/cadastrar_descanso.html', context)

@login_required
def ver_descanso(request, servidor_id):
    servidor = get_object_or_404(Servidor, id=servidor_id)
    descansos = Descanso.objects.filter(servidor=servidor).order_by('-inicio')
    return render(request, 'descanso/ver_descanso.html', {
        'servidor': servidor,
        'descansos': descansos,
    })

@login_required
def editar_descanso(request, descanso_id):
    descanso = get_object_or_404(Descanso, id=descanso_id)
    servidor = descanso.servidor

    tipos_descanso = [
        ("Férias", "Férias"),
        ("Afastamento", "Afastamento"),
        ("Folga compensatória", "Folga compensatória"),
        ("Outros", "Outros"),
    ]

    if request.method == 'POST':
        descanso.inicio = request.POST.get('inicio')
        descanso.fim = request.POST.get('fim')
        descanso.tipo = request.POST.get('tipo')
        descanso.observacao = request.POST.get('observacao')
        descanso.save()
        return redirect('ver_descanso', servidor_id=servidor.id)

    context = {
        'servidor': servidor,
        'descanso': descanso,
        'tipos_descanso': tipos_descanso,
        'inicio': descanso.inicio.strftime('%Y-%m-%d') if descanso.inicio else '',
        'fim': descanso.fim.strftime('%Y-%m-%d') if descanso.fim else '',
        'tipo_atual': descanso.tipo,
        'observacao': descanso.observacao,
    }
    return render(request, 'descanso/editar_descanso.html', context)

@login_required
def excluir_descanso(request, descanso_id):
    descanso = get_object_or_404(Descanso, id=descanso_id)
    servidor_id = descanso.servidor.id
    descanso.delete()
    return redirect('ver_descanso', servidor_id=servidor_id)


@login_required
def relatorio_mapa_ferias(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)
    ano = 2025

    servidores = Servidor.objects.filter(unidade=unidade, status="Ativo") if unidade else Servidor.objects.none()
    descansos = Descanso.objects.filter(servidor__in=servidores, inicio__year=ano)

    servidor_mapa = defaultdict(dict)  # agora um dict simples
    meses_set = set()  # coletar todos os meses usados para o header

   
    mes_mapa = defaultdict(dict)
    for servidor in servidores:
        descansos_servidor = descansos.filter(servidor=servidor)
        for d in descansos_servidor:
            mes_inicio = d.inicio.month
            mes_fim = d.fim.month
            for mes in range(mes_inicio, mes_fim + 1):
                dias_no_mes = calendar.monthrange(ano, mes)[1]
                dias = mes_mapa[mes].get(servidor, [None] * dias_no_mes)
                for dia in range(1, dias_no_mes + 1):
                    data = datetime.date(ano, mes, dia)
                    if d.inicio <= data <= d.fim:
                        dias[dia - 1] = True
                mes_mapa[mes][servidor] = dias


    meses_usados = sorted(mes_mapa.keys())
    meses_nomes = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    meses_label = [(mes, meses_nomes[mes-1]) for mes in meses_usados]

    context = {
        'ano': ano,
        'mes_mapa': mes_mapa,
        'meses_label': meses_label,  # [(8, 'Agosto'), (9, 'Setembro'), ...]
    }
    return render(request, 'descanso/relatorio_mapa_ferias.html', context)
