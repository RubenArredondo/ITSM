from django.contrib.auth.models import AbstractUser
from django.db import models

class User (AbstractUser):
    class Rol(models.TextChoices):
        CLIENTE = 'CLIENTE', 'Cliente'
        AGENTE = 'AGENTE', 'Agente'
        SUPERVISOR = 'SUPERVISOR', 'Supervisor'

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.CLIENTE)

    departamento = models.ForeignKey(
        'departamentos.Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
    )

    def __str__(self) -> str:
        return f'{self.username} ({self.rol})'
