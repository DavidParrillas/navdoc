import os
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login  
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages  
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect, get_object_or_404

from .models import DocumentoCarga, Puerto, Validacion, Ruta, PuertoRuta
from django.contrib.auth.models import User


# Decorador para controlar acceso por grupos
def grupo_requerido(*grupos):
    def en_grupo(user):
        return user.is_authenticated and user.groups.filter(name__in=grupos).exists()
    return user_passes_test(en_grupo, login_url='login')

# ---------- Dashboard ----------
@login_required
def dashboard(request):
    user = request.user

    context = {
        'total_documentos': DocumentoCarga.objects.count(),
        'usuarios_activos': User.objects.filter(is_active=True).count(),
        'total_puertos': Puerto.objects.count(),
        'validaciones_completadas': Validacion.objects.filter(estado='VALIDO').count()
    }

    if user.groups.filter(name="Administradores").exists():
        template = 'core/dashboard_admin.html'
    elif user.groups.filter(name="Usuario").exists():
        template = 'core/dashboard_usuario.html'
    elif user.groups.filter(name="Encargados").exists():
        template = 'core/dashboard_encargado.html'
    else:
        return HttpResponseForbidden("No tienes un rol asignado.")

    return render(request, template, context)


# ---------- API Puertos ----------
@csrf_exempt
@login_required
@grupo_requerido('Administradores')
def puertos_api(request):
    if request.method == 'GET':
        puertos = list(Puerto.objects.values())
        return JsonResponse(puertos, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        nombre = data.get('nombre')
        pais = data.get('pais')
        direccion = data.get('direccion')
        estado = data.get('estado', True)

        if not all([nombre, pais, direccion]):
            return JsonResponse({'error': 'Datos incompletos'}, status=400)

        puerto = Puerto.objects.create(
            nombre=nombre,
            pais=pais,
            direccion=direccion,
            estado=estado
        )
        return JsonResponse({'id': puerto.id, 'mensaje': 'Puerto creado'})

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
@login_required
@grupo_requerido('Administradores')
def puerto_detalle(request, id):
    try:
        puerto = Puerto.objects.get(id=id)
    except Puerto.DoesNotExist:
        return JsonResponse({'error': 'Puerto no encontrado'}, status=404)

    if request.method == 'GET':
        data = {
            'id': puerto.id,
            'nombre': puerto.nombre,
            'pais': puerto.pais,
            'direccion': puerto.direccion,
            'estado': puerto.estado,
        }
        return JsonResponse(data)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        puerto.nombre = data.get('nombre', puerto.nombre)
        puerto.pais = data.get('pais', puerto.pais)
        puerto.direccion = data.get('direccion', puerto.direccion)
        puerto.estado = data.get('estado', puerto.estado)
        puerto.save()
        return JsonResponse({'mensaje': 'Puerto actualizado'})

    elif request.method == 'DELETE':
        puerto.delete()
        return JsonResponse({'mensaje': 'Puerto eliminado'})

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
@login_required
@grupo_requerido('Administradores', 'Usuario')
def rutas_api(request):
    if request.method == 'GET':
        rutas_db = Ruta.objects.filter(estado=True)  # solo activas
        rutas = [{'id': ruta.id, 'nombre': ruta.nombre} for ruta in rutas_db]
        return JsonResponse(rutas, safe=False)

    elif request.method == 'POST':
        # tu código actual para crear rutas
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        nombre = data.get('nombre')
        if not nombre:
            return JsonResponse({'error': 'El nombre es obligatorio'}, status=400)

        if Ruta.objects.filter(nombre=nombre).exists():
            return JsonResponse({'error': 'Ya existe una ruta con ese nombre.'}, status=400)

        descripcion = data.get('descripcion', '')
        puertos_ids = data.get('puertos', [])

        try:
            ruta = Ruta.objects.create(nombre=nombre, descripcion=descripcion)
            for orden, pid in enumerate(puertos_ids, start=1):
                puerto = Puerto.objects.filter(id=pid).first()
                if puerto:
                    PuertoRuta.objects.create(ruta=ruta, puerto=puerto, orden=orden)
        except IntegrityError:
            return JsonResponse({'error': 'Error al crear la ruta.'}, status=400)

        return JsonResponse({'id': ruta.id, 'mensaje': 'Ruta creada'})

    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt
@login_required
@grupo_requerido('Administradores')
def detalle_ruta(request, id):
    try:
        ruta = Ruta.objects.get(id=id)
    except Ruta.DoesNotExist:
        return JsonResponse({'error': 'Ruta no encontrada'}, status=404)

    if request.method == 'GET':
        puertos_ruta = PuertoRuta.objects.filter(ruta=ruta).order_by('orden')
        data_puertos = [{'id': pr.puerto.id, 'nombre': pr.puerto.nombre, 'orden': pr.orden} for pr in puertos_ruta]

        data = {
            'id': ruta.id,
            'nombre': ruta.nombre,
            'descripcion': ruta.descripcion,
            'estado': ruta.estado,
            'puertos': data_puertos
        }
        return JsonResponse(data)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        ruta.nombre = data.get('nombre', ruta.nombre)
        ruta.descripcion = data.get('descripcion', ruta.descripcion)
        ruta.estado = data.get('estado', ruta.estado)
        ruta.save()

        puertos_ids = data.get('puertos', None)
        if puertos_ids is not None:
            PuertoRuta.objects.filter(ruta=ruta).delete()
            for orden, pid in enumerate(puertos_ids, start=1):
                try:
                    puerto = Puerto.objects.get(id=pid)
                    PuertoRuta.objects.create(ruta=ruta, puerto=puerto, orden=orden)
                except Puerto.DoesNotExist:
                    continue

        return JsonResponse({'mensaje': 'Ruta actualizada'})

    elif request.method == 'DELETE':
        ruta.delete()
        return JsonResponse({'mensaje': 'Ruta eliminada'})

    # Si llega un método HTTP no soportado
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# ---------- Vista para listar rutas con puertos ----------
@login_required
@grupo_requerido('Administradores')
def lista_rutas(request):
    rutas = Ruta.objects.all()
    rutas_con_puertos = []
    for ruta in rutas:
        puertos = PuertoRuta.objects.filter(ruta=ruta).order_by('orden')
        rutas_con_puertos.append({
            'ruta': ruta,
            'puertos': [pr.puerto for pr in puertos],
        })
    return render(request, 'core/lista_rutas.html', {'rutas_con_puertos': rutas_con_puertos})


# ---------- Subir documento ----------
@login_required
@csrf_exempt
@grupo_requerido('Administradores', 'Usuario')
def subir_documento_api(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        ruta_id = request.POST.get('ruta')  # id de la ruta seleccionada
        fecha = request.POST.get('fecha')
        archivo = request.FILES.get('archivo_pdf')

        if not all([tipo, ruta_id, fecha, archivo]):
            return JsonResponse({'error': 'Datos incompletos.'}, status=400)

        try:
            ruta = Ruta.objects.get(id=ruta_id)
            puerto_ruta = PuertoRuta.objects.filter(ruta=ruta).order_by('orden').first()
            if not puerto_ruta:
                return JsonResponse({'error': 'La ruta no tiene puertos asignados.'}, status=400)
        except Ruta.DoesNotExist:
            return JsonResponse({'error': 'Ruta no válida.'}, status=404)

        DocumentoCarga.objects.create(
            tipo=tipo,
            PuertoRuta=puerto_ruta,
            fecha=fecha,
            archivo_pdf=archivo,
            creado_por=request.user
        )
        return JsonResponse({'mensaje': 'Documento guardado exitosamente'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)
        
# ---------- Vista para renderizar rutas y puertos para frontend ----------
@login_required
@grupo_requerido('Administradores', 'Usuario')
def rutas_view(request):
    puertos = Puerto.objects.filter(estado=True)
    rutas = Ruta.objects.all().prefetch_related('puertoruta_set__puerto')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado') == 'true'
        puertos_ids = request.POST.getlist('puertos[]')

        with transaction.atomic():
            ruta = Ruta.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                estado=estado
            )
            for orden, pid in enumerate(puertos_ids, start=1):
                puerto = get_object_or_404(Puerto, id=pid)
                PuertoRuta.objects.create(ruta=ruta, puerto=puerto, orden=orden)

        messages.success(request, f"Ruta '{ruta.nombre}' creada correctamente.")
        return redirect('rutas')

    context = {
        'rutas': rutas,
        'puertos': puertos,
    }
    return render(request, 'core/rutas.html', context)


# ---------- Vistas HTML protegidas ----------
@login_required
@grupo_requerido('Administradores')
def vista_puertos(request):
    return render(request, 'core/puertos.html')


@login_required
@grupo_requerido('Administradores')
def listar_usuarios(request):
    return render(request, 'core/usuarios.html')


@login_required
@grupo_requerido('Administradores', 'Encargados')
def ver_validaciones(request):
    return render(request, 'core/validaciones.html')


@login_required
@grupo_requerido('Administradores', 'Usuario')
def cargar_documento(request):
    rutas = PuertoRuta.objects.select_related('ruta', 'puerto').order_by('ruta__nombre', 'orden')
    documentos = DocumentoCarga.objects.filter(creado_por=request.user).order_by('-fecha')[:5]  # últimos 5 docs del usuario

    return render(request, 'core/cargar_documento.html', {
        'rutas': rutas,
        'documentos': documentos,
    })


@login_required
@grupo_requerido('Administradores', 'Usuario', 'Encargados')
def vista_documentos(request):
    return render(request, 'core/documentos.html')


@login_required
@grupo_requerido('Administradores')
def lista_rutas_html(request):
    return render(request, 'core/rutas.html')


def home(request):
    return render(request, 'core/home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")  

    return render(request, 'core/login.html')
