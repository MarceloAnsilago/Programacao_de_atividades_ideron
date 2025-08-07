from django.urls import path
from . import views

app_name = 'plantao'

urlpatterns = [
    path('', views.pagina_plantao, name='pagina_plantao'),
    path('salvar/', views.salvar_plantao, name='salvar_plantao'),
    # ... outras rotas ...
]