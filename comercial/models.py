from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import date
from model_utils import FieldTracker

# Create your models here.

class Cliente(models.Model):
    SERVICIOS = 'SE'
    FABRICANTE = 'FA'
    COMERCIAL = 'CM'
    business_choices = (
        (SERVICIOS, 'servicios'),
        (FABRICANTE, 'fabricante'),
        (COMERCIAL, 'comercial'),
    )
    PROSPECTO = 'PR'
    CLIENTE_ACTIVO = 'CA'
    CLIENTE_PROSPECTO = 'CP'
    CLIENTE_INACTIVO = 'CI'
    PROSPECTO_FALLIDO = 'PF'
    status_choices = (
        (PROSPECTO, 'prospecto'),
        (CLIENTE_ACTIVO, 'cliente activo'),
        (CLIENTE_PROSPECTO, 'cliente prospecto'),
        (CLIENTE_INACTIVO, 'cliente inactivo'),
        (PROSPECTO_FALLIDO, 'prospecto fallido'),
    )
    RFC = models.CharField(max_length=40, unique=True)
    Persona_Moral = models.BooleanField(default=True)
    Nombre_Empresa = models.CharField(max_length=40, unique=True)
    Tipo_Negocio = models.CharField(max_length=2, choices=business_choices, default=SERVICIOS)
    Industria = models.CharField(max_length=40)
    Atiende = models.ForeignKey(User, blank=True)
    Status = models.CharField(max_length=2, choices=status_choices, default=PROSPECTO, blank=True)

    def get_absolute_url(self):
        return '/comercial/detalle_cliente/%d/' % self.pk

    def __unicode__(self):
        return self.Nombre_Empresa

class Direccion_Fiscal_Cliente(models.Model):
    Calle = models.CharField(max_length=140)
    Calle2 = models.CharField(max_length=140, blank=True, null=True)
    Colonia = models.CharField(max_length=40)
    Ciudad = models.CharField(max_length=40, default='CDMX')
    Estado = models.CharField(max_length=40, default='CDMX')
    Codigo_Postal = models.PositiveIntegerField()
    Pais = models.CharField(max_length=40, default='Mexico')
    Cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.Cliente.Nombre_Empresa + self.Calle

class Contacto_C(models.Model):
    REPRESENTANTE_LEGAL = 'RL'
    AVAL = 'AV'
    CONTADOR = 'CO'
    COMPRADOR = 'CM'
    rol_choices = (
        (REPRESENTANTE_LEGAL, 'representante legal'),
        (AVAL, 'aval'),
        (CONTADOR, 'contador'),
        (COMPRADOR, 'comprador'),
    )
    Nombre_del_Contacto = models.CharField(max_length=40)
    Rol = models.CharField(max_length=2, choices=rol_choices, default=COMPRADOR)
    Email = models.EmailField(blank=True, null=True)
    Telefono = models.CharField(max_length=40, blank=True, null=True)
    Celular = models.CharField(max_length=40, blank=True, null=True)
    Cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True)
    Atiende = models.ForeignKey(User, blank=True)

    class Meta:
        unique_together = ('Cliente', 'Nombre_del_Contacto',)

    def __unicode__(self):
        return self.Nombre_del_Contacto

class Agencia_Automotriz(models.Model):
    acura = 'AC'
    audi = 'AU'
    bmw = 'BM'
    chevrolet = 'CH'
    chrysler = 'CY'
    ford = 'FO'
    gmc = 'GM'
    honda = 'HO'
    hyundai = 'HY'
    kia = 'KI'
    infiniti = 'IN'
    isuzu = 'IZ'
    lincoln = 'LN'
    mazda = 'MZ'
    mercedes = 'MB'
    nissan = 'NI'
    seat = 'SE'
    volkswagen = 'VW'
    volvo = 'VO'
    brand_choices = (
        (acura, 'ACURA'),
        (audi, 'AUDI'),
        (bmw, 'BMW'),
        (chevrolet, 'CHEVROLET'),
        (chrysler, 'CHRYSLER'),
        (ford, 'FORD'),
        (gmc, 'GMC | BUICK'),
        (honda, 'HONDA'),
        (hyundai, 'HYUNDAI'),
        (kia, 'KIA'),
        (infiniti, 'INFINITI'),
        (isuzu, 'ISUZU'),
        (lincoln, 'LINCOLN'),
        (mazda, 'MAZDA'),
        (mercedes, 'MERCEDES BENZ'),
        (nissan, 'NISSAN'),
        (seat, 'SEAT'),
        (volkswagen, 'VOLKSWAGEN'),
        (volvo, 'VOLVO'),
    )
    alden = 'al'
    aeroplaza = 'ae'
    andrade = 'an'
    camsa = 'ca'
    cever = 'ce'
    dalton = 'da'
    excelencia = 'ge'
    picacho = 'pi'
    sonni = 'so'
    uribe = 'ur'
    independiente = 'in'
    corp_choices = (
        (alden, 'ALDEN'),
        (aeroplaza, 'AEROPLAZA AUT'),
        (andrade, 'ANDRADE'),
        (camsa, 'CAMSA'),
        (cever, 'CEVER'),
        (excelencia, 'GRUPO EXCELENCIA'),
        (picacho, 'PICACHO'),
        (dalton, 'DALTON'),
        (sonni, 'SONNI'),
        (uribe, 'URIBE'),
        (independiente, 'Independiente'),
    )
    Marca = models.CharField(max_length=2, choices=brand_choices, default=ford)
    Grupo = models.CharField(max_length=2, choices=corp_choices, default=alden)
    Ciudad = models.CharField(max_length=30)
    Colonia = models.CharField(max_length=30)
    Telefono = models.CharField(max_length=40)
    URL = models.CharField(max_length=40, blank=True, null=True)
    Atiende = models.ForeignKey(User, blank=True)

    class Meta:
        unique_together = ('Marca', 'Grupo', 'Colonia',)

    def get_absolute_url(self):
        return '/comercial/detalle_agencia/%d/' % self.pk

    def __unicode__(self):
        return self.get_Marca_display() + ' | ' + self.Ciudad + ' | ' + self.Colonia + ' | ' + self.Atiende.first_name

class Contacto_Agencia(models.Model):
    director = 'dir'
    gte_vtas = 'gv'
    fyi = 'fi'
    vendedor = 've'
    role_a_choices = (
        (director, 'Director'),
        (gte_vtas, 'Gerente de Ventas'),
        (fyi, 'F&I'),
        (vendedor, 'Vendedor'),
    )
    Nombre_del_Contacto = models.CharField(max_length=40)
    Rol = models.CharField(max_length=2, choices=role_a_choices, default=gte_vtas)
    Agencia = models.ForeignKey(Agencia_Automotriz, on_delete=models.CASCADE)
    Email = models.EmailField()
    Celular = models.CharField(max_length=40, blank=True, null=True)
    Atiende = models.ForeignKey(User, blank=True)

    class Meta:
        unique_together = ('Agencia', 'Email',)

    def __unicode__(self):
        return self.Nombre_del_Contacto

class Caso(models.Model):
    INTERES = 'int'
    COTIZACION = 'cot'
    ESPERANDO_PAPELES = 'epa'
    ESPERANDO_APROBACION = 'eap'
    APROBADO = 'apr'
    FONDEADO = 'fon'
    CERRADO = 'crd'
    PERDIDO = 'prd'
    RECHAZADO = 'rzo'
    stage_choices = (
        (INTERES, 'Interes'),
        (COTIZACION, 'Cotizacion Enviada'),
        (ESPERANDO_PAPELES, 'Esperando Papeles'),
        (ESPERANDO_APROBACION, 'Esperando Aprobacion'),
        (APROBADO, 'Aprobado'),
        (FONDEADO, 'Fondeado'),
        (CERRADO, 'Cerrado'),
        (PERDIDO, 'Perdido'),
        (RECHAZADO, 'Rechazado'),
    )
    Agencia = models.ForeignKey(Agencia_Automotriz, blank=True, null=True)
    Vendedor_Agencia = models.ForeignKey(Contacto_Agencia, blank=True, null=True)
    Atiende = models.ForeignKey(User, blank=True)
    Cliente = models.ForeignKey(Cliente, blank=True)
    Descripcion = models.TextField(max_length=500)
    Contacto = models.ForeignKey(Contacto_C, blank=True)
    Monto = models.PositiveIntegerField()
    Etapa = models.CharField(max_length=3, choices=stage_choices, default=INTERES)
    Buscar_el = models.DateField()
    Requiere_revision_admon = models.BooleanField(default=False, blank=True)
    Requiere_revision_vtas = models.BooleanField(default=False, blank=True)
    Activo = models.BooleanField(default=True, blank=True)

    tracker = FieldTracker()

    def get_absolute_url(self):
        return '/comercial/detalle_caso/%d/' % self.pk

    def __unicode__(self):
        return self.Cliente.Nombre_Empresa + ' | ' + self.Descripcion + ' | ' + self.get_Etapa_display()

class Historial_Etapa(models.Model):
    INTERES = 'int'
    COTIZACION = 'cot'
    ESPERANDO_PAPELES = 'epa'
    ESPERANDO_APROBACION = 'eap'
    APROBADO = 'apr'
    FONDEADO = 'fon'
    CERRADO = 'crd'
    PERDIDO = 'prd'
    RECHAZADO = 'rzo'
    stage_choices = (
        (INTERES, 'Interes'),
        (COTIZACION, 'Cotizacion Enviada'),
        (ESPERANDO_PAPELES, 'Esperando Papeles'),
        (ESPERANDO_APROBACION, 'Esperando Aprobacion'),
        (APROBADO, 'Aprobado'),
        (FONDEADO, 'Fondeado'),
        (CERRADO, 'Cerrado'),
        (PERDIDO, 'Perdido'),
        (RECHAZADO, 'Rechazado'),
    )
    Caso = models.ForeignKey(Caso, blank=True)
    Etapa = models.CharField(max_length=3, choices=stage_choices, default=INTERES)
    Fecha = models.DateTimeField(auto_now_add=True, blank=True)

class Interaccion(models.Model):
    del_Caso = models.ForeignKey(Caso, blank=True)
    Numero = models.PositiveIntegerField(blank=True)
    Fecha = models.DateTimeField(auto_now_add=True, blank=True)
    Descripcion = models.TextField(max_length=500)
    Buscar_el = models.DateField()
    Hecha_por = models.ForeignKey(User, blank=True)
    Hist_Etapa = models.ForeignKey(Historial_Etapa, blank=True)

    def __unicode__(self):
        return str(self.Numero) + ' | ' + self.del_Caso.Cliente.Nombre_Empresa + ' | ' + self.del_Caso.Descripcion + ' | ' + str(self.Fecha)

class Anotacion(models.Model):
    al_Caso = models.ForeignKey(Caso, blank=True)
    Requerimiento = models.TextField(max_length=300)
    Fecha = models.DateTimeField(auto_now_add=True, blank=True)
    Hecha_por = models.ForeignKey(User, blank=True)
    Hist_Etapa = models.ForeignKey(Historial_Etapa, blank=True)

    def __unicode__(self):
        return self.al_Caso.Cliente.Nombre_Empresa + ' | ' + self.Requerimiento

class Cita(models.Model):
    Agencia = models.ForeignKey(Agencia_Automotriz, blank=True, null=True)
    Cliente = models.ForeignKey(Cliente, blank=True, null=True)
    Fecha = models.DateField()
    Hora = models.TimeField()
    Descripcion = models.CharField(max_length=140, blank=True)
    Atiende = models.ForeignKey(User, blank=True)

    class Meta:
        unique_together = ('Fecha', 'Hora', 'Atiende',)

    def get_absolute_url(self):
        return '/comercial/detalle_cita/%d/' % self.pk

    def __unicode__(self):
        if self.Cliente:
            return self.Cliente.Nombre_Empresa + ' | ' + self.Descripcion
        elif self.Agencia:
            return self.Agencia.get_Marca_display() + ' | ' + self.Agencia.Colonia
