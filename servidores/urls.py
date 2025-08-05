from django.urls import path
from . import views  # apenas um tipo de importação é suficiente e ideal

urlpatterns = [
    path('', views.pagina_servidores, name='pagina_servidores'),
    path('servidor/<int:id>/editar/', views.servidor_editar, name='servidor_editar'),
    path('servidor/<int:id>/ativar/', views.servidor_ativar, name='servidor_ativar'),
    path('servidor/<int:id>/inativar/', views.servidor_inativar, name='servidor_inativar'),
    path('editar/<int:id>/', views.servidor_editar, name='servidor_editar'),
    path('', views.pagina_servidores, name='pagina_servidores'),
]