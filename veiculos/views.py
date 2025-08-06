from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Veiculo

@login_required
def pagina_veiculos(request):
    unidade_usuario = request.user.perfilusuario.unidade
    busca = request.GET.get('busca', '')
    placa = request.GET.get('placa', '')     # <-- ADICIONE ESTA LINHA!
    status = request.GET.get('status', '')
    veiculos = Veiculo.objects.filter(unidade=unidade_usuario)

    if busca:
        veiculos = veiculos.filter(nome__icontains=busca)
    if placa:
        veiculos = veiculos.filter(placa__icontains=placa)
    if status:
        veiculos = veiculos.filter(status=status)
    
    status_opcoes = [('Ativo', 'Ativo'), ('Inativo', 'Inativo')]

    if request.method == 'POST':
        nome = request.POST.get('nome')
        placa = request.POST.get('placa')
        if nome and placa:
            Veiculo.objects.create(
                nome=nome,
                placa=placa,
                unidade=unidade_usuario,
            )
            return redirect('pagina_veiculos')

    context = {
        'veiculos': veiculos,
        'status_opcoes': status_opcoes,
    }
    return render(request, 'veiculos/pagina_veiculos.html', context)


@login_required
def editar_veiculos(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    if request.method == 'POST':
        veiculo.nome = request.POST.get('nome')
        veiculo.placa = request.POST.get('placa')
        veiculo.save()
        return redirect('pagina_veiculos')
    return render(request, 'veiculos/editar_veiculos.html', {'veiculo': veiculo})

@login_required
def ativar_veiculo(request, veiculo_id):
    unidade_usuario = request.user.perfilusuario.unidade
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, unidade=unidade_usuario)
    veiculo.status = 'Ativo'
    veiculo.save()
    return redirect('pagina_veiculos')

@login_required
def inativar_veiculo(request, veiculo_id):
    unidade_usuario = request.user.perfilusuario.unidade
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, unidade=unidade_usuario)
    veiculo.status = 'Inativo'
    veiculo.save()
    return redirect('pagina_veiculos')
