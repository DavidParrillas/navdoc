from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import DocumentoCargaForm

def home(request):
    return HttpResponse("¡Bienvenido a NavDoc desde la vista 'home'!")

def cargar_documento(request):
    if request.method == 'POST':
        form = DocumentoCargaForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.creado_por = request.user
            documento.save()
            return redirect('lista_documentos')
    else:
        form = DocumentoCargaForm()
    return render(request, 'cargar_documento.html', {'form': form})

def home(request):
    return HttpResponse("¡Bienvenido a NavDoc desde la vista 'home'!")
