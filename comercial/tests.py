from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from comercial.models import (Cliente, Contacto_C, Direccion_Fiscal_Cliente, Agencia_Automotriz, Contacto_Agencia, Caso,
                            Interaccion, Anotacion, Historial_Etapa)
# Create your tests here.
class AgenciaTestCase(TestCase):
    def setUp(self):
        Claudio_V = User.objects.create_user(username='Claudio_V', first_name='Claudio', last_name='Velazquez',
                                        email='claudio@avance.mg', password="shjshjsh")
        Fernanda_R = User.objects.create_user(username='Fernanda_R', first_name='Fernanda', last_name='Rivera',
                                        email='fernanda@avance.mg', password="bsghak")

        Agencia_Automotriz.objects.create(Marca='MZ', Grupo='al', Ciudad="CDMX", Colonia="Tacubaya",
                                        Telefono="55438789", Atiende=Claudio_V)
        Agencia_Automotriz.objects.create(Marca='KI', Grupo='al', Ciudad="Queretaro", Colonia="San Juan",
                                        Telefono="431 438 7789", Atiende=Fernanda_R)

        Cliente.objects.create(RFC='ACL9807HJMF6T', Persona_Moral=True, Nombre_Empresa='Arroz con Leche',
                                Tipo_Negocio='FA', Industria='Textil', Atiende=Claudio_V, Status='PR')

    def test_lista_agencias(self):
        self.client.login(username='Claudio_V', password='shjshjsh')
        response = self.client.get('/comercial/lista_agencias/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comercial/lista_agencias.html')
        self.assertContains(response, 'Tacubaya')
        self.assertContains(response, 'Queretaro')

    def test_detalle_agencia(self):
        self.client.login(username='Claudio_V', password='shjshjsh')
        url = reverse('detalle_agencia', kwargs={'pk': mazda.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
