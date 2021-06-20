from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    comissao = models.DecimalField(max_digits=4, decimal_places=2,
                                   validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return self.nome


class Vendedor(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return self.nome


class Venda(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey("Vendedor", on_delete=models.PROTECT, blank=True, null=True)
    cliente = models.ForeignKey("Cliente", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)


class ItemVenda(models.Model):
    produto = models.ForeignKey("Produto", on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.produto)

    def __unicode__(self):
        return str(self.produto)
