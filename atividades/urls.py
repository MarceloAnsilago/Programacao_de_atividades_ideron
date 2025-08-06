from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('', views.lista_atividades, name='lista'),  # <-- agora está certo!
    # Outras rotas:
    path('editar/<int:pk>/', views.edita_atividade, name='editar'),
    path('deletar/<int:pk>/', views.deleta_atividade, name='deletar'),
    path('ativar/<int:pk>/', views.ativar_atividade, name='ativar'),
    path('inativar/<int:pk>/', views.inativar_atividade, name='inativar'),
]