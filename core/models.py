from django.db import models
from django.contrib.auth.models import User

# Modelo para los puertos donde se desembarcan 
class Puerto(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

# Perfil extendido del usuario
class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    puerto_asignado = models.ForeignKey(Puerto, null=True, blank=True, on_delete=models.SET_NULL)
    cargo = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.cargo})"

# Modelo para los documentos de carga
class DocumentoCarga(models.Model):
    TIPO_CHOICES = [
        ('FACTURA', 'Factura de Desembarco'),
        ('MANIFIESTO', 'Manifiesto'),
        ('CERTIFICADO', 'Certificado de Origen'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
    fecha = models.DateField()
    archivo_pdf = models.FileField(upload_to='documentos/')
    observaciones = models.TextField(blank=True)
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.puerto.nombre} - {self.fecha}"

# Validación de los documentos por los encargados del puerto
class Validacion(models.Model):
    ESTADO_CHOICES = [
        ('VALIDO', 'Válido'),
        ('RECHAZADO', 'Rechazado'),
        ('PENDIENTE', 'Pendiente'),
    ]

    documento = models.ForeignKey(DocumentoCarga, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    comentario = models.TextField(blank=True)
    fecha_validacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.documento} - {self.estado} por {self.usuario.username}"
