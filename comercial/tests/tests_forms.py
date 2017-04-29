from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group

from comercial.models import Cliente
from comercial.forms import (ClienteForm, Cliente_VForm, Contacto_CForm, Contacto_CCForm, Contacto_CCAForm,
                            Caso_VForm, Caso_CVForm, Caso_IniForm, Caso_StatusForm,
                            Agencia_AutomotrizForm, Agencia_AutomotrizVForm, Contacto_AgenciaForm,
                            Contacto_AgenciaVForm, Contacto_Agencia_IniForm, Direccion_Fiscal_ClienteForm,
                            Contacto_Agencia_AForm, Direccion_Fiscal_ClienteCForm, InteraccionForm,
                            AnotacionForm)

class Cliente_FormTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='Claudio_V', first_name='Claudio', last_name='Velazquez',
                                    email='claudio@avance.mg', password="shjshjsh")

    def test_Cliente_VForm(self):
        form_data = {'RFC': 'something', 'Persona_Moral': True, 'Nombre_Empresa': 'Arroz con Leche',
                    'Tipo_Negocio': 'FA', 'Industria': 'Textil'}
        form = Cliente_VForm(data=form_data)
        self.assertTrue(form.is_valid())
