from django.contrib import admin
from fideicomisos_backend import models as ModelosDelProyecto


admin.site.register(ModelosDelProyecto.Empleado)
admin.site.register(ModelosDelProyecto.Prestamo)
admin.site.register(ModelosDelProyecto.GastosFunerarios)
admin.site.register(ModelosDelProyecto.SeguroVida)
admin.site.register(ModelosDelProyecto.PrestamoAprobado)