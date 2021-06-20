from django.contrib import admin
from .models import Venda, Produto, Vendedor, Cliente, ItemVenda


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "comissao")
    exclude = ("venda",)


@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display = ("nome",)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome",)


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ("data_hora", "vendedor", "cliente",)


@admin.register(ItemVenda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ("produto", "quantidade", "venda",)
