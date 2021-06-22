# Desafio AMcom

⚠ Utilizar o python 3.7.4

⚠ Utilizar virtualenv


## Descrição:

Esta é uma pequena aplicação que tem como objetivo a criação de clientes, vendedores, produtos e vendas dos produtos.;

A aplicação também fornece endpoints para criação (POST) e consulta (GET).

## Abordagem e Implementação:

A abordagem para realizar essa tarefa foi a criação de um modelo para os vendedores, no código chamado de Vendedor, 
um modelo para os clientes, no código chamado de Cliente, um modelo para os produtos, no código chamado de Produto,
um modelo para os vendas, no código chamado de Venda e um modelo para os itens da venda, no código chamado de ItemVenda.

Abaixo temos o código de Vendedor:

```
class Vendedor(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return self.nome
```

Abaixo temos o código de Cliente:

```
class Cliente(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return self.nome
```

Abaixo temos o código de Produto:

```
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    preco = models.DecimalField(max_digits=12, decimal_places=2)
    comissao = models.DecimalField(max_digits=4, decimal_places=2,
                                   validators=[MaxValueValidator(10), MinValueValidator(0)])

    def __str__(self):
        return self.nome

    def __unicode__(self):
        return self.nome
```

Abaixo temos o código de Venda:

```
class Venda(models.Model):
    data_hora = models.DateTimeField(auto_now_add=True)
    vendedor = models.ForeignKey("Vendedor", on_delete=models.PROTECT, blank=True, null=True)
    cliente = models.ForeignKey("Cliente", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)
```

Abaixo temos o código de ItemVenda:

```
class ItemVenda(models.Model):
    produto = models.ForeignKey("Produto", on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    venda = models.ForeignKey(Venda, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.produto)

    def __unicode__(self):
        return str(self.produto)
```

## Endpoints:

Para essa pequena API foram criados os seguintes endpoints:

| Endpoint               | Função                    | Método  | JSON                                                            |
|------------------------|---------------------------|---------|--------------------------------------------------------------------|
|/api/vendedores/     | Criar um vendedores         | POST    | {"nome": "nome do vendedor"}              |
|/api/vendedores/         | Mostra todos os vendedores  | GET     |            |
|/api/vendedores/pk/    | Dado o id de um vendedor, mostra os seus dados, podendo excluir o vendedor ou editar         | GET    |    |
|/api/vendedores/pk/comissao_por_periodo/    | Dado o id de um vendedor, podera ver todas as comissões do vendedor passando as datas no metodo       | GET    | {"data_inicial": "2017-01-01", "data_final": "2022-01-01"}    |
|/api/clientes/     | Criar um vendedores         | POST    | {"nome": "nome do cliente"}              |
|/api/clientes/         | Mostra todos os Clientes  | GET     |            |
|/api/clientes/pk/    | Dado o id de um Cliente, mostra os seus dados, podendo excluir o cliente ou editar         | GET    |    |
|/api/clientes/pk/produtos_comprados_no_periodo/    | Dado o id de um cliente, Apresenta os produtos e quantidade que o cliente comprou em um intervalo de datas.       | GET    | {"data_inicial": "2017-01-01", "data_final": "2022-01-01"}    |
|/api/produtos/     | Criar um vendedores         | POST    | {"nome": "nome do produto", "preco": valor do produto ex: 150.35 , "comissao": valor da comissao ex: 7.35}             |
|/api/produtos/         | Mostra todos os produtos  | GET     |            |
|/api/produtos/pk/    | Dado o id de um produto, mostra os seus dados, podendo excluir o produto ou editar         | GET    |    |
|/api/produtos/pk/produtos_mais_vendidos_por_periodo/    | Dado o id de um produto,         Apresenta os produtos mais vendidos em um intervalo de datas, apresentados em ordem decrescente     | GET    | {"data_inicial": "2017-01-01", "data_final": "2022-01-01"}    |
|/api/criarvenda/     | para criar uma venda.          | POST    | {"vendedor": id do vendedor ex.: 1, "cliente": "nome do cliente", "produto": id do vendedor ex.: 1,"quantidade": valor da quantidade ex.: 4 }             |
|/api/vendas/         | Mostra todas as vendas e itens da venda  | GET     |            |
|/api/vendas/pk/    | Dado o id de uma venda, mostra todos os dados da venda.         | GET    |    |


## Instalação

### Instalar as dependencias do python após ativação da virtualenv.
    pip install -r requirements.txt

### Criar o banco de dados
    createdb -h localhost -p 5432 -U postgres amcom

### Efetuar as migrações do banco
    python manage.py migrate

### Importar dados para testes
    python manage.py loaddata data/data.json

### Criar o super usuário
    python manage.py createsuperuser

### Para executar os testes
    python manage.py test

### Para executar a aplicação
    python manage.py runserver
    
## Como usar:

Ao executar a aplicação, pode ser acessada pelo link:

http://127.0.0.1:8000/

Como a aplicação é focada na sua API, nenhuma página retornará se o link acima for acessado, logo, 
é preciso ter em mente que essa aplicação só funcionará se algum dos endpoints acima for usado, por exemplo:

http://127.0.0.1:8000/api/vendedores/

Esse link retornará todas os vendedores cadastrados no sistema.

http://127.0.0.1:8000/api/clientes/

Esse link retornará todas os clientes cadastrados no sistema.

### Obs.: Pode-se criar uma venda com mais de um produto para isso é necessario passar um Json da seguinte forma.

### EX.:

```
[{
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
    "produto": 4,
    "quantidade": 4
}]
```
