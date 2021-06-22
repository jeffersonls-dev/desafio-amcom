from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Produto, Vendedor, Cliente, Venda, ItemVenda


class ProdutoTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "teste@gmail.com", "123456")
        self.client.login(username="tester", password="123456")
        self.client.force_authenticate(user=self.user)

    def test_inclusao_produto(self):
        url = reverse('produtos-list')
        data = {'nome': 'Smartphone',
                'preco': 350.20,
                'comissao': 5.30}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(Produto.objects.get().nome, 'Smartphone')


class VendedorTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "teste@gmail.com", "123456")
        self.client.login(username="tester", password="123456")
        self.client.force_authenticate(user=self.user)

    def test_inclusao_vendedor(self):
        url = reverse('vendedores-list')
        data = {'nome': 'jonas'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendedor.objects.count(), 1)
        self.assertEqual(Vendedor.objects.get().nome, 'jonas')


class ClienteTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "teste@gmail.com", "123456")
        self.client.login(username="tester", password="123456")
        self.client.force_authenticate(user=self.user)

    def test_inclusao_cliente(self):
        url = reverse('clientes-list')
        data = {'nome': 'felipe'}
        breakpoint()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 1)
        self.assertEqual(Cliente.objects.get().nome, 'felipe')


class VendasTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser("tester", "teste@gmail.com", "123456")
        self.client.login(username="tester", password="123456")
        self.client.force_authenticate(user=self.user)
        self.vendedor = Vendedor.objects.create(id=1, nome="lucas")
        self.produto = Produto.objects.create(id=1, nome="smartphone", preco=3510.20, comissao=7.50)
        self.produto = Produto.objects.create(id=2, nome="capa smartphone", preco=50.00, comissao=5.00)
        self.produto = Produto.objects.create(id=3, nome="fone de ouvido", preco=150.00, comissao=3.50)

    def test_inclusao_venda_um_produto(self):
        url = reverse('itemvenda-list')
        data = {
            "vendedor": 1,
            "cliente": 'fernando',
            "produto": 1,
            "quantidade": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(Venda.objects.get().pk, 1)
        self.assertEqual(ItemVenda.objects.count(), 1)
        self.assertEqual(ItemVenda.objects.get().produto.nome, "smartphone")

    def test_inclusao_venda_muitos_produto(self):
        url = reverse('itemvenda-list')
        data = [
            {
                "vendedor": 1,
                "cliente": "fernando",
                "produto": 1,
                "quantidade": 5
            },
            {
                "vendedor": 1,
                "cliente": "fernando",
                "produto": 2,
                "quantidade": 3
            },
            {
                "vendedor": 1,
                "cliente": "fernando",
                "produto": 3,
                "quantidade": 4
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Venda.objects.count(), 1)
        self.assertEqual(Venda.objects.get().pk, 1)
        self.assertEqual(ItemVenda.objects.count(), 3)
        self.assertEqual(ItemVenda.objects.get(id=1).produto.nome, "smartphone")
        self.assertEqual(ItemVenda.objects.get(id=2).produto.nome, "capa smartphone")
        self.assertEqual(ItemVenda.objects.get(id=3).produto.nome, "fone de ouvido")
