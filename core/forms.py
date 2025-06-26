from django import forms
from .models import DocumentoCarga
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DocumentoCargaForm(forms.ModelForm):
    class Meta:
        model = DocumentoCarga
        fields = ['tipo', 'fecha', 'archivo_pdf', 'PuertoRuta']

class CrearUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    #Etiquetas en el formulario
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nombre de Usuario"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"
