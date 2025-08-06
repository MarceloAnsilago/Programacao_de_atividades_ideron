from django.urls import path
from . import views

app_name = 'atividades'

urlpatterns = [
    path('', views.atividades_view, name='lista'),  # lista e criação unificada
    # Remova ou comente a linha abaixo se não tiver cria_atividade
    # path('nova/', views.cria_atividade, name='criar'),
    path('editar/<int:pk>/', views.edita_atividade, name='editar'),
    path('deletar/<int:pk>/', views.deleta_atividade, name='deletar'),
    path('ativar/<int:pk>/', views.ativar_atividade, name='ativar'),
    path('inativar/<int:pk>/', views.inativar_atividade, name='inativar'),
    path('', views.atividades_view, name='lista'),  # lista e criação
    path('editar/<int:pk>/', views.edita_atividade, name='editar'),  # edição separada

]