from django.urls import path
from . import views, views_politicas, views_vinculos

app_name = "organizacao"  # <<< ADICIONE ISTO

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("politicas/", views_politicas.lista_perfis, name="politicas_lista"),
    path("politicas/novo/", views_politicas.editar_perfil, name="politicas_novo"),
    path("politicas/<int:pk>/", views_politicas.editar_perfil, name="politicas_editar"),
    path("vinculos/", views_vinculos.vinculos_home, name="vinculos_home"),
    path("vinculos/seletor/<int:perfil_id>/", views_vinculos.vinculos_seletor, name="vinculos_seletor"),
    path("vinculos/<int:perfil_id>/<int:unidade_id>/", views_vinculos.vinculos_editar, name="vinculos_editar"),
    path("api/unidades/<int:supervisao_id>/", views_vinculos.unidades_por_supervisao, name="api_unidades_por_supervisao"),
    path("permissoes/seletor/<int:perfil_id>/", views_vinculos.permissoes_seletor, name="permissoes_seletor"),
]
