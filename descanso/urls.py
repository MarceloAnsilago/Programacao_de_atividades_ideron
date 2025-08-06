from django.urls import path
from . import views

urlpatterns = [
    path('', views.pagina_descanso, name='pagina_descanso'),
    path('cadastrar/<int:servidor_id>/', views.cadastrar_descanso, name='cadastrar_descanso'),
    path('ver/<int:servidor_id>/', views.ver_descanso, name='ver_descanso'),
]