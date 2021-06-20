from datetime import date, time
from collections import OrderedDict
from operator import itemgetter
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Produto, Vendedor, Cliente, Venda, ItemVenda
from .serializers import \
    ProdutoSerializer, VendedorSerializer, ClienteSerializer, VendaSerializer, DataSerializer, CriarVendaSerializer


class ProdutoViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API para ver ou editar produtos.
    """
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    @action(methods=['get'], detail=False)
    def produtos_mais_vendidos_por_periodo(self, request, pk=None):
        """
        Apresenta os produtos mais vendidos em um intervalo de datas, apresentados em ordem decrescente
        """
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            vendas_no_periodo = ItemVenda.objects.filter(
                venda__data_hora__gte=date.fromisoformat(serializer.data["data_inicial"]),
                venda__data_hora__lte=date.fromisoformat(serializer.data["data_final"]))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        produto_quantidade = {}
        for itemvenda in vendas_no_periodo:
            produto_quantidade.update({
                itemvenda.produto.nome: produto_quantidade.get(itemvenda.produto.nome, 0) + itemvenda.quantidade
            })

        produto_quantidade = OrderedDict(sorted(produto_quantidade.items(), key=itemgetter(1), reverse=True))
        return Response(produto_quantidade)


class VendedorViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API para ver ou editar vendedores.
    """
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

    @action(methods=['get'], detail=True)
    def comissao_por_periodo(self, request, pk=None):
        """
        Apresenta o valor total da comissão do vendedor em um intervalo de datas
        """
        vendedor = self.get_object()
        serializer = DataSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            vendas_no_periodo = ItemVenda.objects.filter(
                venda__vendedor=vendedor,
                venda__data_hora__gte=date.fromisoformat(serializer.data["data_inicial"]),
                venda__data_hora__lte=date.fromisoformat(serializer.data["data_final"]))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        valor_comissao = 0
        for itemvenda in vendas_no_periodo:
            if (itemvenda.venda.data_hora.time() >= time(0, 0)) and (itemvenda.venda.data_hora.time() <= time(12, 0)):
                comissao = min(itemvenda.produto.comissao, 5)
            else:
                comissao = max(itemvenda.produto.comissao, 4)
            print(itemvenda.produto.comissao)
            print(comissao)
            print(itemvenda.venda.data_hora.time())
            valor_comissao += ((itemvenda.produto.preco * itemvenda.quantidade) * comissao) / 100

        return Response({"valor_comissao": valor_comissao})


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Endpoint da API para ver ou editar clientes.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    @action(methods=['get'], detail=True)
    def produtos_comprados_no_periodo(self, request, pk=None):
        """
        Apresenta os produtos e quantidade que o cliente comprou em um intervalo de datas.
        """
        cliente = self.get_object()
        print(request.data)
        serializer = DataSerializer(data=request.data)

        if serializer.is_valid():
            vendas_no_periodo = ItemVenda.objects.filter(
                venda__cliente=cliente,
                venda__data_hora__gte=date.fromisoformat(serializer.data["data_inicial"]),
                venda__data_hora__lte=date.fromisoformat(serializer.data["data_final"]))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        produtos = []
        for itemvenda in vendas_no_periodo:
            produtos.append({
                itemvenda.produto.id: itemvenda.produto.nome,
                "quantidade": itemvenda.quantidade
            })
        return Response(produtos)


class VendaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint da API para ver as vendas.
    """
    serializer_class = VendaSerializer
    queryset = Venda.objects.all()


class ItemVendaViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    Endpoint da API para criar vendas.
    """
    serializer_class = CriarVendaSerializer
    queryset = ItemVenda.objects.all()

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]

            if isinstance(data, list):
                kwargs["many"] = True

        return super(ItemVendaViewSet, self).get_serializer(*args, **kwargs)
