from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Servidor
from organizacao.models import Unidade
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

@login_required
def pagina_servidores(request):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    cargos = [
        ("Auditor", "Auditor"),
        ("Tecnico fiscal", "Técnico Fiscal"),
        ("Assistente de gestão", "Assistente de Gestão"),
        ("Assessor", "Assessor"),
    ]

    status_opcoes = [
        ("Ativo", "Ativo"),
        ("Inativo", "Inativo"),
    ]

    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')

    # Filtrar servidores apenas da unidade do usuário
    servidores = Servidor.objects.all()
    if unidade:
        servidores = servidores.filter(unidade=unidade)
    else:
        # Se o usuário não tem unidade, não mostra nenhum servidor
        servidores = Servidor.objects.none()

    if busca:
        servidores = servidores.filter(nome__icontains=busca)
    if status:
        servidores = servidores.filter(status=status)

    if request.method == "POST":
        nome = request.POST.get('nome')
        cargo = request.POST.get('cargo')
        telefone = request.POST.get('telefone')
        matricula = request.POST.get('matricula')
        status_post = "Ativo"

        if nome and cargo and unidade:
            Servidor.objects.create(
                nome=nome,
                cargo=cargo,
                telefone=telefone,
                matricula=matricula,
                status=status_post,
                unidade=unidade,  # Associa o servidor à unidade do usuário
            )
            return redirect('pagina_servidores')

    context = {
        "servidores": servidores,
        "cargos": cargos,
        "status_opcoes": status_opcoes,
        "status_atual": status,
        "request": request,
    }
    return render(request, "servidores/pagina_servidores.html", context)


@login_required
def servidor_inativar(request, id):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    servidor = get_object_or_404(Servidor, id=id, unidade=unidade)
    servidor.status = "Inativo"
    servidor.save()
    return redirect('pagina_servidores')


@login_required
def servidor_ativar(request, id):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    servidor = get_object_or_404(Servidor, id=id, unidade=unidade)
    servidor.status = "Ativo"
    servidor.save()
    return redirect('pagina_servidores')


@login_required
def servidor_editar(request, id):
    usuario = request.user
    perfil = getattr(usuario, 'perfilusuario', None)
    unidade = getattr(perfil, 'unidade', None)

    servidor = get_object_or_404(Servidor, id=id, unidade=unidade)
    cargos = [
        ("Auditor", "Auditor"),
        ("Tecnico fiscal", "Técnico Fiscal"),
        ("Assistente de gestão", "Assistente de Gestão"),
        ("Assessor", "Assessor"),
    ]

    if request.method == "POST":
        servidor.nome = request.POST.get("nome")
        servidor.cargo = request.POST.get("cargo")
        servidor.telefone = request.POST.get("telefone")
        servidor.matricula = request.POST.get("matricula")
        servidor.save()
        return redirect("pagina_servidores")

    # Aqui renderize o template de edição com servidor e cargos no contexto
    context = {
        "servidor": servidor,
        "cargos": cargos,
    }
    return render(request, "servidores/editar_servidor.html", context)
