from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Atividade
from .forms import AtividadeForm
from django.contrib.auth.decorators import login_required
from .models import Atividade
from .forms import AtividadeForm


@login_required
def lista_atividades(request):
    # pega unidade
    unidade = getattr(getattr(request.user, 'perfilusuario', None), 'unidade', None)
    if not unidade:
        return render(request, 'atividades/sem_unidade.html', {
            'mensagem': 'Seu usuário não está vinculado a nenhuma unidade. Contate o administrador.'
        })

    # POST → salva nova atividade
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            ativ = form.save(commit=False)
            ativ.unidade = unidade
            ativ.save()
            return redirect('atividades:lista')
    else:
        form = AtividadeForm()

    # QuerySet base
    atividades = Atividade.objects.filter(unidade=unidade)

    # filtros GET
    busca   = request.GET.get('busca', '')
    status  = request.GET.get('status', '')
    area    = request.GET.get('area', '')

    if busca:
        atividades = atividades.filter(nome__icontains=busca)
    if status == 'ativo':
        atividades = atividades.filter(ativo=True)
    elif status == 'inativo':
        atividades = atividades.filter(ativo=False)
    if area:
        atividades = atividades.filter(area=area)

    # opções de select
    areas = [
        ('animal', 'Animal'),
        ('vegetal', 'Vegetal'),
        ('apoio',   'Apoio'),
    ]
    status_opcoes = [
        ('ativo',   'Ativo'),
        ('inativo', 'Inativo'),
    ]

    return render(request, 'atividades/lista_atividades.html', {
        'form': form,
        'atividades': atividades,
        'areas': areas,
        'status_opcoes': status_opcoes,
        # ⚠️ precisamos do request para ler request.GET no template
        'request': request,
    })

@login_required
def atividades_view(request):
    unidade = getattr(getattr(request.user, 'perfilusuario', None), 'unidade', None)
    if not unidade:
        return render(request, 'atividades/sem_unidade.html', {
            'mensagem': 'Seu usuário não está vinculado a nenhuma unidade. Contate o administrador.'
        })

    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.unidade = unidade
            atividade.save()
            return redirect('atividades:lista')
    else:
        form = AtividadeForm()

    atividades = Atividade.objects.filter(unidade=unidade)

    # Filtros GET (busca, status, area)
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

    # Extraindo valores seguros do form para o template
    value_nome = form['nome'].value() if form and 'nome' in form.fields else ''
    value_area = form['area'].value() if form and 'area' in form.fields else ''

    context = {
        'form': form,
        'atividades': atividades,
        'areas': areas,
        'status_opcoes': status_opcoes,
        'request': request,
        'titulo': 'Gerenciar Atividades',
        'value_nome': value_nome,
        'value_area': value_area,
    }
    return render(request, 'atividades/form_atividade.html', context)


@login_required
def atividades_view(request):
    # Pega a unidade do usuário logado
    unidade = getattr(getattr(request.user, 'perfilusuario', None), 'unidade', None)
    if not unidade:
        return render(request, 'atividades/sem_unidade.html', {
            'mensagem': 'Seu usuário não está vinculado a nenhuma unidade. Contate o administrador.'
        })

    # Trata o POST para criar nova atividade
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.unidade = unidade
            atividade.save()
            return redirect('atividades:lista')
    else:
        form = AtividadeForm()

    # Consulta inicial das atividades da unidade do usuário
    atividades = Atividade.objects.filter(unidade=unidade)

    # Aplicar filtros GET
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
        'form': form,
        'atividades': atividades,
        'areas': areas,
        'status_opcoes': status_opcoes,
        'titulo': 'Cadastrar Atividade',
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
        'areas': areas,
    }
    return render(request, 'atividades/editar_atividade.html', context)

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

