# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm

from comercial.models import (Cliente, Contacto_C, Agencia_Automotriz,
                              Contacto_Agencia, Caso, Equipo_Solicitado,
                              Direccion_Fiscal_Cliente, Interaccion,
                              Anotacion, Cita)


def has_group(user, group_name):
    """
    Verifica que este usuario pertence a un grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

# ------------------------------- Forms ------------------------------


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('RFC', 'Persona_Moral', 'Nombre_Empresa', 'Tipo_Negocio',
                  'Industria', 'Atiende')


class Cliente_VForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ('RFC', 'Persona_Moral', 'Nombre_Empresa', 'Tipo_Negocio',
                  'Industria')


class Contacto_CForm(ModelForm):
    class Meta:
        model = Contacto_C
        fields = '__all__'


class Contacto_CCForm(ModelForm):
    class Meta:
        model = Contacto_C
        exclude = ['Atiende']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(Contacto_CCForm, self).__init__(*args, **kwargs)
        if has_group(user, 'comercial_vendedor'):
            self.fields['Cliente'].queryset = Cliente.objects.filter(
                                                                Atiende=user)


class Contacto_CCAForm(ModelForm):
    class Meta:
        model = Contacto_C
        exclude = ['Cliente', 'Atiende']


class Direccion_Fiscal_ClienteForm(ModelForm):
    class Meta:
        model = Direccion_Fiscal_Cliente
        fields = '__all__'


class Direccion_Fiscal_ClienteCForm(ModelForm):
    class Meta:
        model = Direccion_Fiscal_Cliente
        exclude = ['Cliente']


class Agencia_AutomotrizForm(ModelForm):
    class Meta:
        model = Agencia_Automotriz
        fields = '__all__'


class Agencia_AutomotrizVForm(ModelForm):
    class Meta:
        model = Agencia_Automotriz
        exclude = ['Atiende']


class Contacto_AgenciaForm(ModelForm):
    class Meta:
        model = Contacto_Agencia
        fields = '__all__'


class Contacto_AgenciaVForm(ModelForm):
    class Meta:
        model = Contacto_Agencia
        exclude = ['Atiende']


class Contacto_Agencia_IniForm(ModelForm):
    class Meta:
        model = Contacto_Agencia
        exclude = ['Agencia', 'Atiende']


class Caso_VForm(ModelForm):
    class Meta:
        model = Caso
        exclude = ['Atiende', 'Requiere_revision_admon', 'Activo',
                   'Monto', 'Requiere_revision_vtas']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(Caso_VForm, self).__init__(*args, **kwargs)
        self.fields['Cliente'].queryset = Cliente.objects.filter(
                                    Atiende=user).order_by('Nombre_Empresa')
        self.fields['Contacto'].queryset = Contacto_C.objects.filter(
                                                                Atiende=user)
        self.fields['Agencia'].queryset = Agencia_Automotriz.objects.filter(
                                            Atiende=user).order_by('Marca')
        self.fields['Vendedor_Agencia'].queryset = (
                                        Contacto_Agencia.objects.filter(
                                                    Atiende=user).order_by(
                                                    'Nombre_del_Contacto'))
        INTERES = 'int'
        COTIZACION = 'cot'
        ESPERANDO_PAPELES = 'epa'
        ESPERANDO_APROBACION = 'eap'
        APROBADO = 'apr'
        CONTRATO_FIRMADO = 'cfr'
        PAGO_INICIAL_RECIBIDO = 'pir'
        FONDEADO = 'fon'
        CERRADO = 'crd'
        PERDIDO = 'prd'
        RECHAZADO = 'rzo'
        if has_group(user, 'comercial_vendedor'):
            self.fields['Etapa'].choices = [(INTERES, 'Interes'),
                                            (COTIZACION, 'Cotizacion Enviada'),
                                            (ESPERANDO_PAPELES,
                                            'Esperando Papeles'),
                                            (CONTRATO_FIRMADO,
                                            'Contrato Firmado'),
                                            (CERRADO, 'Cerrado'),
                                            (PERDIDO, 'Perdido'), ]
        elif has_group(user, 'comercial_backup'):
            self.fields['Etapa'].choices = [(ESPERANDO_PAPELES,
                                            'Esperando Papeles'),
                                            (ESPERANDO_APROBACION,
                                            'Esperando Aprobacion'),
                                            (APROBADO, 'Aprobado'),
                                            (PAGO_INICIAL_RECIBIDO,
                                            'Pago Inicial Recibido'),
                                            (FONDEADO, 'Fondeado'),
                                            (CERRADO, 'Cerrado'),
                                            (RECHAZADO, 'Rechazado'), ]


class Caso_CVForm(ModelForm):
    class Meta:
        model = Caso
        exclude = ['Cliente', 'Atiende', 'Requiere_revision_admon', 'Activo',
                   'Monto', 'Requiere_revision_vtas']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        cliente = kwargs.pop("cliente")
        super(Caso_CVForm, self).__init__(*args, **kwargs)
        self.fields['Contacto'].queryset = Contacto_C.objects.filter(
                                                            Cliente=cliente)
        self.fields['Agencia'].queryset = Agencia_Automotriz.objects.filter(
                                                Atiende=user).order_by('Marca')
        self.fields['Vendedor_Agencia'].queryset = (
                                            Contacto_Agencia.objects.filter(
                                                Atiende=user).order_by(
                                                'Nombre_del_Contacto'))
        INTERES = 'int'
        COTIZACION = 'cot'
        ESPERANDO_PAPELES = 'epa'
        ESPERANDO_APROBACION = 'eap'
        APROBADO = 'apr'
        CONTRATO_FIRMADO = 'cfr'
        PAGO_INICIAL_RECIBIDO = 'pir'
        FONDEADO = 'fon'
        CERRADO = 'crd'
        PERDIDO = 'prd'
        RECHAZADO = 'rzo'
        if has_group(user, 'comercial_vendedor'):
            self.fields['Etapa'].choices = [(INTERES, 'Interes'),
                                            (COTIZACION, 'Cotizacion Enviada'),
                                            (ESPERANDO_PAPELES,
                                            'Esperando Papeles'),
                                            (CONTRATO_FIRMADO,
                                            'Contrato Firmado'),
                                            (CERRADO, 'Cerrado'),
                                            (PERDIDO, 'Perdido'), ]
        elif has_group(user, 'comercial_backup'):
            self.fields['Etapa'].choices = [(ESPERANDO_PAPELES,
                                            'Esperando Papeles'),
                                            (ESPERANDO_APROBACION,
                                            'Esperando Aprobacion'),
                                            (APROBADO, 'Aprobado'),
                                            (PAGO_INICIAL_RECIBIDO,
                                            'Pago Inicial Recibido'),
                                            (FONDEADO, 'Fondeado'),
                                            (CERRADO, 'Cerrado'),
                                            (RECHAZADO, 'Rechazado'), ]


class Caso_IniForm(ModelForm):
    class Meta:
        model = Caso
        exclude = ['Cliente', 'Atiende', 'Contacto', 'Requiere_revision_admon',
                   'Activo', 'Monto', 'Requiere_revision_vtas']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(Caso_IniForm, self).__init__(*args, **kwargs)
        if has_group(user, 'comercial_vendedor'):
            self.fields['Agencia'].queryset = (
                                        Agencia_Automotriz.objects.filter(
                                            Atiende=user).order_by('Marca'))
            self.fields['Vendedor_Agencia'].queryset = (
                                            Contacto_Agencia.objects.filter(
                                                Atiende=user).order_by(
                                                'Nombre_del_Contacto'))
        INTERES = 'int'
        COTIZACION = 'cot'
        ESPERANDO_PAPELES = 'epa'
        self.fields['Etapa'].choices = [(INTERES, 'Interes'),
                                        (COTIZACION, 'Cotizacion Enviada'),
                                        (ESPERANDO_PAPELES,
                                        'Esperando Papeles'), ]


class Caso_StatusForm(ModelForm):
    class Meta:
        model = Caso
        fields = ('Etapa',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(Caso_StatusForm, self).__init__(*args, **kwargs)

        INTERES = 'int'
        COTIZACION = 'cot'
        ESPERANDO_PAPELES = 'epa'
        ESPERANDO_APROBACION = 'eap'
        APROBADO = 'apr'
        CONTRATO_FIRMADO = 'cfr'
        PAGO_INICIAL_RECIBIDO = 'pir'
        FONDEADO = 'fon'
        CERRADO = 'crd'
        PERDIDO = 'prd'
        RECHAZADO = 'rzo'
        if has_group(user, 'comercial_vendedor'):
            self.fields['Etapa'].choices = [(INTERES, 'Interes'),
                                            (COTIZACION, 'Cotizacion Enviada'),
                                            (ESPERANDO_PAPELES,
                                            'Esperando Papeles'),
                                            (CONTRATO_FIRMADO,
                                            'Contrato Firmado'),
                                            (CERRADO, 'Cerrado'),
                                            (PERDIDO, 'Perdido'), ]
        elif has_group(user, 'comercial_backup'):
            self.fields['Etapa'].choices = [(ESPERANDO_PAPELES,
                                            'Esperando Papeles'),
                                            (ESPERANDO_APROBACION,
                                            'Esperando Aprobacion'),
                                            (APROBADO, 'Aprobado'),
                                            (PAGO_INICIAL_RECIBIDO,
                                            'Pago Inicial Recibido'),
                                            (FONDEADO, 'Fondeado'),
                                            (CERRADO, 'Cerrado'),
                                            (RECHAZADO, 'Rechazado'), ]


class Equipo_SolicitadoForm(ModelForm):
    class Meta:
        model = Equipo_Solicitado
        exclude = ['Caso']


class InteraccionForm(ModelForm):
    class Meta:
        model = Interaccion
        exclude = ['Hecha_por', 'del_Caso', 'Numero', 'Hist_Etapa',
                   'Requiere_revision_admon', 'Requiere_revision_vtas']


class AnotacionForm(ModelForm):
    class Meta:
        model = Anotacion
        exclude = ['al_Caso', 'Hecha_por', 'Hist_Etapa']


class CitaClienteForm(ModelForm):
    class Meta:
        model = Cita
        exclude = ['Agencia', 'Atiende']
        widgets = {
            'Hora': forms.TimeInput(format='%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(CitaClienteForm, self).__init__(*args, **kwargs)
        self.fields['Cliente'].queryset = Cliente.objects.filter(
                                    Atiende=user).order_by('Nombre_Empresa')


class CitaAgenciaForm(forms.Form):
    dias = (
            ("0", "lunes"),
            ("1", "martes"),
            ("2", "miercoles"),
            ("3", "jueves"),
            ("4", "viernes"),
            ("5", "sabado"),
            )
    Agencia = forms.ModelChoiceField(
                                queryset=Agencia_Automotriz.objects.none())
    Hora = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    Todos_los = forms.MultipleChoiceField(
                            widget=forms.CheckboxSelectMultiple, choices=dias)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(CitaAgenciaForm, self).__init__(*args, **kwargs)
        self.fields['Agencia'].queryset = Agencia_Automotriz.objects.filter(
                                                Atiende=user).order_by('Marca')


class ComparativaForm(forms.Form):
    plazos = (
             (24, "24"),
             (36, "36"),
             (48, "48"),
    )
    Monto = forms.IntegerField(initial=400000)
    Plazo = forms.ChoiceField(choices=plazos)
    Aportacion_Adicional = forms.IntegerField(required=False)
    Vehiculo_de_Trabajo = forms.BooleanField(required=False, initial=False)
    Contra = forms.CharField(required=False)
    Pago_Inicial = forms.IntegerField()
    Numero_Rentas_Incluidas_en_Pago_Inicial = forms.IntegerField(initial=1)
    Renta = forms.IntegerField()
    Deduccion_Mensual = forms.IntegerField()
    Valor_Residual = forms.IntegerField()


class OC_Form(forms.Form):
    Cantidad = forms.IntegerField(initial=1)
    Modelo = forms.CharField()
    Color = forms.CharField()
    Color_Interno = forms.CharField()
    Transmision = forms.CharField()
    Precio_Unitario = forms.IntegerField()
