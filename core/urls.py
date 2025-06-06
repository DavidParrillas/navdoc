from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # Páginas principales (HTML)
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentos/', views.vista_documentos, name='documentos'),
    path('documentos/cargar/', views.cargar_documento, name='cargar_documento'),
    path('puertos/', views.vista_puertos, name='puertos'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('validaciones/', views.ver_validaciones, name='validaciones'),

    # API Puertos
    path('api/puertos/', views.puertos_api, name='puertos_api'),
    path('api/puertos/<int:id>/', views.puerto_detalle, name='puerto_detalle'),

    # API Documentos
    path('api/documentos/subir/', views.subir_documento_api, name='subir_documento_api'),

    # API Rutas (funciones)
    path('api/rutas/', views.rutas_api, name='rutas_api'),
    path('api/rutas/<int:id>/', views.detalle_ruta, name='detalle_ruta'),
    path('rutas/', views.rutas_view, name='rutas'),

    
]
