from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Profissional, Consulta

class MedicalAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testador', password='123')
        self.client.force_authenticate(user = self.user)

        self.prof_url = '/api/profissionais/'
        self.cons_url = '/api/consultas/'

        self.profissional_data = {
            "nome_social": "Ana Souza",
            "profissao": "Psicóloga",
            "endereco": "Rua das Flores,123",
            "contato": "119999999",
        }


    def test_criar_profissional_com_sucesso(self):
        response = self.client.post(self.prof_url, self.profissional_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(),1)
        self.assertEqual(Profissional.objects.get().nome_social, "Ana Souza")
    
    def test_criar_consulta_com_sucesso(self):
        prof_response = self.client.post(self.prof_url, self.profissional_data)

        prof_id = prof_response.data['id']

        data_future = timezone.now() + timedelta(days=2)

        consulta_data = {
            "data": data_future.isoformat(),
            "profissional": prof_id
        }

        response = self.client.post(self.cons_url, consulta_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_erro_criar_profissional_sem_nome(self):
        dados_invalidos = self.profissional_data.copy()
        dados_invalidos['nome_social'] = "  "

        response = self.client.post(self.prof_url, dados_invalidos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_erro_criar_consulta_no_passado(self):
        prof_response = self.client.post(self.prof_url, self.profissional_data)

        prof_id = prof_response.data['id']

        data_past = timezone.now() - timedelta(days=2)

        consult_data = {
            "data": data_past.isoformat(),
            "profissional": prof_id
        }

        response = self.client.post(self.cons_url, consult_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_erro_acesso_sem_token(self):
        self.client.force_authenticate(user=None)
        
        response = self.client.get(self.prof_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
