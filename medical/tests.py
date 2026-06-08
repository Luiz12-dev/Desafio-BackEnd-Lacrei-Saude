import uuid
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from .models import Profissional, Consulta


class ProfissionalAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testador', password='senha_teste_123'
        )
        self.client.force_authenticate(user=self.user)

        self.prof_url = '/api/profissionais/'

        self.profissional_data = {
            "nome_social": "Ana Souza",
            "profissao": "Psicóloga",
            "endereco": "Rua das Flores, 123",
            "contato": "11999999999",
        }

    def test_criar_profissional_com_sucesso(self):
        response = self.client.post(self.prof_url, self.profissional_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profissional.objects.count(), 1)
        self.assertEqual(
            Profissional.objects.get().nome_social, "Ana Souza"
        )

    def test_listar_profissionais(self):
        self.client.post(self.prof_url, self.profissional_data)

        response = self.client.get(self.prof_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_atualizar_profissional(self):
        prof = self.client.post(self.prof_url, self.profissional_data)
        prof_id = prof.data['id']
        url = f'{self.prof_url}{prof_id}/'

        novos_dados = {'nome_social': 'Nome Atualizado Pelo Teste'}
        response = self.client.patch(url, novos_dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['nome_social'], 'Nome Atualizado Pelo Teste'
        )

    def test_deletar_profissional(self):
        prof = self.client.post(self.prof_url, self.profissional_data)
        prof_id = prof.data['id']
        url = f'{self.prof_url}{prof_id}/'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profissional.objects.count(), 0)

    def test_erro_criar_profissional_sem_nome(self):
        dados_invalidos = self.profissional_data.copy()
        dados_invalidos['nome_social'] = "  "

        response = self.client.post(self.prof_url, dados_invalidos)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_erro_criar_profissional_campos_vazios(self):
        response = self.client.post(self.prof_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_erro_sanitizacao_xss(self):
        dados_xss = self.profissional_data.copy()
        dados_xss['nome_social'] = '<script>alert("xss")</script>'

        response = self.client.post(self.prof_url, dados_xss)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_erro_acesso_sem_token(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.prof_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ConsultaAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testador', password='senha_teste_123'
        )
        self.client.force_authenticate(user=self.user)

        self.prof_url = '/api/profissionais/'
        self.cons_url = '/api/consultas/'

        self.profissional_data = {
            "nome_social": "Ana Souza",
            "profissao": "Psicóloga",
            "endereco": "Rua das Flores, 123",
            "contato": "11999999999",
        }

    def _criar_profissional(self):
        response = self.client.post(self.prof_url, self.profissional_data)
        return response.data['id']

    def _data_futura(self, dias=2):
        return (timezone.now() + timedelta(days=dias)).isoformat()

    def test_criar_consulta_com_sucesso(self):
        prof_id = self._criar_profissional()

        consulta_data = {
            "data": self._data_futura(),
            "profissional": prof_id,
        }

        response = self.client.post(self.cons_url, consulta_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_listar_consultas(self):
        prof_id = self._criar_profissional()
        self.client.post(self.cons_url, {
            "data": self._data_futura(),
            "profissional": prof_id,
        })

        response = self.client.get(self.cons_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_atualizar_consulta(self):
        prof_id = self._criar_profissional()
        consulta = self.client.post(self.cons_url, {
            "data": self._data_futura(2),
            "profissional": prof_id,
        })

        consulta_id = consulta.data['id']
        url = f'{self.cons_url}{consulta_id}/'
        nova_data = self._data_futura(5)

        response = self.client.patch(url, {'data': nova_data})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deletar_consulta(self):
        prof_id = self._criar_profissional()
        consulta = self.client.post(self.cons_url, {
            "data": self._data_futura(),
            "profissional": prof_id,
        })

        consulta_id = consulta.data['id']
        url = f'{self.cons_url}{consulta_id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Consulta.objects.count(), 0)

    def test_buscar_consultas_por_profissional(self):
        prof_id = self._criar_profissional()
        self.client.post(self.cons_url, {
            "data": self._data_futura(2),
            "profissional": prof_id,
        })
        self.client.post(self.cons_url, {
            "data": self._data_futura(5),
            "profissional": prof_id,
        })

        url = f'{self.prof_url}{prof_id}/consultas/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_erro_criar_consulta_no_passado(self):
        prof_id = self._criar_profissional()
        data_passada = (timezone.now() - timedelta(days=2)).isoformat()

        response = self.client.post(self.cons_url, {
            "data": data_passada,
            "profissional": prof_id,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_erro_criar_consulta_profissional_inexistente(self):
        fake_id = str(uuid.uuid4())

        response = self.client.post(self.cons_url, {
            "data": self._data_futura(),
            "profissional": fake_id,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_erro_acesso_consultas_sem_token(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.cons_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)