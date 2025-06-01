from django import forms
from .models import DocumentoCarga

class DocumentoCargaForm(forms.ModelForm):
    class Meta:
        model = DocumentoCarga
        fields = ['tipo', 'fecha', 'archivo_pdf', 'PuertoRuta']
