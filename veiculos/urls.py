from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_veiculos, name='pagina_veiculos'),
    path('editar/<int:veiculo_id>/', views.editar_veiculos, name='editar_veiculos'),
    path('ativar/<int:veiculo_id>/', views.ativar_veiculo, name='ativar_veiculo'),
    path('inativar/<int:veiculo_id>/', views.inativar_veiculo, name='inativar_veiculo'),  
]