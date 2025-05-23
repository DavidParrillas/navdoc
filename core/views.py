from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  
from django.contrib import messages  
from .forms import DocumentoCargaForm

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

@login_required
def dashboard(request):
    user = request.user

    if user.groups.filter(name="Administradores").exists():
        return render(request, 'core/dashboard_admin.html')
    elif user.groups.filter(name="Usuarios").exists():
        return render(request, 'core/dashboard_usuario.html')
    elif user.groups.filter(name="Encargados").exists():
        return render(request, 'core/dashboard_encargado.html')

    return HttpResponseForbidden("No tienes un rol asignado.")

@login_required
def cargar_documento(request):
    if not request.user.groups.filter(name__in=["Usuarios", "Administradores"]).exists():
        return HttpResponseForbidden("No tienes permiso para subir documentos.")

    if request.method == 'POST':
        form = DocumentoCargaForm(request.POST, request.FILES)
    else:
        form = DocumentoCargaForm()

    # Asignar queryset aquí, de forma segura y controlada por la vista
    from .models import Puerto
    form.fields['puerto'].queryset = Puerto.objects.all()

    if request.method == 'POST' and form.is_valid():
        documento = form.save(commit=False)
        documento.creado_por = request.user
        documento.save()
        return redirect('documentos')

    return render(request, 'core/cargar_documento.html', {'form': form})


# Vista: Documentos
@login_required
def lista_documentos(request):
    return render(request, 'core/documentos.html')

# Vista: Puertos
@login_required
def listar_puertos(request):
    return render(request, 'core/puertos.html')

# Vista: Usuarios
@login_required
def listar_usuarios(request):
    return render(request, 'core/usuarios.html')

# Vista: Validaciones
@login_required
def ver_validaciones(request):
    return render(request, 'core/validaciones.html')
