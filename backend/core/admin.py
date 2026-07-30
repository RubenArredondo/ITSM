from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'departamento', 'is_staff')
    list_filter = ('rol', 'departamento', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (('Datos de soporte', {'fields': ('rol', 'departamento'),}),)

    add_fieldsets = UserAdmin.add_fieldsets + (('Datos de soporte', {'fields': ('rol', 'departamento'),}),)
