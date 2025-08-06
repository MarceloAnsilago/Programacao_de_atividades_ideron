from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from servidores.models import Servidor
from descanso.models import Descanso
from django.db.models import Q
from django.contrib import messages

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