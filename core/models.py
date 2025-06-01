from django.db import models
from django.contrib.auth.models import User

# Modelo para los puertos donde se desembarcan
class Puerto(models.Model):
    pais = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)  # True = activo, False = inactivo

    def __str__(self):
        return f"{self.nombre}, {self.pais} ({'Activo' if self.estado else 'Inactivo'})"

# Modelo para rutas de navegación
class Ruta(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True)  # True = Activa, False = Inactiva


# Modelo intermedio para relacionar puertos con rutas y mantener el orden
class PuertoRuta(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField()  # Indica el orden del puerto en la ruta

    class Meta:
        unique_together = ('ruta', 'puerto')
        ordering = ['orden']

    def __str__(self):
        return f"{self.ruta.nombre} - {self.puerto.nombre} (Orden {self.orden})"

# Perfil extendido del usuario con rol explícito
class PerfilUsuario(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('GESTOR', 'Gestor de Documentos'),
        ('ENCARGADO', 'Encargado de Puerto'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    puerto_asignado = models.ForeignKey(Puerto, null=True, blank=True, on_delete=models.SET_NULL)
    cargo = models.CharField(max_length=100, blank=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='ENCARGADO')

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

# Modelo para los documentos de carga
class DocumentoCarga(models.Model):
    TIPO_CHOICES = [
        ('FACTURA', 'Factura de Desembarco'),
        ('MANIFIESTO', 'Manifiesto'),
        ('CERTIFICADO', 'Certificado de Origen'),
        ('GUIA', 'Guía de Carga'),
        ('INSPECCION', 'Informe de Inspección'),
        ('PERMISO', 'Permiso o Licencia Especial'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    PuertoRuta = models.ForeignKey(PuertoRuta, on_delete=models.CASCADE)
    fecha = models.DateField()
    archivo_pdf = models.FileField(upload_to='documentos/')
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.PuertoRuta.puerto.nombre} - {self.fecha}"

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

    class Meta:
        unique_together = ('documento', 'usuario')

    def __str__(self):
        return f"{self.documento} - {self.estado} por {self.usuario.username}"
