from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Servidor
from organizacao.models import Unidade
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

@login_required
def pagina_servidores(request):
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

    servidores = Servidor.objects.all()
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

        if nome and cargo:
            Servidor.objects.create(
                nome=nome,
                cargo=cargo,
                telefone=telefone,
                matricula=matricula,
                status=status_post,
            )
            return redirect('pagina_servidores')

    context = {
        "servidores": servidores,
        "cargos": cargos,
        "status_opcoes": status_opcoes,
        "status_atual": status,  # <- Envie essa variável
        "request": request,
    }
    return render(request, "servidores/pagina_servidores.html", context)


def servidor_inativar(request, id):
    servidor = get_object_or_404(Servidor, id=id)
    servidor.status = "Inativo"
    servidor.save()
    return redirect('pagina_servidores')

def servidor_ativar(request, id):
    servidor = get_object_or_404(Servidor, id=id)
    servidor.status = "Ativo"
    servidor.save()
    return redirect('pagina_servidores')

def servidor_editar(request, id):
    servidor = get_object_or_404(Servidor, id=id)
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

    return render(request, "servidores/editar_servidores.html", {
        "servidor": servidor,
        "cargos": cargos,
    })