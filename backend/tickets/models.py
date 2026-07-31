from django.db import models
from django.conf import settings
# Create your models here.
class Ticket(models.Model):
    class Prioridad(models.TextChoices):
        BAJA = 'BAJA', 'Baja'
        MEDIA = 'MEDIA', 'Media'
        ALTA = 'ALTA', 'Alta'
        CRITICA = 'CRITICA', 'Critica'

    class Estado(models.TextChoices):
        NUEVO = 'NUEVO', 'Nuevo'
        EN_REVISION = 'EN_REVISION', 'En revision'
        ESPERANDO_CLIENTE = 'ESPERANDO_CLIENTE', 'Esperando cliente'
        RESUELTO = 'RESUELTO', 'Resuelto'
        CERRADO = 'CERRADO', 'Cerrado'

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    prioridad = models.CharField(max_length=20, choices=Prioridad.choices, default=Prioridad.BAJA)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.NUEVO)
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='tickets_solicitados'
    )
    agente_asignado = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tickets_asignados'
    )
    departamento = models.ForeignKey(
        'departamentos.Departamento',
        on_delete=models.PROTECT,
        related_name='tickets'
    )
    fecha_vencimiento_sla = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'[{self.estado}] {self.titulo}'
