from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Atividade
from .forms import AtividadeForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Atividade
from .forms import AtividadeForm

@login_required
def lista_atividades(request):
    unidade = getattr(request.user, 'unidade', None)
    atividades = Atividade.objects.all()
    if unidade:
        atividades = atividades.filter(unidade=unidade)

    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')
    area = request.GET.get('area', '')

    if busca:
        atividades = atividades.filter(nome__icontains=busca)
    if status == 'ativo':
        atividades = atividades.filter(ativo=True)
    elif status == 'inativo':
        atividades = atividades.filter(ativo=False)
    if area:
        atividades = atividades.filter(area=area)

    areas = [
        ('animal', 'Animal'),
        ('vegetal', 'Vegetal'),
        ('apoio', 'Apoio'),
    ]

    status_opcoes = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    context = {
        'atividades': atividades,
        'areas': areas,
        'status_opcoes': status_opcoes,
        'request': request,
    }
    return render(request, 'atividades/lista_atividades.html', context)


@login_required
def cria_atividade(request):
    # Tenta pegar a unidade pelo perfilusuario
    unidade = None
    if hasattr(request.user, 'perfilusuario'):
        unidade = getattr(request.user.perfilusuario, 'unidade', None)
    print("UNIDADE FINAL:", unidade)

    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.unidade = unidade
            atividade.save()
            print("SALVOU ATIVIDADE!")
            return redirect('atividades:lista')
        else:
            print("ERROS NO FORM:", form.errors)
    else:
        form = AtividadeForm()
    # ... resto igual ...
    areas = [
        ('animal', 'Animal'),
        ('vegetal', 'Vegetal'),
        ('apoio', 'Apoio'),
    ]
    context = {
        'form': form,
        'titulo': 'Criar Atividade',
        'areas': areas,
        'request': request,
    }
    return render(request, 'atividades/form_atividade.html', context)


@login_required
def edita_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            return redirect('atividades:lista')
    else:
        form = AtividadeForm(instance=atividade)

    areas = [
        ('animal', 'Animal'),
        ('vegetal', 'Vegetal'),
        ('apoio', 'Apoio'),
    ]

    context = {
        'form': form,
        'atividade': atividade,
        'titulo': 'Editar Atividade',
        'areas': areas,  # aqui!
    }
    return render(request, 'atividades/form_atividade.html', context)

def deleta_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    if request.method == 'POST':
        atividade.delete()
        return redirect('atividades:lista')
    return render(request, 'atividades/confirma_delete.html', {'atividade': atividade})

def ativar_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    atividade.ativo = True
    atividade.save()
    return redirect('atividades:lista')

def inativar_atividade(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    atividade.ativo = False
    atividade.save()
    return redirect('atividades:lista')

