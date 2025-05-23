from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentos/', views.lista_documentos, name='documentos'),
    path('documentos/cargar/', views.cargar_documento, name='cargar_documento'), 
    path('puertos/', views.listar_puertos, name='puertos'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('validaciones/', views.ver_validaciones, name='validaciones'),
]