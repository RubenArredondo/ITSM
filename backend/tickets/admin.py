from django.contrib import admin
from .models import Ticket
# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'prioridad', 'estado', 'solicitante', 'agente_asignado', 'departamento')
    list_filter = ('prioridad', 'estado', 'departamento')
    search_fields = ('titulo', 'departamento__nombre')


