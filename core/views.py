from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login  
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import DocumentoCarga, Puerto, Validacion
from django.contrib.auth.models import User

# ---------- Vistas para el Dashboard ----------
@login_required
def dashboard(request):
    user = request.user

    # Datos del dashboard
    total_documentos = DocumentoCarga.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    total_puertos = Puerto.objects.count()
    validaciones_completadas = Validacion.objects.filter(estado='VALIDO').count()

    context = {
        'total_documentos': total_documentos,
        'usuarios_activos': usuarios_activos,
        'total_puertos': total_puertos,
        'validaciones_completadas': validaciones_completadas
    }

    # Render según rol
    if user.groups.filter(name="Administradores").exists():
        return render(request, 'core/dashboard_admin.html', context)
    elif user.groups.filter(name="Usuario").exists():
        return render(request, 'core/dashboard_usuario.html', context)
    elif user.groups.filter(name="Encargados").exists():
        return render(request, 'core/dashboard_encargado.html', context)

    return HttpResponseForbidden("No tienes un rol asignado.")

# ---------- API para Puertos (GET y POST) ----------
@csrf_exempt
def puertos_api(request):
    if request.method == 'GET':
        puertos = list(Puerto.objects.values())
        return JsonResponse(puertos, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        puerto = Puerto.objects.create(
            nombre=data['nombre'],
            pais=data['pais'],
            direccion=data['direccion'],
            estado=data['estado']
        )
        return JsonResponse({'id': puerto.id, 'mensaje': 'Puerto creado'})

# ---------- API para actualizar ----------
@csrf_exempt
def actualizar_puerto(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            puerto = Puerto.objects.get(id=id)
            puerto.nombre = data['nombre']
            puerto.pais = data['pais']
            puerto.direccion = data['direccion']
            puerto.estado = data['estado']
            puerto.save()
            return JsonResponse({'mensaje': 'Puerto actualizado'})
        except Puerto.DoesNotExist:
            return JsonResponse({'error': 'Puerto no encontrado'}, status=404)

# ---------- API para eliminar ----------
@csrf_exempt
def eliminar_puerto(request, id):
    if request.method == 'DELETE':
        try:
            Puerto.objects.get(id=id).delete()
            return JsonResponse({'mensaje': 'Puerto eliminado'})
        except Puerto.DoesNotExist:
            return JsonResponse({'error': 'Puerto no encontrado'}, status=404)

# ---------- Vistas HTML ----------
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

def api_puertos(request):
    if request.method == 'GET':
        puertos = list(Puerto.objects.values('id', 'nombre'))
        return JsonResponse(puertos, safe=False)

@csrf_exempt
def puerto_detalle(request, id):
    try:
        puerto = Puerto.objects.get(id=id)
    except Puerto.DoesNotExist:
        return JsonResponse({'error': 'Puerto no encontrado'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        puerto.nombre = data['nombre']
        puerto.pais = data['pais']
        puerto.direccion = data['direccion']
        puerto.estado = data['estado']
        puerto.save()
        return JsonResponse({'mensaje': 'Puerto actualizado'})

    elif request.method == 'DELETE':
        puerto.delete()
        return JsonResponse({'mensaje': 'Puerto eliminado'})

@login_required
@csrf_exempt
def subir_documento_api(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        puerto_id = request.POST.get('puerto')
        fecha = request.POST.get('fecha')
        observaciones = request.POST.get('observaciones', '')
        archivo = request.FILES.get('archivo_pdf')

        if not all([tipo, puerto_id, fecha, archivo]):
            return JsonResponse({'error': 'Datos incompletos.'}, status=400)

        try:
            puerto = Puerto.objects.get(id=puerto_id)
        except Puerto.DoesNotExist:
            return JsonResponse({'error': 'Puerto no válido.'}, status=404)

        doc = DocumentoCarga.objects.create(
            tipo=tipo,
            puerto=puerto,
            fecha=fecha,
            archivo_pdf=archivo,
            observaciones=observaciones,
            creado_por=request.user
        )
        return JsonResponse({'mensaje': 'Documento guardado exitosamente', 'id': doc.id})
    
@login_required
def cargar_documento(request):
    return render(request, 'core/cargar_documento.html')

@login_required
def vista_documentos(request):  # ← Renombrada para evitar conflicto
    return render(request, 'core/documentos.html')

@login_required
def vista_puertos(request):  # ← Renombrada para evitar conflicto
    return render(request, 'core/puertos.html')

@login_required
def listar_usuarios(request):
    return render(request, 'core/usuarios.html')

@login_required
def ver_validaciones(request):
    return render(request, 'core/validaciones.html')
