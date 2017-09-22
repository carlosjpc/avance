from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from datetime import date

from comercial import models as comercial_models
# Create your models here.


class Contrato(models.Model):
    Num_Contrato = models.PositiveIntegerField(unique=True)
    Cliente = models.ForeignKey(comercial_models.Cliente, blank=True)
    Nombre_Rep_Legal = models.CharField(max_length=100)
    Nombre_Aval = models.CharField(max_length=100)
    Fecha = models.DateField()
    Scan_Contrato = models.FileField(upload_to=None, max_length=100,
                                     blank=True, null=True)

    def __unicode__(self):
        return ('#' + str(self.Num_Contrato) + ' Cliente: '
                + self.Cliente.Empresa)


class Anexo(models.Model):
    Num_Anexo = models.PositiveIntegerField()
    Contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE,
                                 blank=True)
    Cliente = models.ForeignKey(comercial_models.Cliente, blank=True)
    FISO = models.CharField(max_length=20)
    Fecha_Inicio = models.DateField(blank=True)
    Plazo_Meses = models.PositiveIntegerField()
    Monto_Anexo = models.PositiveIntegerField()
    Vendedor_Avance = models.ForeignKey(User, blank=True)
    Procedente_de = models.ForeignKey(comercial_models.Caso)
    Descripcion = models.CharField(max_length=500)
    Scan_Anexo = models.FileField(upload_to=None, max_length=100,
                                  blank=True, null=True)
    Scan_Pagare = models.FileField(upload_to=None, max_length=100,
                                   blank=True, null=True)
    Scan_Pagare_VR = models.FileField(upload_to=None, max_length=100,
                                      blank=True, null=True)
    Scan_Carta = models.FileField(upload_to=None, max_length=100,
                                  blank=True, null=True)

    class Meta:
        unique_together = ('Num_Anexo', 'Contrato',)

    def __unicode__(self):
        return ('Anexo #: ' + str(self.Num_Anexo) + 'a contrato #: '
                + str(self.Contrato.Num_Contrato) + ' de '
                + self.Cliente.Nombre_Empresa)


class Modificatorio(models.Model):
    A_Contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE,
                                   blank=True)
    Para_Anexo = models.ForeignKey(Anexo, on_delete=models.CASCADE,
                                   blank=True)
    Descripcion_Modificacion = models.CharField(max_length=700)
    Scan_Modificatorio = models.FileField(upload_to=None, max_length=100,
                                          blank=True, null=True)

    def __unicode__(self):
        return ('Modificatorio a anexo: #' + str(self.Para_Anexo.Num_Anexo) +
                ' Cliente: ' + self.Para_Anexo.Cliente.Nombre_Empresa)


class Poliza_Seguro(models.Model):
    abba = 'AB'
    maphre = 'MA'
    gnp = 'GN'
    hdi = 'HD'
    anna = 'AN'
    insurance_choices = (
        (abba, 'ABBA'),
        (maphre, 'MAPHRE'),
        (gnp, 'GNP'),
        (hdi, 'HDI'),
        (anna, 'ANNA'),
    )
    Aseguradora = models.CharField(max_length=2, choices=insurance_choices,
                                   default=abba)
    Num_Poliza = models.PositiveIntegerField()
    Poliza_Fecha_Inicio = models.DateField(blank=True)
    Poliza_Fecha_Final = models.DateField(blank=True)
    Scan_Poliza = models.FileField(upload_to=None, max_length=100,
                                   blank=True, null=True)
    Aceptada = models.BooleanField(default=False)

    def __unicode__(self):
        return ('Poliza: #' + str(self.Num_Poliza) + ' | '
                + self.get_Aseguradora_display())


class Placas(models.Model):
    cdmx = 'cx'
    edom = 'em'
    mrls = 'ms'
    qrto = 'qo'
    edo_emisor = (
        (cdmx, 'CDMX'),
        (edom, 'Edo. de Mexico'),
        (mrls, 'Morelos'),
        (qrto, 'Queretaro'),
    )
    Estado_emisor = models.CharField(max_length=2, choices=edo_emisor,
                                     default=cdmx)
    Clave_placas = models.Charfiel(max_length=10)
    Scan_placas = models.FileField(upload_to=None, max_length=100,
                                   blank=True, null=True)


class Factura(models.Model):
    VEHICULO_PARTICULAR = 'VP'
    VEHICULO_CARGA = 'VC'
    MAQUINARIA_AMARILLA = 'MA'
    EQUIPO_COMPUTO = 'EC'
    MOBILIARIO = 'MOB'
    MAQUINA = 'MQ'
    OTROS = 'OT'
    capital_choices = (
        (VEHICULO_PARTICULAR, 'auto particular'),
        (VEHICULO_CARGA, 'camion'),
        (MAQUINARIA_AMARILLA, 'maquinaria amarilla'),
        (EQUIPO_COMPUTO, 'equipo de computo'),
        (MOBILIARIO, 'mobiliario'),
        (MAQUINA, 'maquinas'),
        (OTROS, 'otros'),
    )
    # info factura
    Num_Factura = models.PositiveIntegerField()
    Monto_Factura = models.PositiveIntegerField()
    Agencia_que_Factura = models.ForeignKey(
                                        comercial_models.Agencia_Automotriz,
                                        blank=True, null=True)
    Vendedor_Agencia = models.ForeignKey(comercial_models.Contacto_Agencia,
                                         blank=True, null=True)
    Scan_Factura = models.FileField(upload_to=None, max_length=100,
                                    blank=True, null=True)
    # info Avance
    Caso = models.ForeignKey(comercial_models.Caso, blank=True)
    Cliente = models.ForeignKey(comercial_models.Cliente,
                                blank=True, related_name="arrendatario")
    Anexo = models.ForeignKey(Anexo, blank=True)
    Tipo_Activo = models.CharField(max_length=3, choices=capital_choices,
                                   default=VEHICULO_PARTICULAR)
    Eq_Solicitado = models.OneToOneField(comercial_models.Equipo_Solicitado)
    # Poliza Seguro
    Poliza = models.ForeignKey(Poliza_Seguro, blank=True, null=True)

    class Meta:
        unique_together = ('Num_Factura', 'Cliente', 'Anexo',)

    def __unicode__(self):
        return ('Factura: #' + str(self.Num_Factura) + ' | '
                + self.Concepto_Factura)


class Documentacion_PMoral(models.Model):
    ife = 'ie'
    pasaporte = 'pe'
    identificacion_choices = (
        (ife, 'IFE'),
        (pasaporte, 'PASAPORTE'),
    )
    cfe = 'ce'
    telmex = 'tx'
    total_play = 'ty'
    izzi = 'ii'
    comprobante_choices = (
        (cfe, 'CFE'),
        (telmex, 'TELMEX'),
        (total_play, 'TOTAL PLAY'),
        (izzi, 'IZZI'),
    )
    Caso = models.OneToOneField(comercial_models.Caso, blank=True)
    Fecha_Creacion = models.DateField(auto_now_add=True, blank=True)
    Ultima_Actualizacion = models.DateField(auto_now=True, blank=True)
    # Solicitud Arrendamiento
    Firma_Solicitud_Rep_legal = models.BooleanField(default=False)
    Firma_Solicitud_Aval = models.BooleanField(default=False)
    Anotacion_Solicitud = models.TextField(blank=True, null=True)
    # Edos Financieros
    Edo_Fin_Anual_1 = models.BooleanField(default=False)
    Edo_Fin_Anual_2 = models.BooleanField(default=False)
    Edo_Fin_Parciales = models.BooleanField(default=False)
    Anotacion_Edos_Fin = models.TextField(blank=True, null=True)
    # Declaraciones y Acuses
    Declaracion_Anual_1 = models.BooleanField(default=False)
    Declaracion_Anual_2 = models.BooleanField(default=False)
    Acuse_Declaracion_1 = models.BooleanField(default=False)
    Acuse_Declaracion_2 = models.BooleanField(default=False)
    Anotacion_Declaraciones_y_Acuses = models.TextField(blank=True, null=True)
    # acta constitutiva
    Acta_Constitutiva = models.BooleanField(default=False)
    Sello_Inscripcion_Acta_Constitutiva = models.BooleanField(default=False)
    Num_Notaria = models.PositiveIntegerField(blank=True, null=True)
    Notario = models.CharField(max_length=300, blank=True, null=True)
    Num_Acta_Constitutiva = models.PositiveIntegerField(blank=True, null=True)
    Fecha_Acta = models.DateField(blank=True, null=True)
    Inscrita_en_el_Estado = models.CharField(max_length=50,
                                             blank=True, null=True)
    Inscrita_en_el_Municipio = models.CharField(max_length=50,
                                                blank=True, null=True)
    Fecha_Inscripcion = models.DateField(blank=True, null=True)
    Datos_Registro = models.CharField(max_length=300, blank=True, null=True)
    Poderes = models.BooleanField(default=False)
    Sello_Inscripcion_Poderes = models.BooleanField(default=False)
    Anotacion_Acta_Constitutiva = models.TextField(blank=True, null=True)
    # RFC
    RFC = models.BooleanField(default=False)
    Anotacion_RFC = models.TextField(blank=True, null=True)
    # edos de cuenta bancarios
    Edo_cuenta_Rep_Legal_1 = models.BooleanField(default=False)
    Edo_cuenta_Rep_Legal_2 = models.BooleanField(default=False)
    Edo_cuenta_Rep_Legal_3 = models.BooleanField(default=False)
    Edo_cuenta_Aval_1 = models.BooleanField(default=False)
    Edo_cuenta_Aval_2 = models.BooleanField(default=False)
    Edo_cuenta_Aval_3 = models.BooleanField(default=False)
    Anotacion_Edos_Cuenta = models.TextField(blank=True, null=True)
    # identificaciones
    Identificacion_Rep_legal = models.BooleanField(default=False)
    Tipo_identificacion_Rep_legal = models.CharField(
                                                max_length=2,
                                                choices=identificacion_choices,
                                                default=ife,
                                                blank=True, null=True)
    Num_identificacion_Rep_legal = models.CharField(max_length=20,
                                                    blank=True, null=True)
    Vigente_hasta_identificacion_Rep_legal = models.DateField(
                                                    blank=True, null=True)
    Representante_legal_es_aval = models.BooleanField(default=True)
    Identificacion_Rep_Aval = models.BooleanField(default=False)
    Tipo_identificacion_Aval = models.CharField(max_length=2,
                                                choices=identificacion_choices,
                                                default=ife,
                                                blank=True, null=True)
    Num_identificacion_Aval = models.CharField(max_length=20,
                                               blank=True, null=True)
    Vigente_hasta_identificacion_Aval = models.DateField(blank=True, null=True)
    Anotacion_Identificaciones = models.TextField(blank=True, null=True)
    # comprobantes domicilio
    Comprobante_domicilio_Empresa = models.BooleanField(default=False)
    Fuente_comprobante_domicilio_Empresa = models.CharField(
                                            max_length=2,
                                            choices=comprobante_choices,
                                            default=cfe, blank=True, null=True)
    Domicilio_comprobante_domicilio_Empresa = models.CharField(
                                                        max_length=20,
                                                        blank=True, null=True)
    Fecha_comprobante_domicilio_Empresa = models.DateField(
                                                        blank=True, null=True)
    Comprobante_domicilio_Aval = models.BooleanField(default=False)
    Fuente_comprobante_domicilio_Aval = models.CharField(
                                        max_length=2,
                                        choices=comprobante_choices,
                                        default=cfe, blank=True, null=True)
    Domicilio_comprobante_domicilio_Aval = models.CharField(max_length=20,
                                                            blank=True,
                                                            null=True)
    Fecha_comprobante_domicilio_Aval = models.DateField(blank=True, null=True)
    Anotacion_Comprobantes_Domicilio = models.TextField(blank=True, null=True)
    # autorizaciones Buro
    Aut_Buro_Empresa = models.BooleanField(default=False)
    Aut_Buro_Rep_legal = models.BooleanField(default=False)
    Aut_Buro_Aval = models.BooleanField(default=False)
    Anotacion_Autorizaciones_Buro = models.TextField(blank=True, null=True)
    # Nota
    Nota_General = models.TextField(max_length=800, blank=True, null=True)
    Necesario_para_Evaluacion = models.BooleanField(default=False)


class Documentacion_PFisica(models.Model):
    ife = 'ie'
    pasaporte = 'pe'
    identificacion_choices = (
        (ife, 'IFE'),
        (pasaporte, 'PASAPORTE'),
    )
    cfe = 'ce'
    telmex = 'tx'
    total_play = 'ty'
    izzi = 'ii'
    comprobante_choices = (
        (cfe, 'CFE'),
        (telmex, 'TELMEX'),
        (total_play, 'TOTAL PLAY'),
        (izzi, 'IZZI'),
    )
    Caso = models.OneToOneField(comercial_models.Caso, blank=True)
    Fecha_Creacion = models.DateField(auto_now_add=True, blank=True)
    Ultima_Actualizacion = models.DateField(auto_now=True, blank=True)
    # Solicitud Arrendamiento
    Firma_Solicitud_Persona_Fisica = models.BooleanField(default=False)
    Firma_Solicitud_Aval = models.BooleanField(default=False)
    Anotacion_Solicitud = models.TextField(blank=True, null=True)
    # Declaraciones y Acuses
    Declaracion_Anual = models.BooleanField(default=False)
    Acuse_Declaracion = models.BooleanField(default=False)
    # RFC
    RFC = models.BooleanField(default=False)
    # edos de cuenta bancarios
    Edo_cuenta_P_Fisica_1 = models.BooleanField(default=False)
    Edo_cuenta_P_Fisica_2 = models.BooleanField(default=False)
    Edo_cuenta_P_Fisica_3 = models.BooleanField(default=False)
    Edo_cuenta_Aval_1 = models.BooleanField(default=False)
    Edo_cuenta_Aval_2 = models.BooleanField(default=False)
    Edo_cuenta_Aval_3 = models.BooleanField(default=False)
    Anotacion_Edos_Cuenta = models.TextField(blank=True, null=True)
    # identificaciones
    Identificacion_P_Fisica = models.BooleanField(default=False)
    Tipo_identificacion_P_Fisica = models.CharField(
                                                max_length=2,
                                                choices=identificacion_choices,
                                                default=ife,
                                                blank=True, null=True)
    Num_identificacion_P_Fisica = models.CharField(max_length=20,
                                                   blank=True, null=True)
    Vigente_hasta_identificacion_P_Fisica = models.DateField(
                                                    blank=True, null=True)
    P_Fisica_es_aval = models.BooleanField(default=True)
    Identificacion_Aval = models.BooleanField(default=False)
    Tipo_identificacion_Aval = models.CharField(max_length=2,
                                                choices=identificacion_choices,
                                                default=ife,
                                                blank=True, null=True)
    Num_identificacion_Aval = models.CharField(max_length=20,
                                               blank=True, null=True)
    Vigente_hasta_identificacion_Aval = models.DateField(blank=True, null=True)
    Anotacion_Identificaciones = models.TextField(blank=True, null=True)
    # comprobantes domicilio
    Comprobante_P_Fisica = models.BooleanField(default=False)
    Fuente_comprobante_domicilio_P_Fisica = models.CharField(
                                            max_length=2,
                                            choices=comprobante_choices,
                                            default=cfe, blank=True, null=True)
    Domicilio_comprobante_P_Fisica = models.CharField(max_length=20,
                                                      blank=True, null=True)
    Fecha_comprobante_domicilio_P_Fisica = models.DateField(
                                                        blank=True, null=True)
    Comprobante_domicilio_Aval = models.BooleanField(default=False)
    Fuente_comprobante_domicilio_Aval = models.CharField(
                                        max_length=2,
                                        choices=comprobante_choices,
                                        default=cfe, blank=True, null=True)
    Domicilio_comprobante_domicilio_Aval = models.CharField(max_length=20,
                                                            blank=True,
                                                            null=True)
    Fecha_comprobante_domicilio_Aval = models.DateField(blank=True, null=True)
    Anotacion_Comprobantes_Domicilio = models.TextField(blank=True, null=True)
    # autorizaciones Buro
    Aut_Buro_P_Fisica = models.BooleanField(default=False)
    Aut_Buro_Aval = models.BooleanField(default=False)
    Anotacion_Autorizaciones_Buro = models.TextField(blank=True, null=True)
    # Nota
    Nota_General = models.TextField(max_length=800, blank=True, null=True)
    Necesario_para_Evaluacion = models.BooleanField(default=False)
