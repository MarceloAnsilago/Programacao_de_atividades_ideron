# organizacao/views_politicas.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PerfilPoliticaForm
from .models import PerfilPolitica

@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def lista_perfis(request):
    perfis = PerfilPolitica.objects.all().order_by('nome')
    return render(request, 'organizacao/politicas_lista.html', {'perfis': perfis})

@login_required
@permission_required('organizacao.manage_policies', raise_exception=True)
def editar_perfil(request, pk=None):
    perfil = get_object_or_404(PerfilPolitica, pk=pk) if pk else None
    if request.method == 'POST':
        form = PerfilPoliticaForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil salvo com sucesso.')
            return redirect('organizacao:politicas_lista')
    else:
        form = PerfilPoliticaForm(instance=perfil)
    return render(request, 'organizacao/politicas_editar.html', {'form': form, 'perfil': perfil})


