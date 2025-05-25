from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login  
from django.contrib import messages  
from .forms import DocumentoCargaForm
from django.shortcuts import render


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
    print(user.groups.all()) 

    if user.groups.filter(name="Administradores").exists():
        return render(request, 'core/dashboard_admin.html')
    elif user.groups.filter(name="Usuario").exists():
        return render(request, 'core/dashboard_usuario.html')
    elif user.groups.filter(name="Encargados").exists():
        return render(request, 'core/dashboard_encargado.html')

    return HttpResponseForbidden("No tienes un rol asignado.")

@login_required
def cargar_documento(request):
    return render(request, 'core/cargar_documento.html',)


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
