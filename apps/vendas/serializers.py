from django.db.models import Sum
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Produto, Vendedor, Cliente, Venda, ItemVenda


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ["id", "nome", "preco", "comissao"]


class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ["id", "nome"]


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["id", "nome"]


class ValorTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ["preco"]


class ItemVendaSerializer(serializers.ModelSerializer):
    produto = serializers.StringRelatedField()
    preco = ValorTotalSerializer(read_only=True, many=True)

    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade", "preco"]


class VendaSerializer(serializers.ModelSerializer):
    itens = serializers.SerializerMethodField()
    valor_total = serializers.SerializerMethodField()

    class Meta:
        model = Venda
        fields = ["id", "data_hora", "vendedor", "cliente", "valor_total", "itens"]

    def get_itens(self, obj):
        response = []
        contador = 0
        for item in ItemVenda.objects.filter(venda=obj):
            user_profile = ItemVendaSerializer(
                item,
                context={'request': self.context['request']})
            response.append(user_profile.data)
            response[contador]['preco'] = item.produto.preco
            contador += 1
        return response

    def get_valor_total(self, obj):
        response = []
        for item in ItemVenda.objects.filter(venda=obj):
            response.append(item.produto.preco)
        return sum(response)


class CriarVendaSerializer(serializers.ModelSerializer):
    cliente = serializers.CharField(default=0)
    vendedor = serializers.IntegerField(default=0)
    try:
        venda = int(Venda.objects.last().id) + 1
    except AttributeError:
        venda = 1

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(CriarVendaSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = ItemVenda
        fields = ['vendedor', 'cliente', 'produto', 'quantidade']
        depht = 1

    def create(self, validated_data):
        vendedor = Vendedor.objects.get(id=validated_data.pop('vendedor'))
        cliente_created = Cliente.objects.get_or_create(nome=validated_data.pop('cliente'))
        venda_created = Venda.objects.get_or_create(id=self.venda, cliente=cliente_created[0], vendedor=vendedor)
        item_venda = ItemVenda.objects.create(**validated_data, venda=venda_created[0])
        return {
            'vendedor': int(vendedor.pk),
            'cliente': cliente_created[0].nome,
            **validated_data
        }


class DataSerializer(serializers.Serializer):
    data_inicial = serializers.DateField()
    data_final = serializers.DateField()
