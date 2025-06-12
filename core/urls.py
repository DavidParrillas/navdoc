from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views
print('urls.py cargado')

urlpatterns = [
    # Páginas principales (HTML)
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentos/', views.lista_documentos, name='documentos'),
    path('documentos/cargar/', views.cargar_documento, name='cargar_documento'),
    path('puertos/', views.vista_puertos, name='puertos'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('validaciones/', views.lista_validaciones, name='validaciones'),
    path('buscar-documentos/', views.buscar_documentos, name='buscar_documentos'),

    # API Puertos
    path('api/puertos/', views.puertos_api, name='puertos_api'),
    path('api/puertos/<int:id>/', views.puerto_detalle, name='puerto_detalle'),

    # API Documentos
    path('api/documentos/subir/', views.subir_documento_api, name='subir_documento_api'),

    # API Rutas (funciones)
    path('api/rutas/', views.rutas_api, name='rutas_api'),
    path('api/rutas/<int:id>/', views.detalle_ruta, name='detalle_ruta'),
    path('rutas/', views.rutas_view, name='rutas'),

    #Actualizar estados
    path('validaciones/actualizar_estado/<int:pk>/', views.actualizar_estado, name='actualizar_estado'),

    #Eliminar usuario
    path('usuarios/eliminar/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    #Actualizar usuario
    path('usuarios/editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),




    
]
