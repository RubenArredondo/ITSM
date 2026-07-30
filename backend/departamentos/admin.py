from django.contrib import admin
from .models import Departamento
# Register your models here.

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display =  ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)

