from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_descanso, name='pagina_descanso'),
    path('cadastrar/<int:servidor_id>/', views.cadastrar_descanso, name='cadastrar_descanso'),
    path('ver/<int:servidor_id>/', views.ver_descanso, name='ver_descanso'),
    path('editar/<int:descanso_id>/', views.editar_descanso, name='editar_descanso'),
    path('excluir/<int:descanso_id>/', views.excluir_descanso, name='excluir_descanso'),
    path('relatorio/', views.relatorio_mapa_ferias, name='relatorio_mapa_ferias'),
]
