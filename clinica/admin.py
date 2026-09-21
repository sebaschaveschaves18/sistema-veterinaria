from django.contrib import admin
from .models import Propietario, Mascota, ConsultaVeterinaria


class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'propietario', 'peso', 'activo')


admin.site.register(Propietario)
admin.site.register(Mascota, MascotaAdmin)
admin.site.register(ConsultaVeterinaria)
