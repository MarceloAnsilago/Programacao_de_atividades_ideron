from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from servidores.models import Servidor
from descanso.models import Descanso
from django.db.models import Q
import datetime
import locale
from django.contrib import messages
from organizacao.models import Unidade 
from django.shortcuts import render, redirect
from .models import Plantao, SemanaPlantao

def gerar_plantao_semana_com_impedimentos(servidores, descansos, data_inicio, data_fim):
    semanas = []
    inicio_semana = data_inicio
    while inicio_semana.weekday() != 5:
        inicio_semana += datetime.timedelta(days=1)
    while inicio_semana <= data_fim:
        fim_semana = min(inicio_semana + datetime.timedelta(days=6), data_fim)
        semanas.append((inicio_semana, fim_semana))
        inicio_semana = fim_semana + datetime.timedelta(days=1)

    descansos_por_servidor = {s.id: [] for s in servidores}
    for d in descansos:
        descansos_por_servidor.setdefault(d.servidor_id, []).append((d.inicio, d.fim, str(d.tipo)))

    escala = []
    impedimentos_msgs = []
    idx = 0
    n_servidores = len(servidores)

    for semana_idx, (sem_ini, sem_fim) in enumerate(semanas):
        escolhido = None
        tentativas = 0
        impedidos_essa_semana = []
        while tentativas < n_servidores:
            s = servidores[(idx + tentativas) % n_servidores]
            impedido = False
            for d_ini, d_fim, tipo in descansos_por_servidor.get(s.id, []):
                if not (d_fim < sem_ini or d_ini > sem_fim):
                    impedido = True
                    impedidos_essa_semana.append(
                        f"{s.nome}: impedido na semana {sem_ini.strftime('%d/%m/%Y')} a {sem_fim.strftime('%d/%m/%Y')} por {tipo.lower()} ({d_ini.strftime('%d/%m/%Y')} - {d_fim.strftime('%d/%m/%Y')})"
                    )
                    break
            if not impedido:
                escolhido = s
                idx = (idx + tentativas + 1) % n_servidores
                break
            tentativas += 1
        escala.append({
            "inicio": sem_ini,
            "fim": sem_fim,
            "servidor": escolhido,
        })
        # Adiciona todos os impedimentos tentados para a semana (mesmo que tenha escolhido alguém)
        impedimentos_msgs.extend(impedidos_essa_semana)
        # Se ninguém pôde assumir, também mostra a mensagem padrão
        if not escolhido:
            impedimentos_msgs.append(
                f"Semana {sem_ini.strftime('%d/%m/%Y')} a {sem_fim.strftime('%d/%m/%Y')}: Nenhum servidor disponível."
            )

    return escala, impedimentos_msgs


@login_required
def pagina_plantao(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    periodo_inicial = request.POST.get('periodo_inicial')
    periodo_final = request.POST.get('periodo_final')

    # Use todos ativos para seleção!
    servidores_todos = Servidor.objects.filter(unidade=unidade, status="Ativo") if unidade else Servidor.objects.none()

    servidores_em_descanso = []
    servidores_livres = []

    descanso_qs = Descanso.objects.filter(servidor__in=servidores_todos)
    periodo_ok = periodo_inicial and periodo_final

    data_inicio = None
    data_fim = None

    if periodo_ok:
        data_inicio = datetime.datetime.strptime(periodo_inicial, "%Y-%m-%d").date()
        data_fim = datetime.datetime.strptime(periodo_final, "%Y-%m-%d").date()
        for servidor in servidores_todos:
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
        servidores_livres = servidores_todos

    if request.method == "POST":
        ids_selecionados = request.POST.getlist("servidores_selecionados")
    else:
        ids_selecionados = [str(s.id) for s in servidores_livres[:3]]

    # Monte o multiselect com todos os ativos!
    servidores_options = [
        {
            "value": str(s.id),
            "label": s.nome,
            "selected": str(s.id) in ids_selecionados
        }
        for s in servidores_todos
    ]

    tabela_plantao = None
    impedimentos_msgs = None
    if periodo_ok and request.method == "POST" and ids_selecionados:
        servidores_selecionados = [s for s in servidores_todos if str(s.id) in ids_selecionados]
        servidores_selecionados = sorted(
            servidores_selecionados,
            key=lambda x: ids_selecionados.index(str(x.id))
        )
        if servidores_selecionados and data_inicio and data_fim:
            descansos_selecionados = Descanso.objects.filter(servidor__in=servidores_selecionados)
            tabela_plantao, impedimentos_msgs = gerar_plantao_semana_com_impedimentos(
                servidores_selecionados,
                descansos_selecionados,
                data_inicio,
                data_fim
            )
    meses_plantao = []
    if tabela_plantao:
        # Opcional: coloca nomes dos meses em português, se disponível no sistema operacional
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except:
            pass
        meses_set = set()
        for semana in tabela_plantao:
            meses_set.add((semana['inicio'].month, semana['inicio'].year))
            meses_set.add((semana['fim'].month, semana['fim'].year))
        meses_plantao = [
            f"{datetime.date(ano, mes, 1).strftime('%B').capitalize()}/{ano}"
            for mes, ano in sorted(meses_set, key=lambda x: (x[1], x[0]))
        ]
   
    context = {
        "servidores_livres": servidores_livres,
        "servidores_em_descanso": servidores_em_descanso,
        "periodo_inicial": periodo_inicial,
        "periodo_final": periodo_final,
        "servidores_options": servidores_options,
        "tabela_plantao": tabela_plantao,
        "impedimentos_msgs": impedimentos_msgs,
        "meses_plantao": meses_plantao,  # <--- aqui!
        "request": request,
    }

    return render(request, "plantao/pagina_plantao.html", context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Plantao, SemanaPlantao
import datetime

@login_required
def salvar_plantao(request):
    if request.method == "POST":
        periodo_inicial_str = request.POST.get('periodo_inicial')
        periodo_final_str = request.POST.get('periodo_final')
        nome = request.POST.get('nome_plantao')
        unidade_id = request.user.perfilusuario.unidade_id

        # Converte as datas de string para date
        try:
            periodo_inicial = datetime.datetime.strptime(periodo_inicial_str, "%Y-%m-%d").date()
            periodo_final = datetime.datetime.strptime(periodo_final_str, "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Erro ao processar as datas.")
            return redirect('plantao:pagina_plantao')

        # Verifica sobreposição de plantões
        existe = Plantao.objects.filter(
            unidade_id=unidade_id,
            periodo_inicial__lte=periodo_final,
            periodo_final__gte=periodo_inicial
        ).exists()

        if existe:
            messages.warning(request, "Já existe um plantão cadastrado para esse período e unidade.")
            return redirect('plantao:pagina_plantao')

        # Cria o Plantão
        plantao = Plantao.objects.create(
            nome=nome or f"Plantão {periodo_inicial} a {periodo_final}",
            periodo_inicial=periodo_inicial,
            periodo_final=periodo_final,
            unidade_id=unidade_id,
            criado_por=request.user
        )

        # Salva as semanas do plantão
        data_inicio = periodo_inicial
        data_fim = periodo_final
        semanas = []
        inicio_semana = data_inicio
        while inicio_semana.weekday() != 5:  # Sábado
            inicio_semana += datetime.timedelta(days=1)
        while inicio_semana <= data_fim:
            fim_semana = min(inicio_semana + datetime.timedelta(days=6), data_fim)
            semanas.append((inicio_semana, fim_semana))
            inicio_semana = fim_semana + datetime.timedelta(days=1)

        for semana in semanas:
            SemanaPlantao.objects.create(
                plantao=plantao,
                data_inicio=semana[0],
                data_fim=semana[1],
                motivo_bloqueio='' # ajuste se quiser adicionar motivo
            )

        messages.success(request, "Plantão salvo com sucesso!")
        return redirect('plantao:pagina_plantao')
    else:
        return redirect('plantao:pagina_plantao')
