from django.contrib import admin
from .models import Ticket, ComentarioTicket
# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'prioridad', 'estado', 'solicitante', 'agente_asignado', 'departamento')
    list_filter = ('prioridad', 'estado', 'departamento')
    search_fields = ('titulo', 'departamento__nombre')

@admin.register(ComentarioTicket)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'ticket', 'autor', 'fecha_creacion')
    list_filter = ('autor', )
    search_fields = ('texto', )
