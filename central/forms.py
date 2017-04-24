from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

# Crispy Forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import TabHolder, Tab

from central.models import (Contrato, Anexo, Modificatorio, Factura, Documentacion_PMoral)

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class Contrato_Form(ModelForm):
    class Meta:
        model = Contrato
        fields = ('Cliente', 'Nombre_Rep_Legal', 'Nombre_Aval', 'Fecha', 'Scan_Contrato')

class Anexo_Form(ModelForm):
    class Meta:
        model = Anexo
        exclude = ['Num_Anexo']

class Documentacion_PMoral_Form(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        TabHolder(
            Tab('Empresa',
                'Acta_Constitutiva',
                'RFC',
                'Sello_Inscripcion_Acta_Constitutiva',
                'Num_Notaria',
                'Num_Acta_Constitutiva',
                'Poderes',
                'Sello_Inscripcion_Poderes',
                'Declaracion_Anual_1',
                'Declaracion_Anual_2',
                'Acuse_Declaracion_1',
                'Acuse_Declaracion_2',
                'Edo_Fin_Anual_1',
                'Edo_Fin_Anual_2',
                'Edo_Fin_Parciales',
                'Aut_Buro_Empresa',
                'Comprobante_domicilio_Empresa',
                'Fuente_comprobante_domicilio_Empresa',
                'Domicilio_comprobante_domicilio_Empresa',
                'Fecha_comprobante_domicilio_Empresa'
            ),
            Tab('Representante Legal',
                'Identificacion_Rep_legal',
                'Tipo_identificacion_Rep_legal',
                'Num_identificacion_Rep_legal',
                'Vigente_hasta_identificacion_Rep_legal',
                'Representante_legal_es_aval',
                'Aut_Buro_Rep_legal',
                'Firma_Solicitud_Rep_legal'
            ),
            Tab('Aval',
                'Identificacion_Rep_Aval',
                'Tipo_identificacion_Aval',
                'Num_identificacion_Aval',
                'Vigente_hasta_identificacion_Aval',
                'Aut_Buro_Aval',
                'Comprobante_domicilio_Aval',
                'Fuente_comprobante_domicilio_Aval',
                'Domicilio_comprobante_domicilio_Aval',
                'Fecha_comprobante_domicilio_Aval',
                'Firma_Solicitud_Aval'
            ),
            Tab('Extras',
                'Nota',
                'Necesario_para_Evaluacion'
            )
        )
    )

    class Meta:
        model = Documentacion_PMoral
        exclude = ['Caso', 'Fecha', 'Ultima_Actualizacion',]
