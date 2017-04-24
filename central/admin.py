from django.contrib import admin

# Register your models here.
from models import (Contrato, Anexo, Factura)

admin.site.register(Contrato)
admin.site.register(Anexo)
admin.site.register(Factura)
