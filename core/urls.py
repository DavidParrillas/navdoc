from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentos/', views.lista_documentos, name='documentos'),
    path('documentos/cargar/', views.cargar_documento, name='cargar_documento'),
    path('puertos/', views.listar_puertos, name='puertos'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('validaciones/', views.ver_validaciones, name='validaciones'),
]
