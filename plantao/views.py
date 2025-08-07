from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from servidores.models import Servidor
from descanso.models import Descanso
from django.db.models import Q
import datetime

@login_required
def pagina_plantao(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    periodo_inicial = request.POST.get('periodo_inicial')
    periodo_final = request.POST.get('periodo_final')

    servidores = Servidor.objects.filter(unidade=unidade, status="Ativo") if unidade else Servidor.objects.none()

    # lógica dos descansos etc.
    servidores_em_descanso = []
    servidores_livres = []

    descanso_qs = Descanso.objects.filter(servidor__in=servidores)
    periodo_ok = periodo_inicial and periodo_final

    if periodo_ok:
        data_inicio = datetime.datetime.strptime(periodo_inicial, "%Y-%m-%d").date()
        data_fim = datetime.datetime.strptime(periodo_final, "%Y-%m-%d").date()
        for servidor in servidores:
            descansos_conflitantes = list(
                descanso_qs.filter(
                    servidor=servidor
                ).filter(
                    Q(inicio__lte=data_fim, fim__gte=data_inicio)
                )
            )
            if descansos_conflitantes:
                servidores_em_descanso.append((servidor, descansos_conflitantes))
            else:
                servidores_livres.append(servidor)
    else:
        servidores_livres = servidores

    # --- PRÉ-SELEÇÃO dos servidores ---
    # Exemplo: IDs dos servidores que você quer já selecionados (pode ser via lógica, banco, ou do POST)
    if request.method == "POST":
        # Quando for POST, pega os que o usuário escolheu no submit
        ids_selecionados = request.POST.getlist("servidores_selecionados")
    else:
        # No GET, define os IDs que você quer selecionar por padrão (exemplo: sempre os 3 primeiros)
        ids_selecionados = [str(s.id) for s in servidores_livres[:3]]  # ajuste para sua lógica

    # Monta as opções já marcando os 'selected'
    servidores_options = [
        {
            "value": str(s.id),
            "label": s.nome,
            "selected": str(s.id) in ids_selecionados
        }
        for s in servidores_livres
    ]

    context = {
        "servidores_livres": servidores_livres,
        "servidores_em_descanso": servidores_em_descanso,
        "periodo_inicial": periodo_inicial,
        "periodo_final": periodo_final,
        "servidores_options": servidores_options,
        "request": request,
    }

    return render(request, "plantao/pagina_plantao.html", context)
