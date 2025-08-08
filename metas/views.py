
# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from atividades.models import Atividade  # Importa do app atividades
from .models import Meta
@login_required
def pagina_metas(request):
    unidade = getattr(getattr(request.user, 'perfilusuario', None), 'unidade', None)
    if not unidade:
        return render(request, 'atividades/sem_unidade.html', {
            'mensagem': 'Seu usuário não está vinculado a nenhuma unidade. Contate o administrador.'
        })

    # QuerySet base igual ao app atividades
    atividades = Atividade.objects.filter(unidade=unidade)

    # Filtros GET
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

    return render(request, 'metas/pagina_metas.html', {
        'metas': atividades,  # Aqui mudamos o nome da variável para "metas"
        'areas': areas,
        'status_opcoes': status_opcoes,
        'request': request,
    })

def definir_meta(request, pk):
    meta = get_object_or_404(Atividade, pk=pk)

    if request.method == "POST":
        quantidade = request.POST.get('quantidade')
        prazo = request.POST.get('prazo')
        observacoes = request.POST.get('observacoes')
        # Aqui você salva esses dados em um model (que vamos criar depois)
        # Por enquanto, só redireciona de volta, ou renderiza a página de novo.
        return redirect('metas:pagina_metas')

    return render(request, 'metas/definir_metas.html', {'meta': meta})


@login_required
def definir_meta(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)

    if request.method == "POST":
        quantidade = request.POST.get('quantidade')
        prazo = request.POST.get('prazo')
        observacoes = request.POST.get('observacoes')
        usuario = request.user

        # Aqui você define o destinatário conforme a regra de negócio. Exemplo, unidade do usuário:
        unidade = getattr(getattr(request.user, 'perfilusuario', None), 'unidade', None)
        supervisao = getattr(getattr(request.user, 'perfilusuario', None), 'supervisao', None)

        meta = Meta.objects.create(
            atividade=atividade,
            quantidade=quantidade,
            prazo=prazo,
            observacoes=observacoes,
            autor=usuario,
            destinatario_unidade=unidade,
            destinatario_supervisao=supervisao,
        )
        return redirect('metas:definir_meta', pk=atividade.pk)

    # Lista todas as metas já cadastradas para essa atividade
    metas = Meta.objects.filter(atividade=atividade).order_by('-criada_em')

    return render(request, 'metas/definir_metas.html', {
        'meta_atividade': atividade,
        'metas': metas,
    })

@login_required
def atribuir_meta(request, meta_id):
    meta = get_object_or_404(Meta, id=meta_id)
    # Aqui você pode depois adicionar lógica de atribuição, form, etc.
    return render(request, 'metas/atribuir.html', {'meta': meta})