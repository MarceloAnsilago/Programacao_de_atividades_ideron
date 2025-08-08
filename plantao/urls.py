from django.urls import path
from . import views

app_name = 'plantao'

urlpatterns = [
    path('', views.pagina_plantao, name='pagina_plantao'),
    path('salvar/', views.salvar_plantao, name='salvar_plantao'),
    path('listar/', views.lista_plantoes, name='lista_plantoes'),
    path('escala/<int:id>/', views.escala_plantao_ajax, name='escala_plantao_ajax'),
    path('excluir/<int:id>/', views.excluir_plantao, name='excluir_plantao'),
    path('imprimir/<int:plantao_id>/', views.imprimir_plantao, name='imprimir_plantao'),
]