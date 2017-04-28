from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group

from comercial.models import (Cliente, Contacto_C, Direccion_Fiscal_Cliente, Agencia_Automotriz, Contacto_Agencia, Caso,
                            Interaccion, Anotacion, Historial_Etapa)
# Create your tests here.
class AgenciaTestCase(TestCase):
    def setUp(self):
        comercial_v = Group.objects.create(name='comercial_vendedor')
        Claudio_V = User.objects.create_user(username='Claudio_V', first_name='Claudio', last_name='Velazquez',
                                        email='claudio@avance.mg', password="shjshjsh")
        Claudio_V.groups.add(comercial_v)
        Fernanda_R = User.objects.create_user(username='Fernanda_R', first_name='Fernanda', last_name='Rivera',
                                        email='fernanda@avance.mg', password="bsghak")
        Fernanda_R.groups.add(comercial_v)

        Agencia_Automotriz.objects.create(Marca='MZ', Grupo='al', Ciudad="CDMX", Colonia="Tacubaya",
                                        Telefono="55438789", Atiende=Claudio_V)
        Agencia_Automotriz.objects.create(Marca='KI', Grupo='al', Ciudad="Queretaro", Colonia="San Juan",
                                        Telefono="431 438 7789", Atiende=Fernanda_R)


    def test_lista_agencias(self):
        self.client.login(username='Claudio_V', password='shjshjsh')
        response = self.client.get('/comercial/lista_agencias/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comercial/lista_agencias.html')
        self.assertContains(response, 'Tacubaya')
        self.assertContains(response, 'Queretaro')

    def test_detalle_agencia(self):
        self.client.login(username='Claudio_V', password='shjshjsh')
        response = self.client.get(reverse('detalle_agencia', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comercial/detalle_agencia.html')
        self.assertContains(response, 'Tacubaya')

class ClienteTestCase(TestCase):
    def setUp(self):
        comercial_v = Group.objects.create(name='comercial_vendedor')
        Claudio_V = User.objects.create_user(username='Claudio_V', first_name='Claudio', last_name='Velazquez',
                                        email='claudio@avance.mg', password="shjshjsh")
        Claudio_V.groups.add(comercial_v)
        Fernanda_R = User.objects.create_user(username='Fernanda_R', first_name='Fernanda', last_name='Rivera',
                                        email='fernanda@avance.mg', password="bsghak")
        Fernanda_R.groups.add(comercial_v)

        Cliente.objects.create(RFC='ACL9807HJMF6T', Persona_Moral=True, Nombre_Empresa='Arroz con Leche',
                                Tipo_Negocio='FA', Industria='Textil', Atiende=Claudio_V, Status='PR')

    #vendedor puede revisar los detalles de su cliente
    def test_detalle_cliente(self):
        self.client.login(username='Claudio_V', password='shjshjsh')
        response = self.client.get(reverse('detalle_cliente', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comercial/detalle_cliente.html')
        self.assertContains(response, 'Arroz con Leche')

    #vendedor no puede revisar los detalles del cliente de otro vendedor
    def test_vista_denegada(self):
        self.client.login(username='Fernanda_R', password='bsghak')
        response = self.client.get(reverse('detalle_cliente', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

class Lista_ClienteTestCase(TestCase):
    def setUp(self):
        Claudio_V = User.objects.create_user(username='Claudio_V', first_name='Claudio', last_name='Velazquez',
                                        email='claudio@avance.mg', password="shjshjsh")
        Fernanda_R = User.objects.create_user(username='Fernanda_R', first_name='Fernanda', last_name='Rivera',
                                        email='fernanda@avance.mg', password="bsghak")

        Cliente.objects.create(RFC='ACL9807HJMF6T', Persona_Moral=True, Nombre_Empresa='Arroz con Leche',
                                Tipo_Negocio='FA', Industria='Textil', Atiende=Claudio_V, Status='PR')
        Cliente.objects.create(RFC='CAK9807HJMF6T', Persona_Moral=True, Nombre_Empresa='Carolina K',
                                Tipo_Negocio='FA', Industria='Textil', Atiende=Claudio_V, Status='CA')
        Cliente.objects.create(RFC='GRO8807HJMF6T', Persona_Moral=True, Nombre_Empresa='Guss Roch',
                                Tipo_Negocio='FA', Industria='Metalmecanica', Atiende=Fernanda_R, Status='CA')

    def test_lista_clientes(self):
        self.client.login(username='Claudio_V', password='shjshjsh')
        response = self.client.get(reverse('lista_clientes', kwargs={'vendedor_pk': 1, 'status': 'AL', 'tipo': 'L'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comercial/lista_clientes.html')
        self.assertContains(response, 'Arroz con Leche')
        self.assertContains(response, 'Carolina K')
        self.assertNotContains(response, 'Guss Roch')