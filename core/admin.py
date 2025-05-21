from django.contrib import admin

from .models import Puerto, PerfilUsuario, DocumentoCarga, Validacion

admin.site.register(Puerto)
admin.site.register(PerfilUsuario)
admin.site.register(DocumentoCarga)
admin.site.register(Validacion)
