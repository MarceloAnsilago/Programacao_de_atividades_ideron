from django.urls import path
from . import views


app_name = 'metas'
urlpatterns = [
    path('', views.pagina_metas, name='pagina_metas'),
    path('definir/<int:pk>/', views.definir_meta, name='definir'),
  
   
   
]