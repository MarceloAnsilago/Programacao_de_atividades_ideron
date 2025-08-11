# organizacao/seed_perfis.py
from django.contrib.auth.models import Permission
from organizacao.models import PerfilPolitica

def run():
    # Atividades
    view_ativ = Permission.objects.get(codename='view_atividade', content_type__app_label='atividades')
    add_ativ = Permission.objects.get(codename='add_atividade', content_type__app_label='atividades')
    change_ativ = Permission.objects.get(codename='change_atividade', content_type__app_label='atividades')
    delete_ativ = Permission.objects.get(codename='delete_atividade', content_type__app_label='atividades')

    # Perfil Unidade — apenas visualizar
    unidade, _ = PerfilPolitica.objects.get_or_create(nome='Unidade', defaults={'descricao': 'Perfil base de unidade'})
    unidade.permissoes.set([view_ativ])

    # Perfil Supervisor — visualizar + criar/editar
    supervisor, _ = PerfilPolitica.objects.get_or_create(nome='Supervisor', defaults={'descricao': 'Perfil de supervisão'})
    supervisor.permissoes.set([view_ativ, add_ativ, change_ativ])

    # Perfil Gerente — todas as permissões do app atividades
    gerente, _ = PerfilPolitica.objects.get_or_create(nome='Gerente', defaults={'descricao': 'Perfil de gerência'})
    gerente.permissoes.set([view_ativ, add_ativ, change_ativ, delete_ativ])

    print("Perfis padrão criados/atualizados com sucesso!")
