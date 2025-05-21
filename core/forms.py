from django import forms
from .models import DocumentoCarga

class DocumentoCargaForm(forms.ModelForm):
    class Meta:
        model = DocumentoCarga
        fields = ['tipo', 'puerto', 'fecha', 'archivo_pdf', 'observaciones']
