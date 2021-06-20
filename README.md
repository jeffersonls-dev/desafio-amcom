# Desafio AMcom

⚠ Utilizar o python 3.7.4

⚠ Utilizar virtualenv

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
