from django.contrib import admin

# Register your models here.
from models import (Cliente, Contacto_C, Direccion_Fiscal_Cliente,
                    Agencia_Automotriz, Contacto_Agencia, Caso,
                    Interaccion, Anotacion, Historial_Etapa, Cita,
                    Equipo_Solicitado)

admin.site.register(Anotacion)
admin.site.register(Cliente)
admin.site.register(Contacto_C)
admin.site.register(Agencia_Automotriz)
admin.site.register(Contacto_Agencia)
admin.site.register(Caso)
admin.site.register(Interaccion)
admin.site.register(Direccion_Fiscal_Cliente)
admin.site.register(Historial_Etapa)
admin.site.register(Cita)
admin.site.register(Equipo_Solicitado)
