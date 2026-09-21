from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Propietario, Mascota, ConsultaVeterinaria
from .serializers import MascotaSerializer, ConsultaVeterinariaSerializer


class ClinicaTests(APITestCase):
    def setUp(self):
        self.propietario = Propietario.objects.create(
            identificacion='1-1111-1111',
            nombre='Juan Perez',
            telefono='8888-1111',
            email='juan@example.com'
        )
        self.mascota = Mascota.objects.create(
            nombre='Luna',
            especie='Perro',
            raza='Labrador',
            peso=Decimal('12.50'),
            propietario=self.propietario
        )

    def test_serializer_mascota_peso_cero_invalido(self):
        datos = {
            'nombre': 'Luna',
            'especie': 'Perro',
            'raza': 'Labrador',
            'peso': 0,
            'activo': True,
            'propietario': self.propietario.id,
        }
        serializer = MascotaSerializer(data=datos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('peso', serializer.errors)

    def test_serializer_consulta_costo_negativo_invalido(self):
        datos = {
            'mascota': self.mascota.id,
            'motivo': 'Control',
            'diagnostico': 'Revision general',
            'tratamiento': 'Ninguno',
            'costo': -10,
        }
        serializer = ConsultaVeterinariaSerializer(data=datos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('costo', serializer.errors)

    def test_perfil_usuario_anonimo_rechazado(self):
        respuesta = self.client.get('/clinica/api/perfil/')
        self.assertEqual(respuesta.status_code, 401)

    def test_perfil_usuario_autenticado_obtiene_200(self):
        usuario = User.objects.create_user(
            username='usuario_prueba',
            password='clave12345',
            email='usuario@example.com'
        )
        token = Token.objects.create(user=usuario)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        respuesta = self.client.get('/clinica/api/perfil/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data['username'], 'usuario_prueba')
